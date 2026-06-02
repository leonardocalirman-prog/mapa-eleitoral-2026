"""
pesquisas.py - Scraper das pesquisas de intencao de voto presidencial 2026 (Wikipedia PT).

Como funciona:
    1. Baixa a pagina da Wikipedia
    2. Itera por todas as tabelas wikitable
    3. Para cada tabela: identifica colunas de data e candidatos
    4. Agrupa candidatos em 'esquerda' / 'direita' por nome conhecido
    5. Extrai linha a linha, somando % de cada bloco

Use:
    python -m src.pesquisas              # roda e imprime debug + mediana
    python -m src.pesquisas --json out.json   # salva resultado em JSON
"""

from __future__ import annotations
import re, io, json, sys, argparse
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = ("https://pt.wikipedia.org/wiki/"
       "Pesquisas_de_opini%C3%A3o_para_a_elei%C3%A7%C3%A3o_presidencial_no_Brasil_em_2026")

# Listas para agrupar candidatos por bloco politico.
# Use sempre lowercase aqui — o match é case-insensitive.
NOMES_ESQUERDA = ["lula", "haddad", "marina", "boulos", "fernando haddad"]
NOMES_DIREITA  = ["bolsonaro", "tarcisio", "tarcísio", "zema", "ratinho",
                  "ronaldo caiado", "caiado", "michelle", "eduardo bolsonaro",
                  "moro", "sergio moro", "sérgio moro", "valdemar",
                  "pablo marçal", "marçal"]

MESES = {"jan":1,"fev":2,"mar":3,"abr":4,"mai":5,"jun":6,
         "jul":7,"ago":8,"set":9,"out":10,"nov":11,"dez":12}

def _parse_data(s: str) -> Optional[datetime]:
    """Datas no formato Wikipedia: '12-15 fev 2026', '15 fev 2026', '15/02/2026', etc."""
    if not s or s == "nan": return None
    s = str(s).strip().lower()
    # pega a ultima data do range se for "10-15 fev 2026"
    s = re.split(r"\s*[-–—]\s*", s)[-1]
    m = re.search(r"(\d{1,2})\s*(?:de\s*)?([a-zç]{3,})\.?\s*(?:de\s*)?(\d{4})", s)
    if m:
        d, mes, y = m.group(1), m.group(2)[:3], m.group(3)
        if mes in MESES:
            try: return datetime(int(y), MESES[mes], int(d))
            except ValueError: return None
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try: return datetime.strptime(s, fmt)
        except ValueError: continue
    return None

def _parse_pct(s) -> Optional[float]:
    if pd.isna(s): return None
    s = str(s)
    m = re.search(r"(\d+[,.]?\d*)", s)
    return float(m.group(1).replace(",", ".")) if m else None

def _identificar_lado(cabecalho: str) -> Optional[str]:
    txt = str(cabecalho).lower()
    if any(n in txt for n in NOMES_ESQUERDA): return "esq"
    if any(n in txt for n in NOMES_DIREITA):  return "dir"
    return None

def baixar(timeout: int = 30, debug: bool = True) -> pd.DataFrame:
    print(f"GET {URL}")
    r = requests.get(URL, timeout=timeout, headers={"User-Agent": "mapa-eleitoral-2026/0.2"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    tabelas = soup.find_all("table", class_="wikitable")
    print(f"  encontradas {len(tabelas)} tabelas wikitable")

    registros = []
    for tab_idx, table in enumerate(tabelas):
        try:
            df = pd.read_html(io.StringIO(str(table)))[0]
        except Exception as e:
            if debug: print(f"  tab#{tab_idx}: skip ({e.__class__.__name__})")
            continue

        # flatten multi-header se houver
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [" ".join(str(c) for c in col if str(c) != "nan") for col in df.columns]

        cols = list(df.columns)
        col_data = next((c for c in cols if re.search(r"data|per[ií]odo", str(c), re.I)), None)
        col_inst = next((c for c in cols if re.search(r"instit|empresa|fonte", str(c), re.I)), None)

        if col_data is None:
            if debug: print(f"  tab#{tab_idx}: sem coluna de data. cols={cols[:5]}...")
            continue

        cols_esq = [c for c in cols if _identificar_lado(c) == "esq"]
        cols_dir = [c for c in cols if _identificar_lado(c) == "dir"]

        if not cols_esq or not cols_dir:
            if debug:
                print(f"  tab#{tab_idx}: sem candidatos. data={col_data!r} esq={cols_esq} dir={cols_dir}")
                print(f"    cols totais: {cols}")
            continue

        if debug:
            print(f"  tab#{tab_idx}: data={col_data!r}  esq={cols_esq}  dir={cols_dir}")

        extraidos = 0
        for _, row in df.iterrows():
            data = _parse_data(row[col_data])
            if data is None: continue
            esq_vals = [v for v in (_parse_pct(row[c]) for c in cols_esq) if v is not None]
            dir_vals = [v for v in (_parse_pct(row[c]) for c in cols_dir) if v is not None]
            if not esq_vals or not dir_vals: continue
            esq, dir_ = sum(esq_vals), sum(dir_vals)
            registros.append({
                "data": data, "instituto": str(row[col_inst]) if col_inst else None,
                "esquerda": esq, "direita": dir_, "margem": esq - dir_,
                "fonte_tabela": tab_idx,
            })
            extraidos += 1
        if debug: print(f"    -> {extraidos} linhas extraidas")

    df_out = pd.DataFrame(registros)
    print(f"\nTotal: {len(df_out)} pesquisas extraidas de {len(tabelas)} tabelas")
    return df_out

def mediana(df: pd.DataFrame, dias: int = 30) -> dict:
    if df.empty:
        return {"esquerda": None, "direita": None, "margem": None, "n_pesquisas": 0, "fonte": "vazio"}
    corte = datetime.now() - timedelta(days=dias)
    recente = df[df["data"] >= corte]
    fonte = f"ultimos {dias}d"
    if recente.empty:
        recente = df.sort_values("data", ascending=False).head(5)
        fonte = "ultimas 5 (sem dado recente)"
    return {
        "esquerda":    round(float(recente["esquerda"].median()), 1),
        "direita":     round(float(recente["direita"].median()),  1),
        "margem":      round(float(recente["margem"].median()),   1),
        "n_pesquisas": len(recente),
        "data_min":    str(recente["data"].min().date()),
        "data_max":    str(recente["data"].max().date()),
        "fonte":       fonte,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="salvar mediana em JSON neste arquivo")
    ap.add_argument("--dias", type=int, default=30)
    args = ap.parse_args()

    try:
        df = baixar()
    except Exception as e:
        print(f"\nERRO ao baixar: {e}")
        if args.json:
            payload = {"erro": str(e), "esquerda": None, "direita": None,
                       "margem": None, "n_pesquisas": 0,
                       "atualizado_em": datetime.now().isoformat()}
            with open(args.json, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            print(f"JSON com erro salvo em {args.json}")
        sys.exit(1)

    if not df.empty:
        print("\nAmostra (10 mais recentes):")
        print(df.sort_values("data", ascending=False).head(10).to_string(index=False))

    med = mediana(df, dias=args.dias)
    print(f"\nMediana {args.dias}d:", med)

    if args.json:
        med["atualizado_em"] = datetime.now().isoformat()
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(med, f, ensure_ascii=False, indent=2)
        print(f"JSON salvo em {args.json}")

if __name__ == "__main__":
    main()
