"""
prep_data.py - Prepara os dados para o dashboard Quarto/Observable.

Quando rodar:
    - Antes de quarto render/preview pela primeira vez.
    - Sempre que mexer em data/*.py ou tracker/*.py.
    - O GitHub Action publish.yml ja chama esse script automaticamente.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.resultados_2022 import RESULTADOS_2022
from src.mapa import _get_geojson
from src import pesquisas
from src import backtest

DATA_DIR       = os.path.join(os.path.dirname(__file__), "data")
JSON_PATH      = os.path.join(DATA_DIR, "resultados_2022.json")
PESQUISAS_PATH = os.path.join(DATA_DIR, "pesquisas_mediana.json")
BACKTEST_PATH  = os.path.join(DATA_DIR, "backtest_2018_2022.json")


def gerar_json_resultados() -> None:
    registros = []
    for uf, d in RESULTADOS_2022.items():
        registros.append({
            "uf": uf, "nome": d["nome"], "regiao": d["regiao"],
            "lula_2022": d["lula"], "bolso_2022": d["bolso"],
            "margem_2022": d["margem"], "votos_validos": d["votos_validos"],
        })
    registros.sort(key=lambda r: r["uf"])
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=2)
    print(f"OK  resultados_2022.json gerado ({len(registros)} UFs)")


def garantir_geojson() -> None:
    _get_geojson()
    print("OK  br_states.geojson disponivel em data/")


def gerar_json_pesquisas(dias: int = 30) -> None:
    import datetime as dt
    import statistics

    MANUAL_PATH = os.path.join(DATA_DIR, "pesquisas_manual.json")
    try:
        with open(MANUAL_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
        lista = raw.get("pesquisas", [])
        registros = []
        for p in lista:
            esq, dir_ = p.get("esquerda_pct"), p.get("direita_pct")
            if esq is None or dir_ is None:
                continue
            registros.append({
                "data": dt.datetime.strptime(p["data"], "%Y-%m-%d"),
                "esquerda": esq, "direita": dir_, "margem": esq - dir_,
                "instituto": p.get("instituto", ""),
            })
        if not registros:
            med = {"esquerda": None, "direita": None, "margem": None,
                   "n_pesquisas": 0, "fonte": "manual vazio",
                   "erro": "Edite data/pesquisas_manual.json."}
        else:
            corte = dt.datetime.now() - dt.timedelta(days=dias)
            recente = [r for r in registros if r["data"] >= corte]
            fonte = f"manual, ultimos {dias}d"
            if not recente:
                recente = sorted(registros, key=lambda r: -r["data"].timestamp())[:5]
                fonte = "manual, ultimas 5"
            med = {
                "esquerda": round(statistics.median(r["esquerda"] for r in recente), 1),
                "direita": round(statistics.median(r["direita"] for r in recente), 1),
                "margem": round(statistics.median(r["margem"] for r in recente), 1),
                "n_pesquisas": len(recente),
                "data_min": min(r["data"] for r in recente).date().isoformat(),
                "data_max": max(r["data"] for r in recente).date().isoformat(),
                "fonte": fonte,
            }
        med["atualizado_em"] = dt.datetime.now().isoformat()
        status = "OK"
    except Exception as e:
        med = {"erro": f"{e.__class__.__name__}: {e}",
               "esquerda": None, "direita": None, "margem": None,
               "n_pesquisas": 0, "atualizado_em": dt.datetime.now().isoformat()}
        status = f"ERRO ({e.__class__.__name__})"

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PESQUISAS_PATH, "w", encoding="utf-8") as f:
        json.dump(med, f, ensure_ascii=False, indent=2)
    print(f"{status}  pesquisas_mediana.json (n={med.get('n_pesquisas', 0)})")


def gerar_json_backtest() -> None:
    import datetime as dt
    r = backtest.rodar()
    r["atualizado_em"] = dt.datetime.now().isoformat()
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(BACKTEST_PATH, "w", encoding="utf-8") as f:
        json.dump(r, f, ensure_ascii=False, indent=2)
    mae_a = r["modelo_A_nacional"]["mae_pp"]
    mae_b = r["modelo_B_regional"]["mae_pp"]
    print(f"OK  backtest_2018_2022.json (MAE A={mae_a} pp | B={mae_b} pp)")


def gerar_tracker() -> None:
    """Pipeline V3 do tracker."""
    from tracker import clean, house_effects, agregador, probabilidade

    RAW_2026 = os.path.join(DATA_DIR, "pesquisas_2026_raw.csv")
    RAW_2022 = os.path.join(DATA_DIR, "pesquisas_2022_raw.csv")
    CSV_2026 = os.path.join(DATA_DIR, "pesquisas_2026.csv")
    CSV_2022 = os.path.join(DATA_DIR, "pesquisas_2022_finais.csv")
    HE_PATH = os.path.join(DATA_DIR, "house_effects.json")
    AGG_PATH = os.path.join(DATA_DIR, "tracker_agregado.json")
    SERIE_PATH = os.path.join(DATA_DIR, "tracker_serie.json")

    try:
        from tracker import ingest, ingest_2022
        ingest.main()
        ingest_2022.main()
        clean.processar(RAW_2026, CSV_2026)
        clean.processar(RAW_2022, CSV_2022)
        ingest_status = "OK ingest Wikipedia + clean"
    except Exception as e:
        print(f"  AVISO ingest falhou ({e.__class__.__name__}): {e}")
        print(f"  -> usando CSVs limpos versionados")
        ingest_status = "FALLBACK (CSVs versionados)"
        if not (os.path.exists(CSV_2026) and os.path.exists(CSV_2022)):
            print(f"  ERRO: nem CSVs versionados existem. Tracker abortado.")
            return

    import pandas as pd
    df_2022 = pd.read_csv(CSV_2022)
    he = house_effects.calcular(df_2022)
    with open(HE_PATH, "w", encoding="utf-8") as f:
        json.dump(he, f, ensure_ascii=False, indent=2)

    df_2026 = pd.read_csv(CSV_2026)
    pesos = agregador.carregar_pesos_institutos()
    snap, serie = agregador.processar(df_2026, he, pesos)

    snap["probabilidades"] = probabilidade.calcular_probabilidades(snap["gap_corrigido"])
    snap["sigmas_cenarios"] = probabilidade.CENARIOS_SIGMA
    snap["bias_2022_aplicado"] = he["bias_agregado"]
    snap["fonte_ingest"] = ingest_status

    with open(AGG_PATH, "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=2, default=str)
    with open(SERIE_PATH, "w", encoding="utf-8") as f:
        json.dump(serie, f, ensure_ascii=False, indent=2, default=str)

    p_base = snap["probabilidades"]["base"]
    print(f"OK  tracker  gap_bruto={snap['gap_bruto']:+.2f}  gap_corr={snap['gap_corrigido']:+.2f}  P(Lula) base={p_base}%  n={snap['n_pesquisas']}")


if __name__ == "__main__":
    print("-- Preparando dados para o dashboard --")
    gerar_json_resultados()
    garantir_geojson()
    gerar_json_pesquisas()
    gerar_json_backtest()
    gerar_tracker()
    print("Pronto. Agora rode: quarto preview")
