"""
prep_data.py — Prepara os dados para o dashboard Quarto/Observable.

Por que existe:
    O dashboard interativo roda no browser (Observable JS). Ele não consegue
    importar um .py diretamente. Esse script converte o dicionário Python
    (resultados_2022.py) em JSON e garante que o GeoJSON do IBGE esteja em disco.

Rodar:
    python prep_data.py
    # Gera: data/resultados_2022.json e data/br_states.geojson

Quando rodar:
    - Antes de `quarto render` (ou `quarto preview`) pela primeira vez.
    - Sempre que mexer em resultados_2022.py.
    - O GitHub Action (publish.yml) já chama esse script automaticamente.
"""

import json
import os
import sys

# permite rodar de qualquer diretório
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.resultados_2022 import RESULTADOS_2022
from src.mapa import _get_geojson  # reaproveita o download/cache do IBGE
from src import pesquisas
from src import backtest

DATA_DIR       = os.path.join(os.path.dirname(__file__), "data")
JSON_PATH      = os.path.join(DATA_DIR, "resultados_2022.json")
PESQUISAS_PATH = os.path.join(DATA_DIR, "pesquisas_mediana.json")
BACKTEST_PATH  = os.path.join(DATA_DIR, "backtest_2018_2022.json")


def gerar_json_resultados() -> None:
    """Serializa RESULTADOS_2022 como JSON (lista, não dict, pra facilitar no JS)."""
    registros = []
    for uf, d in RESULTADOS_2022.items():
        registros.append({
            "uf":             uf,
            "nome":           d["nome"],
            "regiao":         d["regiao"],
            "lula_2022":      d["lula"],
            "bolso_2022":     d["bolso"],
            "margem_2022":    d["margem"],
            "votos_validos":  d["votos_validos"],
        })

    # ordenado por UF para diffs limpos no git
    registros.sort(key=lambda r: r["uf"])

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=2)

    print(f"OK  resultados_2022.json gerado ({len(registros)} UFs) -> {JSON_PATH}")


def garantir_geojson() -> None:
    """Baixa e cacheia o GeoJSON dos estados (uma única vez)."""
    _get_geojson()  # função já existente em src/mapa.py
    print("OK  br_states.geojson disponível em data/")


def gerar_json_pesquisas(dias: int = 30) -> None:
    """
    Le data/pesquisas_manual.json (preenchido a mao pelo usuario) e
    calcula a mediana das margens nos ultimos N dias. Mais robusto que
    scraping da Wikipedia (que muda de layout sem aviso).

    Fallback: se o arquivo manual nao existe ou esta mal formatado, salva
    um JSON com erro - o dashboard mostra mensagem amigavel.
    """
    import datetime as dt
    import statistics

    MANUAL_PATH = os.path.join(DATA_DIR, "pesquisas_manual.json")
    try:
        with open(MANUAL_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
        lista = raw.get("pesquisas", [])

        # filtra pesquisas com numeros validos e calcula margem
        registros = []
        for p in lista:
            esq, dir_ = p.get("esquerda_pct"), p.get("direita_pct")
            if esq is None or dir_ is None:
                continue
            registros.append({
                "data": dt.datetime.strptime(p["data"], "%Y-%m-%d"),
                "esquerda": esq,
                "direita":  dir_,
                "margem":   esq - dir_,
                "instituto": p.get("instituto", ""),
            })

        if not registros:
            med = {"esquerda": None, "direita": None, "margem": None,
                   "n_pesquisas": 0, "fonte": "manual vazio",
                   "erro": "Edite data/pesquisas_manual.json com dados reais."}
        else:
            corte   = dt.datetime.now() - dt.timedelta(days=dias)
            recente = [r for r in registros if r["data"] >= corte]
            fonte   = f"manual, ultimos {dias}d"
            if not recente:
                recente = sorted(registros, key=lambda r: -r["data"].timestamp())[:5]
                fonte   = "manual, ultimas 5 (sem dado recente)"
            med = {
                "esquerda":    round(statistics.median(r["esquerda"] for r in recente), 1),
                "direita":     round(statistics.median(r["direita"]  for r in recente), 1),
                "margem":      round(statistics.median(r["margem"]   for r in recente), 1),
                "n_pesquisas": len(recente),
                "data_min":    min(r["data"] for r in recente).date().isoformat(),
                "data_max":    max(r["data"] for r in recente).date().isoformat(),
                "fonte":       fonte,
            }
        med["atualizado_em"] = dt.datetime.now().isoformat()
        status = "OK"
    except Exception as e:
        med = {"erro": f"{e.__class__.__name__}: {e}",
               "esquerda": None, "direita": None, "margem": None,
               "n_pesquisas": 0,
               "atualizado_em": dt.datetime.now().isoformat()}
        status = f"ERRO ({e.__class__.__name__})"

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PESQUISAS_PATH, "w", encoding="utf-8") as f:
        json.dump(med, f, ensure_ascii=False, indent=2)
    print(f"{status}  pesquisas_mediana.json (n={med.get('n_pesquisas', 0)}) -> {PESQUISAS_PATH}")


def gerar_json_backtest() -> None:
    """Roda o backtest 2018->2022 e salva o resultado em JSON."""
    import datetime as dt
    r = backtest.rodar()
    r["atualizado_em"] = dt.datetime.now().isoformat()
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(BACKTEST_PATH, "w", encoding="utf-8") as f:
        json.dump(r, f, ensure_ascii=False, indent=2)
    mae_a = r["modelo_A_nacional"]["mae_pp"]
    mae_b = r["modelo_B_regional"]["mae_pp"]
    print(f"OK  backtest_2018_2022.json (MAE A={mae_a} pp | B={mae_b} pp) -> {BACKTEST_PATH}")


if __name__ == "__main__":
    print("-- Preparando dados para o dashboard --")
    gerar_json_resultados()
    garantir_geojson()
    gerar_json_pesquisas()
    gerar_json_backtest()
    print("Pronto. Agora rode: quarto preview  (ou: quarto render)")
