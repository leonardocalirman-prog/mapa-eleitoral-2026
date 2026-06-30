"""
tracker/clean.py - Normalizacao do CSV bruto da Wikipedia para schema canonico.

Recebe: data/pesquisas_*_raw.csv (output do ingest)
Produz: data/pesquisas_*.csv (limpo, com schema padrao, editavel manualmente)

Operacoes:
    1. Normaliza nomes de instituto via dicionario de aliases
    2. Parseia datas (varios formatos)
    3. Parseia percentuais (vira float)
    4. Calcula gap_lula_flavio = pct_lula - pct_flavio
    5. Gera poll_id estavel via hash(instituto + data_fim + cenario)
"""

from __future__ import annotations
import re
import hashlib
from datetime import datetime
from typing import Optional
import pandas as pd

# Schema canonico esperado no CSV de saida
COLUNAS_CANONICAS = [
    "poll_id",
    "instituto",
    "contratante",
    "data_inicio_campo",
    "data_fim_campo",
    "data_publicacao",
    "amostra",
    "margem_erro",
    "turno",
    "cenario",
    "candidato_a",
    "candidato_b",
    "pct_lula",
    "pct_flavio",
    "brancos_nulos",
    "indecisos",
    "gap_lula_flavio",
    "fonte_url",
    "observacoes",
]

# Aliases para padronizar nome do instituto. Match case-insensitive.
ALIASES_INSTITUTO = {
    "datafolha": "Datafolha",
    "data folha": "Datafolha",
    "atlas intel": "AtlasIntel",
    "atlasintel": "AtlasIntel",
    "atlas": "AtlasIntel",
    "real time big data": "Real Time Big Data",
    "real time bigdata": "Real Time Big Data",
    "rtbd": "Real Time Big Data",
    "poderdata/aya": "PoderData",
    "poderdata": "PoderData",
    "poder data": "PoderData",
    "quaest/genial": "Quaest",
    "quaest": "Quaest",
    "indexa": "Indexa",
    "vox brasil": "Vox Brasil",
    "vox": "Vox Brasil",
    "verita": "Verita",
    "verità": "Verita",
    "nexus": "Nexus",
    "nexus/btg": "Nexus",
    "vetor": "Vetor",
    "vetor/arrow": "Vetor",
    "apex/futura": "Apex/Futura",
    "apex": "Apex/Futura",
    "futura": "Apex/Futura",
    "meio/ideia": "Meio/Ideia",
    "ideia": "Meio/Ideia",
    "gerp": "Gerp",
    "ipec": "Ipec",
    "ibope": "Ipec",
    "parana pesquisas": "Paraná Pesquisas",
    "paraná pesquisas": "Paraná Pesquisas",
    "ipespe": "IPESPE",
}


def normalizar_instituto(raw: str) -> str:
    """Mapeia o nome bruto para o canonico. Se nao reconhecer, retorna como veio (Titulo)."""
    if not isinstance(raw, str) or not raw.strip():
        return ""
    key = raw.strip().lower()
    return ALIASES_INSTITUTO.get(key, raw.strip().title())


def parse_pct(s) -> Optional[float]:
    """Extrai numero (float) de uma celula com '%', '38,5', '38.5', '38,5 %', etc."""
    if pd.isna(s):
        return None
    s = str(s).replace("%", "").strip()
    m = re.search(r"(-?\d+[,.]?\d*)", s)
    if not m:
        return None
    return float(m.group(1).replace(",", "."))


def parse_data(s) -> Optional[datetime]:
    """
    Datas no formato Wikipedia: '12-15 fev 2026', '15 fev 2026', '15/02/2026', etc.
    Quando intervalo (10-15 fev 2026), pega a ultima data (fim do campo).
    """
    if pd.isna(s):
        return None
    s = str(s).strip().lower()
    s = re.split(r"\s*[-–—]\s*", s)[-1]
    MESES = {"jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6,
             "jul": 7, "ago": 8, "set": 9, "out": 10, "nov": 11, "dez": 12,
             "feb": 2, "apr": 4, "may": 5, "aug": 8, "sep": 9, "oct": 10, "dec": 12}
    m = re.search(r"(\d{1,2})\s*(?:de\s*)?([a-zç]{3,})\.?\s*(?:de\s*)?(\d{4})", s)
    if m:
        d, mes, y = m.group(1), m.group(2)[:3], m.group(3)
        if mes in MESES:
            try:
                return datetime(int(y), MESES[mes], int(d))
            except ValueError:
                return None
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


def gerar_poll_id(instituto: str, data_fim: Optional[datetime], cenario: str) -> str:
    """Hash curto e estavel para identificar uma pesquisa especifica."""
    data_str = data_fim.isoformat() if data_fim else "sem_data"
    raw = f"{instituto}|{data_str}|{cenario}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()[:10]


def processar(path_in: str, path_out: str) -> pd.DataFrame:
    """
    Le CSV bruto, aplica normalizacoes, salva CSV limpo.
    O CSV bruto eh assumido como tendo, no minimo: instituto, data_fim, pct_lula, pct_flavio.
    Colunas faltantes sao deixadas em branco no output.
    """
    df = pd.read_csv(path_in)
    out = pd.DataFrame(columns=COLUNAS_CANONICAS)

    # mapeamento simples coluna -> coluna canonica (pode ser estendido)
    out["instituto"] = df.get("instituto", "").apply(normalizar_instituto)
    out["data_fim_campo"] = df.get("data_fim", "").apply(parse_data)
    out["pct_lula"] = df.get("pct_lula", "").apply(parse_pct)
    out["pct_flavio"] = df.get("pct_flavio", "").apply(parse_pct)
    out["amostra"] = pd.to_numeric(df.get("amostra"), errors="coerce")
    out["cenario"] = df.get("cenario", "Lula vs Flávio direto")
    out["turno"] = df.get("turno", 1)
    out["candidato_a"] = "Lula (PT)"
    out["candidato_b"] = df.get("candidato_b", "F. Bolsonaro (PL)")
    out["fonte_url"] = df.get("fonte_url", "")

    # derivadas
    out["gap_lula_flavio"] = out["pct_lula"] - out["pct_flavio"]
    out["poll_id"] = out.apply(
        lambda r: gerar_poll_id(r["instituto"], r["data_fim_campo"], r["cenario"]),
        axis=1,
    )

    # filtra linhas invalidas (sem gap calculavel)
    out = out.dropna(subset=["gap_lula_flavio"]).reset_index(drop=True)

    out.to_csv(path_out, index=False)
    print(f"OK clean  {path_in} -> {path_out}  ({len(out)} pesquisas)")
    return out


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        processar(sys.argv[1], sys.argv[2])
    else:
        print("Uso: python -m tracker.clean <input.csv> <output.csv>")
