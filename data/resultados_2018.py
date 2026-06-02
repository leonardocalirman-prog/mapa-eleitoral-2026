"""
Resultados eleitorais 2018 por UF - 1o turno presidencial.
Fonte: TSE (1o turno, 07/10/2018)
Margem = Haddad% - Bolsonaro% em votos validos (pp)
Convencao: positivo = esquerda (PT/Haddad), negativo = direita (Bolsonaro)

Numeros sao aproximacoes (arredondamento para pp inteiro) - revisar com dados oficiais
do repositorio de dados abertos do TSE quando refinar o modelo.
"""

RESULTADOS_2018 = {
    "AC": {"nome": "Acre",                "haddad": 18, "bolso": 67, "margem": -49},
    "AL": {"nome": "Alagoas",             "haddad": 38, "bolso": 41, "margem":  -3},
    "AM": {"nome": "Amazonas",            "haddad": 28, "bolso": 51, "margem": -23},
    "AP": {"nome": "Amapa",               "haddad": 23, "bolso": 60, "margem": -37},
    "BA": {"nome": "Bahia",               "haddad": 51, "bolso": 30, "margem":  21},
    "CE": {"nome": "Ceara",               "haddad": 51, "bolso": 33, "margem":  18},
    "DF": {"nome": "Distrito Federal",    "haddad": 16, "bolso": 56, "margem": -40},
    "ES": {"nome": "Espirito Santo",      "haddad": 14, "bolso": 64, "margem": -50},
    "GO": {"nome": "Goias",               "haddad": 18, "bolso": 56, "margem": -38},
    "MA": {"nome": "Maranhao",            "haddad": 53, "bolso": 26, "margem":  27},
    "MT": {"nome": "Mato Grosso",         "haddad": 17, "bolso": 60, "margem": -43},
    "MS": {"nome": "Mato Grosso do Sul",  "haddad": 20, "bolso": 51, "margem": -31},
    "MG": {"nome": "Minas Gerais",        "haddad": 23, "bolso": 48, "margem": -25},
    "PA": {"nome": "Para",                "haddad": 36, "bolso": 41, "margem":  -5},
    "PB": {"nome": "Paraiba",             "haddad": 46, "bolso": 36, "margem":  10},
    "PR": {"nome": "Parana",              "haddad": 19, "bolso": 56, "margem": -37},
    "PE": {"nome": "Pernambuco",          "haddad": 53, "bolso": 32, "margem":  21},
    "PI": {"nome": "Piaui",               "haddad": 53, "bolso": 33, "margem":  20},
    "RJ": {"nome": "Rio de Janeiro",      "haddad": 20, "bolso": 59, "margem": -39},
    "RN": {"nome": "Rio Grande do Norte", "haddad": 47, "bolso": 36, "margem":  11},
    "RS": {"nome": "Rio Grande do Sul",   "haddad": 21, "bolso": 51, "margem": -30},
    "RO": {"nome": "Rondonia",            "haddad": 17, "bolso": 66, "margem": -49},
    "RR": {"nome": "Roraima",             "haddad": 19, "bolso": 56, "margem": -37},
    "SC": {"nome": "Santa Catarina",      "haddad": 16, "bolso": 65, "margem": -49},
    "SP": {"nome": "Sao Paulo",           "haddad": 21, "bolso": 53, "margem": -32},
    "SE": {"nome": "Sergipe",             "haddad": 47, "bolso": 36, "margem":  11},
    "TO": {"nome": "Tocantins",           "haddad": 32, "bolso": 44, "margem": -12},
}

# Margem nacional 2018 (1o turno): Haddad 29.3% - Bolso 46.0% = -16.7 pp
MARGEM_NACIONAL_2018 = -16.7
