"""
Resultados eleitorais 2022 por UF - 1o turno presidencial.
Fonte: TSE (Tribunal Superior Eleitoral) / Wikipedia EN
Data: 2 de outubro de 2022, 100% das secoes totalizadas.

Percentuais sobre votos validos (1o turno).
Margem = Lula% - Bolsonaro%
Votos validos: total de votos validos no estado (1o turno).
"""

RESULTADOS_2022 = {
    "AC": {"nome": "Acre",                "uf": "AC", "margem": -33.24, "lula": 29.26, "bolso": 62.50, "regiao": "N",  "votos_validos":    441_000},
    "AL": {"nome": "Alagoas",             "uf": "AL", "margem":  20.45, "lula": 56.50, "bolso": 36.05, "regiao": "NE", "votos_validos":  1_724_000},
    "AM": {"nome": "Amazonas",            "uf": "AM", "margem":   6.78, "lula": 49.58, "bolso": 42.80, "regiao": "N",  "votos_validos":  2_056_000},
    "AP": {"nome": "Amapa",               "uf": "AP", "margem":   2.26, "lula": 45.67, "bolso": 43.41, "regiao": "N",  "votos_validos":    432_000},
    "BA": {"nome": "Bahia",               "uf": "BA", "margem":  45.42, "lula": 69.73, "bolso": 24.31, "regiao": "NE", "votos_validos":  8_422_000},
    "CE": {"nome": "Ceara",               "uf": "CE", "margem":  40.53, "lula": 65.91, "bolso": 25.38, "regiao": "NE", "votos_validos":  5_429_000},
    "DF": {"nome": "Distrito Federal",    "uf": "DF", "margem": -14.80, "lula": 36.85, "bolso": 51.65, "regiao": "CO", "votos_validos":  1_763_000},
    "ES": {"nome": "Espirito Santo",      "uf": "ES", "margem": -11.83, "lula": 40.40, "bolso": 52.23, "regiao": "SE", "votos_validos":  2_221_000},
    "GO": {"nome": "Goias",               "uf": "GO", "margem": -12.65, "lula": 39.51, "bolso": 52.16, "regiao": "CO", "votos_validos":  3_682_000},
    "MA": {"nome": "Maranhao",            "uf": "MA", "margem":  42.82, "lula": 68.84, "bolso": 26.02, "regiao": "NE", "votos_validos":  3_782_000},
    "MT": {"nome": "Mato Grosso",         "uf": "MT", "margem": -25.45, "lula": 34.39, "bolso": 59.84, "regiao": "CO", "votos_validos":  1_843_000},
    "MS": {"nome": "Mato Grosso do Sul",  "uf": "MS", "margem": -13.66, "lula": 39.04, "bolso": 52.70, "regiao": "CO", "votos_validos":  1_507_000},
    "MG": {"nome": "Minas Gerais",        "uf": "MG", "margem":   4.69, "lula": 48.29, "bolso": 43.60, "regiao": "SE", "votos_validos": 12_016_000},
    "PA": {"nome": "Para",                "uf": "PA", "margem":  11.95, "lula": 52.22, "bolso": 40.27, "regiao": "N",  "votos_validos":  4_680_000},
    "PB": {"nome": "Paraiba",             "uf": "PB", "margem":  34.59, "lula": 64.21, "bolso": 29.62, "regiao": "NE", "votos_validos":  2_421_000},
    "PR": {"nome": "Parana",              "uf": "PR", "margem": -19.27, "lula": 35.99, "bolso": 55.26, "regiao": "S",  "votos_validos":  6_567_000},
    "PE": {"nome": "Pernambuco",          "uf": "PE", "margem":  35.36, "lula": 65.27, "bolso": 29.91, "regiao": "NE", "votos_validos":  5_452_000},
    "PI": {"nome": "Piaui",               "uf": "PI", "margem":  54.35, "lula": 74.25, "bolso": 19.90, "regiao": "NE", "votos_validos":  2_044_000},
    "RJ": {"nome": "Rio de Janeiro",      "uf": "RJ", "margem": -10.41, "lula": 40.68, "bolso": 51.09, "regiao": "SE", "votos_validos":  9_458_000},
    "RN": {"nome": "Rio Grande do Norte", "uf": "RN", "margem":  31.96, "lula": 62.98, "bolso": 31.02, "regiao": "NE", "votos_validos":  2_007_000},
    "RS": {"nome": "Rio Grande do Sul",   "uf": "RS", "margem":  -6.61, "lula": 42.28, "bolso": 48.89, "regiao": "S",  "votos_validos":  6_638_000},
    "RO": {"nome": "Rondonia",            "uf": "RO", "margem": -35.38, "lula": 28.98, "bolso": 64.36, "regiao": "N",  "votos_validos":    903_000},
    "RR": {"nome": "Roraima",             "uf": "RR", "margem": -46.52, "lula": 23.05, "bolso": 69.57, "regiao": "N",  "votos_validos":    298_000},
    "SC": {"nome": "Santa Catarina",      "uf": "SC", "margem": -32.67, "lula": 29.54, "bolso": 62.21, "regiao": "S",  "votos_validos":  4_331_000},
    "SP": {"nome": "Sao Paulo",           "uf": "SP", "margem":  -6.82, "lula": 40.89, "bolso": 47.71, "regiao": "SE", "votos_validos": 25_654_000},
    "SE": {"nome": "Sergipe",             "uf": "SE", "margem":  34.66, "lula": 63.82, "bolso": 29.16, "regiao": "NE", "votos_validos":  1_299_000},
    "TO": {"nome": "Tocantins",           "uf": "TO", "margem":   6.40, "lula": 50.40, "bolso": 44.00, "regiao": "N",  "votos_validos":    862_000},
}
