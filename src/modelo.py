"""
modelo.py — Lógica central do nowcasting eleitoral.

Fórmula V1:
    margem_estimada(UF) = margem_2022(UF) + swing_nacional + ajuste_estadual

Classificação:
    > +20pp  → Sólido esquerda
    +5 a +20 → Provável esquerda
    -5 a +5  → Competitivo
    -5 a -20 → Provável direita
    < -20pp  → Sólido direita
"""

import pandas as pd
from data.resultados_2022 import RESULTADOS_2022


THRESHOLDS = [
    (+20, "solido_esq"),
    (+5,  "provavel_esq"),
    (-5,  "competitivo"),
    (-20, "provavel_dir"),
    (None,"solido_dir"),
]

LABELS = {
    "solido_esq":   "Sólido esquerda",
    "provavel_esq": "Provável esquerda",
    "competitivo":  "Competitivo",
    "provavel_dir": "Provável direita",
    "solido_dir":   "Sólido direita",
}

COLORS = {
    "solido_esq":   "#185FA5",
    "provavel_esq": "#85B7EB",
    "competitivo":  "#B4B2A9",
    "provavel_dir": "#F0997B",
    "solido_dir":   "#993C1D",
}


def classificar(margem: float) -> str:
    for limiar, classe in THRESHOLDS:
        if limiar is None or margem > limiar:
            return classe
    return "solido_dir"


def calcular_margens(
    swing_nacional: float = 0.0,
    ajustes_estaduais: dict | None = None
) -> pd.DataFrame:
    """
    Retorna DataFrame com margem estimada e classificação por UF.

    Parâmetros
    ----------
    swing_nacional : float
        Variação uniforme em pontos percentuais aplicada a todas as UFs.
        Positivo = melhor para esquerda; negativo = melhor para direita.
    ajustes_estaduais : dict, opcional
        Dicionário {UF: ajuste_pp} para ajustes específicos por estado.
        Ex: {"SP": -3, "MG": +2}

    Retorna
    -------
    pd.DataFrame com colunas:
        uf, nome, regiao, margem_2022, swing_nacional, ajuste_estadual,
        margem_estimada, classificacao, label, cor
    """
    if ajustes_estaduais is None:
        ajustes_estaduais = {}

    rows = []
    for uf, d in RESULTADOS_2022.items():
        ajuste_local = ajustes_estaduais.get(uf, 0.0)
        margem_est   = d["margem"] + swing_nacional + ajuste_local
        classe       = classificar(margem_est)
        rows.append({
            "uf":              uf,
            "nome":            d["nome"],
            "regiao":          d["regiao"],
            "lula_2022":       d["lula"],
            "bolso_2022":      d["bolso"],
            "margem_2022":     d["margem"],
            "swing_nacional":  swing_nacional,
            "ajuste_estadual": ajuste_local,
            "margem_estimada": round(margem_est, 1),
            "classificacao":   classe,
            "label":           LABELS[classe],
            "cor":             COLORS[classe],
        })

    return pd.DataFrame(rows).sort_values("margem_estimada", ascending=False)


def resumo(df: pd.DataFrame) -> dict:
    """Agrega o DataFrame de margens em contagens por classificação."""
    counts = df["classificacao"].value_counts().to_dict()
    return {
        "solido_esq":   counts.get("solido_esq",   0),
        "provavel_esq": counts.get("provavel_esq", 0),
        "competitivo":  counts.get("competitivo",  0),
        "provavel_dir": counts.get("provavel_dir", 0),
        "solido_dir":   counts.get("solido_dir",   0),
        "total_esq":    counts.get("solido_esq", 0) + counts.get("provavel_esq", 0),
        "total_dir":    counts.get("solido_dir", 0) + counts.get("provavel_dir", 0),
    }
