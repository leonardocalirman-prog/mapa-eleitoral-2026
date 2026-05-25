"""Lógica do nowcasting eleitoral por UF."""

from __future__ import annotations

from typing import Mapping

import pandas as pd

from data.resultados_2022 import RESULTADOS_2022


def classificar_margem(margem: float) -> tuple[str, int]:
    """
    Classifica a margem Lula - Bolsonaro em cinco buckets.

    Retorna (label, ordem), onde ordem é usada para manter a legenda estável.
    """
    if margem > 20:
        return "Sólido esquerda", 4
    if margem > 5:
        return "Provável esquerda", 3
    if margem >= -5:
        return "Competitivo", 2
    if margem >= -20:
        return "Provável direita", 1
    return "Sólido direita", 0


def calcular_margens(
    swing_nacional: float = -5.0,
    ajustes_estaduais: Mapping[str, float] | None = None,
) -> pd.DataFrame:
    """
    Calcula a margem estimada por UF.

    Fórmula:
        margem_estimada = margem_2022 + swing_nacional + ajuste_estadual

    Convenção:
        margem positiva favorece esquerda/Lula.
        margem negativa favorece direita/Bolsonaro.
    """
    ajustes_estaduais = ajustes_estaduais or {}

    df = pd.DataFrame(RESULTADOS_2022)
    df["margem_2022"] = df["lula_pct"] - df["bolsonaro_pct"]
    df["ajuste_estadual"] = df["uf"].map(lambda uf: float(ajustes_estaduais.get(uf, 0.0)))
    df["swing_nacional"] = float(swing_nacional)
    df["margem_estimada"] = df["margem_2022"] + df["swing_nacional"] + df["ajuste_estadual"]

    classificacoes = df["margem_estimada"].map(classificar_margem)
    df["label"] = classificacoes.map(lambda x: x[0])
    df["categoria_ordem"] = classificacoes.map(lambda x: x[1])

    # Campos formatados para hover/terminal.
    df["margem_2022_fmt"] = df["margem_2022"].map(lambda x: f"{x:+.1f} pp")
    df["margem_estimada_fmt"] = df["margem_estimada"].map(lambda x: f"{x:+.1f} pp")
    df["lula_pct_fmt"] = df["lula_pct"].map(lambda x: f"{x:.2f}%")
    df["bolsonaro_pct_fmt"] = df["bolsonaro_pct"].map(lambda x: f"{x:.2f}%")

    return df.sort_values("uf").reset_index(drop=True)


def resumo(df: pd.DataFrame) -> dict[str, int]:
    """Resumo agregado por bloco de classificação."""
    counts = df["label"].value_counts().to_dict()
    solido_esq = counts.get("Sólido esquerda", 0)
    provavel_esq = counts.get("Provável esquerda", 0)
    competitivo = counts.get("Competitivo", 0)
    provavel_dir = counts.get("Provável direita", 0)
    solido_dir = counts.get("Sólido direita", 0)

    return {
        "solido_esq": solido_esq,
        "provavel_esq": provavel_esq,
        "competitivo": competitivo,
        "provavel_dir": provavel_dir,
        "solido_dir": solido_dir,
        "total_esq": solido_esq + provavel_esq,
        "total_dir": provavel_dir + solido_dir,
    }
