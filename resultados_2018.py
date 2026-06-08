"""
Resultados eleitorais 2018 por UF - 1o turno presidencial.
Fonte: TSE / G1 / Wikipedia EN
Data: 7 de outubro de 2018, 100% das secoes totalizadas.

Convencao: margem = Haddad% - Bolsonaro% (positivo = esquerda).
Nacional 1T 2018: Bolsonaro 46.03% | Haddad 29.28% | Margem -16.75 pp.
"""

RESULTADOS_2018 = {
    "AC": {"nome": "Acre",                "haddad": 18.53, "bolso": 62.24, "margem": -43.71},
    "AL": {"nome": "Alagoas",             "haddad": 44.75, "bolso": 34.40, "margem":  10.35},
    "AM": {"nome": "Amazonas",            "haddad": 40.30, "bolso": 43.48, "margem":  -3.18},
    "AP": {"nome": "Amapa",               "haddad": 32.77, "bolso": 40.74, "margem":  -7.97},
    "BA": {"nome": "Bahia",               "haddad": 60.28, "bolso": 23.41, "margem":  36.87},
    "CE": {"nome": "Ceara",               "haddad": 33.12, "bolso": 21.74, "margem":  11.38},
    "DF": {"nome": "Distrito Federal",    "haddad": 11.87, "bolso": 58.37, "margem": -46.50},
    "ES": {"nome": "Espirito Santo",      "haddad": 24.20, "bolso": 54.76, "margem": -30.56},
    "GO": {"nome": "Goias",               "haddad": 21.86, "bolso": 57.24, "margem": -35.38},
    "MA": {"nome": "Maranhao",            "haddad": 61.26, "bolso": 24.28, "margem":  36.98},
    "MT": {"nome": "Mato Grosso",         "haddad": 24.76, "bolso": 60.04, "margem": -35.28},
    "MS": {"nome": "Mato Grosso do Sul",  "haddad": 23.87, "bolso": 55.06, "margem": -31.19},
    "MG": {"nome": "Minas Gerais",        "haddad": 27.65, "bolso": 48.31, "margem": -20.66},
    "PA": {"nome": "Para",                "haddad": 41.39, "bolso": 36.19, "margem":   5.20},
    "PB": {"nome": "Paraiba",             "haddad": 45.46, "bolso": 31.30, "margem":  14.16},
    "PR": {"nome": "Parana",              "haddad": 19.70, "bolso": 56.89, "margem": -37.19},
    "PE": {"nome": "Pernambuco",          "haddad": 48.87, "bolso": 30.57, "margem":  18.30},
    "PI": {"nome": "Piaui",               "haddad": 63.40, "bolso": 18.76, "margem":  44.64},
    "RJ": {"nome": "Rio de Janeiro",      "haddad": 14.69, "bolso": 59.79, "margem": -45.10},
    "RN": {"nome": "Rio Grande do Norte", "haddad": 41.19, "bolso": 30.21, "margem":  10.98},
    "RS": {"nome": "Rio Grande do Sul",   "haddad": 22.81, "bolso": 52.63, "margem": -29.82},
    "RO": {"nome": "Rondonia",            "haddad": 20.36, "bolso": 62.24, "margem": -41.88},
    "RR": {"nome": "Roraima",             "haddad": 17.85, "bolso": 62.97, "margem": -45.12},
    "SC": {"nome": "Santa Catarina",      "haddad": 15.13, "bolso": 65.82, "margem": -50.69},
    "SP": {"nome": "Sao Paulo",           "haddad": 16.42, "bolso": 53.00, "margem": -36.58},
    "SE": {"nome": "Sergipe",             "haddad": 27.21, "bolso": 50.09, "margem": -22.88},
    "TO": {"nome": "Tocantins",           "haddad": 41.12, "bolso": 44.64, "margem":  -3.52},
}

MARGEM_NACIONAL_2018 = -16.75  # Haddad 29.28% - Bolsonaro 46.03%
