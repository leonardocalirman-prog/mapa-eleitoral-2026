"""
Resultados eleitorais 2022 por UF — 1º turno presidencial.
Fonte: TSE (Tribunal Superior Eleitoral)
Margem = Lula% - Bolsonaro% em votos válidos (pp)
Votos válidos: aproximação a partir do total de votos válidos por UF (TSE).
"""

RESULTADOS_2022 = {
    "AC": {"nome": "Acre",                "uf": "AC", "margem": -1,  "lula": 43, "bolso": 44, "regiao": "N",  "votos_validos": 410_000},
    "AL": {"nome": "Alagoas",             "uf": "AL", "margem": 35,  "lula": 63, "bolso": 28, "regiao": "NE", "votos_validos": 1_640_000},
    "AM": {"nome": "Amazonas",            "uf": "AM", "margem": 20,  "lula": 54, "bolso": 34, "regiao": "N",  "votos_validos": 1_900_000},
    "AP": {"nome": "Amapá",               "uf": "AP", "margem":  3,  "lula": 46, "bolso": 43, "regiao": "N",  "votos_validos": 390_000},
    "BA": {"nome": "Bahia",               "uf": "BA", "margem": 56,  "lula": 73, "bolso": 17, "regiao": "NE", "votos_validos": 6_600_000},
    "CE": {"nome": "Ceará",               "uf": "CE", "margem": 51,  "lula": 72, "bolso": 21, "regiao": "NE", "votos_validos": 4_500_000},
    "DF": {"nome": "Distrito Federal",    "uf": "DF", "margem": -31, "lula": 28, "bolso": 59, "regiao": "CO", "votos_validos": 1_600_000},
    "ES": {"nome": "Espírito Santo",      "uf": "ES", "margem": -18, "lula": 36, "bolso": 54, "regiao": "SE", "votos_validos": 2_100_000},
    "GO": {"nome": "Goiás",               "uf": "GO", "margem": -28, "lula": 29, "bolso": 57, "regiao": "CO", "votos_validos": 3_500_000},
    "MA": {"nome": "Maranhão",            "uf": "MA", "margem": 48,  "lula": 70, "bolso": 22, "regiao": "NE", "votos_validos": 3_400_000},
    "MT": {"nome": "Mato Grosso",         "uf": "MT", "margem": -31, "lula": 28, "bolso": 59, "regiao": "CO", "votos_validos": 1_900_000},
    "MS": {"nome": "Mato Grosso do Sul",  "uf": "MS", "margem": -21, "lula": 33, "bolso": 54, "regiao": "CO", "votos_validos": 1_400_000},
    "MG": {"nome": "Minas Gerais",        "uf": "MG", "margem":  2,  "lula": 44, "bolso": 42, "regiao": "SE", "votos_validos": 10_000_000},
    "PA": {"nome": "Pará",                "uf": "PA", "margem": 29,  "lula": 59, "bolso": 30, "regiao": "N",  "votos_validos": 3_900_000},
    "PB": {"nome": "Paraíba",             "uf": "PB", "margem": 35,  "lula": 63, "bolso": 28, "regiao": "NE", "votos_validos": 2_200_000},
    "PR": {"nome": "Paraná",              "uf": "PR", "margem": -23, "lula": 32, "bolso": 55, "regiao": "S",  "votos_validos": 5_700_000},
    "PE": {"nome": "Pernambuco",          "uf": "PE", "margem": 43,  "lula": 67, "bolso": 24, "regiao": "NE", "votos_validos": 4_500_000},
    "PI": {"nome": "Piauí",               "uf": "PI", "margem": 54,  "lula": 73, "bolso": 19, "regiao": "NE", "votos_validos": 1_700_000},
    "RJ": {"nome": "Rio de Janeiro",      "uf": "RJ", "margem":  1,  "lula": 38, "bolso": 37, "regiao": "SE", "votos_validos": 8_000_000},
    "RN": {"nome": "Rio Grande do Norte", "uf": "RN", "margem": 38,  "lula": 65, "bolso": 27, "regiao": "NE", "votos_validos": 1_800_000},
    "RS": {"nome": "Rio Grande do Sul",   "uf": "RS", "margem": -16, "lula": 38, "bolso": 54, "regiao": "S",  "votos_validos": 5_900_000},
    "RO": {"nome": "Rondônia",            "uf": "RO", "margem": -31, "lula": 29, "bolso": 60, "regiao": "N",  "votos_validos": 800_000},
    "RR": {"nome": "Roraima",             "uf": "RR", "margem": -29, "lula": 30, "bolso": 59, "regiao": "N",  "votos_validos": 280_000},
    "SC": {"nome": "Santa Catarina",      "uf": "SC", "margem": -29, "lula": 30, "bolso": 59, "regiao": "S",  "votos_validos": 4_200_000},
    "SP": {"nome": "São Paulo",           "uf": "SP", "margem": -12, "lula": 36, "bolso": 48, "regiao": "SE", "votos_validos": 22_400_000},
    "SE": {"nome": "Sergipe",             "uf": "SE", "margem": 34,  "lula": 63, "bolso": 29, "regiao": "NE", "votos_validos": 1_100_000},
    "TO": {"nome": "Tocantins",           "uf": "TO", "margem": -3,  "lula": 43, "bolso": 46, "regiao": "N",  "votos_validos": 820_000},
}
