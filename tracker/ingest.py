"""
tracker/ingest.py - Scraper das pesquisas presidenciais 2026 (Wikipedia EN).

Por que Wikipedia EN e nao PT?
    A versao em ingles tem tabelas estruturalmente mais consistentes (separadas
    por cenario com headers claros), enquanto a PT mistura tudo. Os dados sao
    os mesmos (mesma fonte primaria: institutos), so muda o formato da pagina.

Use:
    python -m tracker.ingest               # baixa, parseia, salva CSV bruto
    python -m tracker.ingest --debug       # imprime info de cada tabela
"""

from __future__ import annotations
import argparse
import io
import re
import sys
from typing import List, Optional
import pandas as pd
import requests
from bs4 import BeautifulSoup

URL_EN = (
    "https://en.wikipedia.org/wiki/"
    "Opinion_polling_for_the_2026_Brazilian_presidential_election"
)

OUTPUT_PATH = "data/pesquisas_2026_raw.csv"

# Nomes (substring case-insensitive) que indicam cenario "Lula vs Flavio direto".
# Tipicamente aparecem como headers da tabela ou como contexto antes dela.
CENARIO_LULA_FLAVIO_KEYS = ["lula", "f. bolsonaro", "flávio bolsonaro", "flavio bolsonaro"]


def baixar_html(url: str = URL_EN, timeout: int = 30) -> str:
    print(f"GET {url}")
    r = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": "mapa-eleitoral-2026/0.3 (+github.com/leonardocalirman-prog)"},
    )
    r.raise_for_status()
    return r.text


def extrair_tabelas(html: str) -> List[pd.DataFrame]:
    """Retorna todas as tabelas wikitable como DataFrames, na ordem em que aparecem."""
    soup = BeautifulSoup(html, "lxml")
    tabelas_raw = soup.find_all("table", class_="wikitable")
    dfs = []
    for i, t in enumerate(tabelas_raw):
        try:
            df = pd.read_html(io.StringIO(str(t)))[0]
            # achata multi-index header se houver
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [
                    " | ".join(str(c) for c in col if str(c) != "nan").strip()
                    for col in df.columns
                ]
            dfs.append(df)
        except Exception as e:
            print(f"  tab#{i}: skip ({e.__class__.__name__})")
    return dfs


def identificar_tabela_lula_flavio(dfs: List[pd.DataFrame], debug: bool = False) -> Optional[int]:
    """
    Encontra a tabela cuja header contem colunas tanto para Lula quanto para Flavio Bolsonaro.
    Retorna o indice da tabela, ou None se nao achar.
    """
    for i, df in enumerate(dfs):
        cols = [str(c).lower() for c in df.columns]
        tem_lula = any("lula" in c for c in cols)
        tem_flavio = any(("flavio" in c or "flávio" in c or "f. bolso" in c or "bolsonaro" in c) for c in cols)
        if debug:
            preview = cols[:6]
            print(f"  tab#{i}: lula={tem_lula} flavio={tem_flavio} cols={preview}")
        if tem_lula and tem_flavio:
            return i
    return None


def extrair_colunas(df: pd.DataFrame) -> dict:
    """Identifica colunas relevantes (data, instituto, lula, flavio, amostra)."""
    mapping = {}
    for col in df.columns:
        c = str(col).lower().strip()
        if "pollster" in c or "instit" in c or "empresa" in c or "fonte" in c:
            mapping.setdefault("instituto", col)
        elif "period" in c or "data" in c:
            mapping.setdefault("data_fim", col)
        elif re.search(r"^lula(\b|$)", c) and "%" not in c:
            mapping.setdefault("pct_lula", col)
        elif ("lula" in c and ("pt" in c or "%" in c)) or c == "lula":
            mapping.setdefault("pct_lula", col)
        elif "flavio" in c or "flávio" in c or "f. bolso" in c or (("bolso" in c) and "f" in c[:2]):
            mapping.setdefault("pct_flavio", col)
        elif "sample" in c or "amostra" in c:
            mapping.setdefault("amostra", col)
    return mapping


def parsear_tabela(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza colunas para schema bruto comum (instituto, data_fim, pct_lula, pct_flavio, amostra)."""
    mapping = extrair_colunas(df)
    if "pct_lula" not in mapping or "pct_flavio" not in mapping:
        raise ValueError(f"colunas Lula/Flavio nao encontradas. cols={list(df.columns)[:8]}")

    out = pd.DataFrame()
    out["instituto"] = df.get(mapping.get("instituto", ""), "")
    out["data_fim"] = df.get(mapping.get("data_fim", ""), "")
    out["pct_lula"] = df[mapping["pct_lula"]]
    out["pct_flavio"] = df[mapping["pct_flavio"]]
    out["amostra"] = df.get(mapping.get("amostra", ""), "")
    out["cenario"] = "Lula vs Flávio direto"
    out["candidato_b"] = "F. Bolsonaro (PL)"
    out["fonte_url"] = URL_EN
    return out


def main(debug: bool = False) -> pd.DataFrame:
    html = baixar_html()
    dfs = extrair_tabelas(html)
    print(f"  encontradas {len(dfs)} tabelas wikitable")

    idx = identificar_tabela_lula_flavio(dfs, debug=debug)
    if idx is None:
        print("ERRO: nao encontrou tabela com colunas Lula e Flavio Bolsonaro.")
        print("Listando primeiras colunas de cada tabela para diagnostico:")
        for i, df in enumerate(dfs[:10]):
            print(f"  tab#{i}: {list(df.columns)[:5]}")
        sys.exit(1)

    print(f"  usando tabela #{idx}")
    out = parsear_tabela(dfs[idx])
    print(f"  extraidas {len(out)} linhas brutas")

    # remove linhas obviamente invalidas (sem instituto OU sem pct_lula)
    out_valid = out[out["instituto"].notna() & (out["instituto"].astype(str).str.strip() != "")].copy()

    out_valid.to_csv(OUTPUT_PATH, index=False)
    print(f"OK ingest  -> {OUTPUT_PATH}  ({len(out_valid)} pesquisas)")
    return out_valid


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--debug", action="store_true", help="imprime detalhes de cada tabela")
    args = ap.parse_args()
    main(debug=args.debug)
