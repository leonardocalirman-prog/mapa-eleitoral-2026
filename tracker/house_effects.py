"""
tracker/house_effects.py - Calculo do vies (house effect) por instituto.

Pega as pesquisas finais de 2022 (Lula vs Bolsonaro direto, ultimos 30 dias
pre-1T) e compara o gap mediano com o resultado real (Lula 48.43 - Bolso 43.20
= +5.23 pp).

Se um instituto tem >= 3 pesquisas, calcula seu vies individual.
Caso contrario, usa um vies agregado como fallback.

Vies positivo = pesquisa superestimou Lula.
"""

from __future__ import annotations
import json
from typing import Dict
import pandas as pd

# Resultado real do 1T 2022 (Lula 48.43% vs Bolsonaro 43.20% = +5.23 pp)
MARGEM_REAL_2022 = 5.23

MIN_PESQUISAS_POR_INSTITUTO = 3


def calcular(df_2022: pd.DataFrame) -> Dict:
    """
    Recebe DataFrame com pesquisas 2022 (schema canonico).
    Retorna dict com vies por instituto e vies agregado.
    """
    # vies agregado (mediana geral)
    mediana_geral = float(df_2022["gap_lula_flavio"].median())
    bias_agregado = round(mediana_geral - MARGEM_REAL_2022, 2)

    # vies por instituto (so se tiver dados suficientes)
    bias_por_instituto = {}
    for inst, grupo in df_2022.groupby("instituto"):
        n = len(grupo)
        if n >= MIN_PESQUISAS_POR_INSTITUTO:
            mediana = float(grupo["gap_lula_flavio"].median())
            bias_por_instituto[inst] = {
                "bias_pp": round(mediana - MARGEM_REAL_2022, 2),
                "n_pesquisas": int(n),
                "mediana_gap": round(mediana, 2),
            }

    return {
        "margem_real_2022": MARGEM_REAL_2022,
        "mediana_geral_2022": round(mediana_geral, 2),
        "bias_agregado": bias_agregado,
        "por_instituto": bias_por_instituto,
        "min_pesquisas_por_instituto": MIN_PESQUISAS_POR_INSTITUTO,
    }


if __name__ == "__main__":
    df = pd.read_csv("data/pesquisas_2022_finais.csv")
    resultado = calcular(df)
    with open("data/house_effects.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    print(f"OK house_effects bias agregado: {resultado['bias_agregado']:+.2f} pp")
    print(f"   Institutos com vies individual: {len(resultado['por_instituto'])}")
