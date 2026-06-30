"""
tracker/agregador.py - Agregacao ponderada das pesquisas 2026.

Pondera cada pesquisa pelo produto de tres pesos:
    - w_recencia: decaimento exponencial com meia-vida de 14 dias
    - w_amostra: sqrt(n), com cap em 3000 (ate sqrt(3000) ~= 55)
    - w_instituto: tabela editavel em tracker/pesos_institutos.csv (default 1.0)

Aplica house_effect por pesquisa (correcao_bias_instituto ou fallback agregado)
antes de agregar.

Produz:
    - tracker_agregado.json: snapshot atual (gap bruto, gap corrigido, n, ultima_data)
    - tracker_serie.json:    serie temporal por pesquisa + curva agregada rolling
"""

from __future__ import annotations
import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np

MEIA_VIDA_DIAS = 14
CAP_AMOSTRA = 3000


def peso_recencia(data: datetime, hoje: datetime, meia_vida: int = MEIA_VIDA_DIAS) -> float:
    """Decaimento exponencial. Pesquisa de hoje peso 1.0; de meia_vida dias atras peso 0.5."""
    dias = max(0, (hoje - data).days)
    return math.exp(-math.log(2) * dias / meia_vida)


def peso_amostra(n) -> float:
    """sqrt(n) com cap. Pesquisas muito grandes nao dominam."""
    if pd.isna(n) or n <= 0:
        return 1.0
    return math.sqrt(min(int(n), CAP_AMOSTRA))


def peso_instituto(inst: str, tabela: Dict[str, float]) -> float:
    """Olha em tabela de pesos editavel. Default 1.0 se instituto desconhecido."""
    return tabela.get(inst, 1.0)


def carregar_pesos_institutos(path: str = "tracker/pesos_institutos.csv") -> Dict[str, float]:
    df = pd.read_csv(path)
    return dict(zip(df["instituto_canonico"], df["peso_default"]))


def corrigir_por_instituto(row, house_effects: Dict) -> float:
    """gap - bias_do_instituto (ou bias_agregado se instituto sem vies individual)."""
    inst = row["instituto"]
    bias_info = house_effects.get("por_instituto", {}).get(inst)
    if bias_info:
        bias = bias_info["bias_pp"]
    else:
        bias = house_effects.get("bias_agregado", 0.0)
    return row["gap_lula_flavio"] - bias


def processar(
    df_2026: pd.DataFrame,
    house_effects: Dict,
    pesos_institutos: Dict[str, float] | None = None,
    hoje: datetime | None = None,
) -> Tuple[Dict, Dict]:
    """
    Retorna (snapshot, serie):
        snapshot = {gap_bruto, gap_corrigido, n_pesquisas, ultima_data, ...}
        serie    = {pontos: [...], agregado_rolling: [...]}
    """
    hoje = hoje or datetime.now()
    pesos_institutos = pesos_institutos or {}

    df = df_2026.copy()
    df["data_fim_campo"] = pd.to_datetime(df["data_fim_campo"])

    # corrigir cada pesquisa pelo house effect
    df["gap_corrigido"] = df.apply(lambda r: corrigir_por_instituto(r, house_effects), axis=1)

    # pesos
    df["w_recencia"] = df["data_fim_campo"].apply(lambda d: peso_recencia(d, hoje))
    df["w_amostra"] = df["amostra"].apply(peso_amostra)
    df["w_instituto"] = df["instituto"].apply(lambda i: peso_instituto(i, pesos_institutos))
    df["w_total"] = df["w_recencia"] * df["w_amostra"] * df["w_instituto"]

    # snapshot
    soma_w = df["w_total"].sum()
    gap_bruto = float((df["gap_lula_flavio"] * df["w_total"]).sum() / soma_w)
    gap_corrigido = float((df["gap_corrigido"] * df["w_total"]).sum() / soma_w)

    snapshot = {
        "gap_bruto": round(gap_bruto, 2),
        "gap_corrigido": round(gap_corrigido, 2),
        "n_pesquisas": int(len(df)),
        "ultima_data": df["data_fim_campo"].max().isoformat(),
        "primeira_data": df["data_fim_campo"].min().isoformat(),
        "meia_vida_dias": MEIA_VIDA_DIAS,
        "atualizado_em": hoje.isoformat(),
    }

    # serie temporal: pontos individuais
    pontos = []
    for _, r in df.sort_values("data_fim_campo").iterrows():
        pontos.append({
            "poll_id": r["poll_id"],
            "instituto": r["instituto"],
            "data": r["data_fim_campo"].isoformat(),
            "gap_bruto": round(float(r["gap_lula_flavio"]), 2),
            "gap_corrigido": round(float(r["gap_corrigido"]), 2),
            "amostra": int(r["amostra"]) if not pd.isna(r["amostra"]) else None,
        })

    # agregado rolling: para cada data unica, calcula agregado das pesquisas dos ultimos 30 dias
    rolling = []
    datas = sorted(df["data_fim_campo"].unique())
    for d in datas:
        d_dt = pd.Timestamp(d).to_pydatetime()
        janela = df[df["data_fim_campo"] <= d_dt]
        janela = janela[janela["data_fim_campo"] >= d_dt - timedelta(days=30)]
        if len(janela) >= 2:
            # recalcula pesos relativos a essa data como "hoje"
            w_rec = janela["data_fim_campo"].apply(lambda x: peso_recencia(x, d_dt))
            w_amo = janela["amostra"].apply(peso_amostra)
            w_inst = janela["instituto"].apply(lambda i: peso_instituto(i, pesos_institutos))
            w = w_rec * w_amo * w_inst
            gap_rolling = float((janela["gap_corrigido"] * w).sum() / w.sum())
            rolling.append({
                "data": d_dt.isoformat(),
                "gap_corrigido": round(gap_rolling, 2),
                "n_janela": int(len(janela)),
            })

    serie = {"pontos": pontos, "agregado_rolling": rolling}
    return snapshot, serie


if __name__ == "__main__":
    df_2026 = pd.read_csv("data/pesquisas_2026.csv")
    with open("data/house_effects.json", encoding="utf-8") as f:
        he = json.load(f)
    pesos = carregar_pesos_institutos()
    snap, serie = processar(df_2026, he, pesos)
    with open("data/tracker_agregado.json", "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=2)
    with open("data/tracker_serie.json", "w", encoding="utf-8") as f:
        json.dump(serie, f, ensure_ascii=False, indent=2)
    print(f"OK agregador  gap_bruto {snap['gap_bruto']:+.2f}  gap_corrigido {snap['gap_corrigido']:+.2f}  n={snap['n_pesquisas']}")
