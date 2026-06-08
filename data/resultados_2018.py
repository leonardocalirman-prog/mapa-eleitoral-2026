"""
Resultados eleitorais 2018 por UF - 1o turno presidencial.
Fonte: TSE / Wikipedia EN
Data: 7 de outubro de 2018, 100% das secoes totalizadas.
 
LEITURA "ESQUERDA AMPLA": somamos Haddad (PT) + Ciro Gomes (PDT) como bloco
de esquerda para 2018, ja que em 2022 esses eleitores convergiram para Lula.
Sem essa correcao, o swing 2018->2022 seria inflado pela fragmentacao da
esquerda em 2018.
 
Convencao: margem = (Haddad + Ciro)% - Bolsonaro%   (positivo = esquerda).
Nacional 1T 2018: Bolso 46.03 | Haddad 29.28 | Ciro 12.47 | Esq ampla 41.75
                  Margem (esq ampla - Bolso) = -4.28 pp
"""
 
RESULTADOS_2018 = {
    "AC": {"nome": "Acre",                "haddad": 18.53, "ciro":  5.17, "bolso": 62.24, "margem": -38.54},
    "AL": {"nome": "Alagoas",             "haddad": 44.75, "ciro": 10.12, "bolso": 34.40, "margem":  20.47},
    "AM": {"nome": "Amazonas",            "haddad": 40.30, "ciro":  7.50, "bolso": 43.48, "margem":   4.32},
    "AP": {"nome": "Amapa",               "haddad": 32.77, "ciro": 12.34, "bolso": 40.74, "margem":   4.37},
    "BA": {"nome": "Bahia",               "haddad": 60.28, "ciro":  9.41, "bolso": 23.41, "margem":  46.28},
    "CE": {"nome": "Ceara",               "haddad": 33.12, "ciro": 40.95, "bolso": 21.74, "margem":  52.33},
    "DF": {"nome": "Distrito Federal",    "haddad": 11.87, "ciro": 16.60, "bolso": 58.37, "margem": -29.90},
    "ES": {"nome": "Espirito Santo",      "haddad": 24.20, "ciro":  9.54, "bolso": 54.76, "margem": -21.02},
    "GO": {"nome": "Goias",               "haddad": 21.86, "ciro":  8.60, "bolso": 57.24, "margem": -26.78},
    "MA": {"nome": "Maranhao",            "haddad": 61.26, "ciro":  8.39, "bolso": 24.28, "margem":  45.37},
    "MT": {"nome": "Mato Grosso",         "haddad": 24.76, "ciro":  5.59, "bolso": 60.04, "margem": -29.69},
    "MS": {"nome": "Mato Grosso do Sul",  "haddad": 23.87, "ciro":  8.04, "bolso": 55.06, "margem": -23.15},
    "MG": {"nome": "Minas Gerais",        "haddad": 27.65, "ciro": 11.64, "bolso": 48.31, "margem":  -9.02},
    "PA": {"nome": "Para",                "haddad": 41.39, "ciro": 10.03, "bolso": 36.19, "margem":  15.23},
    "PB": {"nome": "Paraiba",             "haddad": 45.46, "ciro": 16.75, "bolso": 31.30, "margem":  30.91},
    "PR": {"nome": "Parana",              "haddad": 19.70, "ciro":  8.31, "bolso": 56.89, "margem": -28.88},
    "PE": {"nome": "Pernambuco",          "haddad": 48.87, "ciro": 13.56, "bolso": 30.57, "margem":  31.86},
    "PI": {"nome": "Piaui",               "haddad": 63.40, "ciro": 11.42, "bolso": 18.76, "margem":  56.06},
    "RJ": {"nome": "Rio de Janeiro",      "haddad": 14.69, "ciro": 15.22, "bolso": 59.79, "margem": -29.88},
    "RN": {"nome": "Rio Grande do Norte", "haddad": 41.19, "ciro": 22.31, "bolso": 30.21, "margem":  33.29},
    "RS": {"nome": "Rio Grande do Sul",   "haddad": 22.81, "ciro": 11.37, "bolso": 52.63, "margem": -18.45},
    "RO": {"nome": "Rondonia",            "haddad": 20.36, "ciro":  6.03, "bolso": 62.24, "margem": -35.85},
    "RR": {"nome": "Roraima",             "haddad": 17.85, "ciro":  5.36, "bolso": 62.97, "margem": -39.76},
    "SC": {"nome": "Santa Catarina",      "haddad": 15.13, "ciro":  6.68, "bolso": 65.82, "margem": -44.01},
    "SP": {"nome": "Sao Paulo",           "haddad": 16.42, "ciro": 11.35, "bolso": 53.00, "margem": -25.23},
    "SE": {"nome": "Sergipe",             "haddad": 27.21, "ciro": 13.02, "bolso": 50.09, "margem":  -9.86},
    "TO": {"nome": "Tocantins",           "haddad": 41.12, "ciro":  7.17, "bolso": 44.64, "margem":   3.65},
}
 
# Esquerda ampla nacional 2018 = Haddad 29.28% + Ciro 12.47% = 41.75%
# Bolsonaro nacional 2018 = 46.03%
MARGEM_NACIONAL_2018 = -4.28
