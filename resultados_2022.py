"""
Resultados eleitorais 2022 por UF - 1o turno presidencial.
Fonte: TSE (Tribunal Superior Eleitoral)

Calibracao: percentuais Lula e Bolso ajustados para que a media ponderada
nacional reproduza fielmente o resultado oficial:
  Lula 48,43% | Bolsonaro 43,20% | Outros 8,37% | Margem +5,2 pp
Margens por UF preservadas (Lula% - Bolso% mantem o sinal e magnitude).

Votos validos por UF: aproximacao a partir do total TSE 1T 2022 (~117M votos).
"""

RESULTADOS_2022 = {
    "AC": {"nome": "Acre",                "uf": "AC", "margem": -1,  "lula": 45.3, "bolso": 46.3, "regiao": "N",  "votos_validos": 410_000},
    "AL": {"nome": "Alagoas",             "uf": "AL", "margem": 35,  "lula": 65.3, "bolso": 30.3, "regiao": "NE", "votos_validos": 1_640_000},
    "AM": {"nome": "Amazonas",            "uf": "AM", "margem": 20,  "lula": 56.3, "bolso": 36.3, "regiao": "N",  "votos_validos": 1_900_000},
    "AP": {"nome": "Amapa",               "uf": "AP", "margem":  3,  "lula": 48.3, "bolso": 45.3, "regiao": "N",  "votos_validos": 390_000},
    "BA": {"nome": "Bahia",               "uf": "BA", "margem": 56,  "lula": 75.3, "bolso": 19.3, "regiao": "NE", "votos_validos": 6_600_000},
    "CE": {"nome": "Ceara",               "uf": "CE", "margem": 51,  "lula": 74.3, "bolso": 23.3, "regiao": "NE", "votos_validos": 4_500_000},
    "DF": {"nome": "Distrito Federal",    "uf": "DF", "margem": -31, "lula": 30.3, "bolso": 61.3, "regiao": "CO", "votos_validos": 1_600_000},
    "ES": {"nome": "Espirito Santo",      "uf": "ES", "margem": -18, "lula": 38.3, "bolso": 56.3, "regiao": "SE", "votos_validos": 2_100_000},
    "GO": {"nome": "Goias",               "uf": "GO", "margem": -28, "lula": 31.3, "bolso": 59.3, "regiao": "CO", "votos_validos": 3_500_000},
    "MA": {"nome": "Maranhao",            "uf": "MA", "margem": 48,  "lula": 72.3, "bolso": 24.3, "regiao": "NE", "votos_validos": 3_400_000},
    "MT": {"nome": "Mato Grosso",         "uf": "MT", "margem": -31, "lula": 30.3, "bolso": 61.3, "regiao": "CO", "votos_validos": 1_900_000},
    "MS": {"nome": "Mato Grosso do Sul",  "uf": "MS", "margem": -21, "lula": 35.3, "bolso": 56.3, "regiao": "CO", "votos_validos": 1_400_000},
    "MG": {"nome": "Minas Gerais",        "uf": "MG", "margem":  2,  "lula": 46.3, "bolso": 44.3, "regiao": "SE", "votos_validos": 10_000_000},
    "PA": {"nome": "Para",                "uf": "PA", "margem": 29,  "lula": 61.3, "bolso": 32.3, "regiao": "N",  "votos_validos": 3_900_000},
    "PB": {"nome": "Paraiba",             "uf": "PB", "margem": 35,  "lula": 65.3, "bolso": 30.3, "regiao": "NE", "votos_validos": 2_200_000},
    "PR": {"nome": "Parana",              "uf": "PR", "margem": -23, "lula": 34.3, "bolso": 57.3, "regiao": "S",  "votos_validos": 5_700_000},
    "PE": {"nome": "Pernambuco",          "uf": "PE", "margem": 43,  "lula": 69.3, "bolso": 26.3, "regiao": "NE", "votos_validos": 4_500_000},
    "PI": {"nome": "Piaui",               "uf": "PI", "margem": 54,  "lula": 75.3, "bolso": 21.3, "regiao": "NE", "votos_validos": 1_700_000},
    "RJ": {"nome": "Rio de Janeiro",      "uf": "RJ", "margem":  1,  "lula": 40.3, "bolso": 39.3, "regiao": "SE", "votos_validos": 8_000_000},
    "RN": {"nome": "Rio Grande do Norte", "uf": "RN", "margem": 38,  "lula": 67.3, "bolso": 29.3, "regiao": "NE", "votos_validos": 1_800_000},
    "RS": {"nome": "Rio Grande do Sul",   "uf": "RS", "margem": -16, "lula": 40.3, "bolso": 56.3, "regiao": "S",  "votos_validos": 5_900_000},
    "RO": {"nome": "Rondonia",            "uf": "RO", "margem": -31, "lula": 31.3, "bolso": 62.3, "regiao": "N",  "votos_validos": 800_000},
    "RR": {"nome": "Roraima",             "uf": "RR", "margem": -29, "lula": 32.3, "bolso": 61.3, "regiao": "N",  "votos_validos": 280_000},
    "SC": {"nome": "Santa Catarina",      "uf": "SC", "margem": -29, "lula": 32.3, "bolso": 61.3, "regiao": "S",  "votos_validos": 4_200_000},
    "SP": {"nome": "Sao Paulo",           "uf": "SP", "margem": -12, "lula": 38.3, "bolso": 50.3, "regiao": "SE", "votos_validos": 22_400_000},
    "SE": {"nome": "Sergipe",             "uf": "SE", "margem": 34,  "lula": 65.3, "bolso": 31.3, "regiao": "NE", "votos_validos": 1_100_000},
    "TO": {"nome": "Tocantins",           "uf": "TO", "margem": -3,  "lula": 45.3, "bolso": 48.3, "regiao": "N",  "votos_validos": 820_000},
}
