"""
tracker/ingest_2022.py - Scraper das pesquisas presidenciais 2022 (Wikipedia EN).

Mira a pagina 2022 e filtra a janela pre-1T (de 17 set a 1 out 2022).
Esses sao os dados que importam para calibrar o vies historico:
pesquisas finais "previam" tal coisa, o real foi outro.

Use:
    python -m tracker.ingest_2022
"""

from __future__ import annotations
from datetime import datetime
import pandas as pd
from tracker import ingest

URL_EN_2022 = (
    "https://en.wikipedia.org/wiki/"
    "Opinion_polling_for_the_2022_Brazilian_presidential_election"
)

OUTPUT_PATH = "data/pesquisas_2022_raw.csv"

# Janela pre-1T: 17 set a 1 out 2022 (vesperas da eleicao)
JANELA_INICIO = datetime(2022, 9, 17)
JANELA_FIM = datetime(2022, 10, 1)


def parsear_data_simples(s) -> datetime | None:
    """Reuso minimo do parser de clean.py, sem importar pra evitar ciclo."""
    if pd.isna(s):
        return None
    from tracker.clean import parse_data
    return parse_data(s)


def main() -> pd.DataFrame:
    html = ingest.baixar_html(URL_EN_2022)
    dfs = ingest.extrair_tabelas(html)
    print(f"  encontradas {len(dfs)} tabelas wikitable em 2022")

    # 2022 tem cenario "Bolsonaro x Lula direto" - geralmente em tabela separada
    idx = ingest.identificar_tabela_lula_flavio(dfs, debug=False)
    # Atencao: a heuristica busca "flavio" tambem; mas em 2022 eh Jair Bolsonaro.
    # Vamos buscar especificamente "Bolsonaro" ou "Lula vs Bolsonaro"
    if idx is None:
        idx = _identificar_lula_bolsonaro(dfs)
    if idx is None:
        print("ERRO: nao encontrou tabela Lula x Bolsonaro em 2022.")
        print("Primeiras colunas de cada tabela:")
        for i, df in enumerate(dfs[:15]):
            print(f"  tab#{i}: {list(df.columns)[:5]}")
        raise SystemExit(1)

    print(f"  usando tabela #{idx}")
    out = ingest.parsear_tabela(dfs[idx])
    out["candidato_b"] = "Bolsonaro (PL)"
    out["cenario"] = "Lula vs Bolsonaro direto"
    out["fonte_url"] = URL_EN_2022

    # filtra janela pre-1T
    out["_data_parsed"] = out["data_fim"].apply(parsear_data_simples)
    mask = out["_data_parsed"].between(JANELA_INICIO, JANELA_FIM)
    out_janela = out[mask].drop(columns=["_data_parsed"])

    out_janela.to_csv(OUTPUT_PATH, index=False)
    print(f"OK ingest_2022 -> {OUTPUT_PATH}  ({len(out_janela)} pesquisas pre-1T)")
    return out_janela


def _identificar_lula_bolsonaro(dfs):
    """Mais especifico para 2022: busca tabela com 'Lula' e 'Bolsonaro' (sem F.)."""
    for i, df in enumerate(dfs):
        cols = [str(c).lower() for c in df.columns]
        tem_lula = any("lula" in c for c in cols)
        tem_bolso = any(("bolsonaro" in c) and ("flavio" not in c) and ("flávio" not in c) for c in cols)
        if tem_lula and tem_bolso:
            return i
    return None


if __name__ == "__main__":
    main()
