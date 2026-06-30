"""
tracker/probabilidade.py - Probabilidade implicita de vitoria pelo agregado.

Modelo simples gaussiano: P(Lula vence) = Phi(gap_corrigido / sigma).

Sigma representa a incerteza total esperada sobre a margem real no dia da eleicao.
Como nao temos dados suficientes para estimar sigma empiricamente bem, usamos
3 cenarios fixos:
    - conservador: sigma = 8 pp  (incerteza alta, pesquisas pouco informativas)
    - base:        sigma = 5 pp  (incerteza media, default razoavel)
    - agressivo:   sigma = 3 pp  (incerteza baixa, pesquisas muito informativas)

IMPORTANTE: isso eh leitura INDICATIVA, nao previsao. Modelos gaussianos
simples nao capturam choques exogenos, mudancas de candidato, ou eventos
de cauda. Documentar bem.
"""

from __future__ import annotations
from typing import Dict
from math import erf, sqrt

CENARIOS_SIGMA = {
    "conservador": 8.0,
    "base": 5.0,
    "agressivo": 3.0,
}


def _phi(x: float) -> float:
    """CDF da normal padrao. Usa erf da stdlib para evitar dependencia de scipy."""
    return 0.5 * (1 + erf(x / sqrt(2)))


def prob_lula(gap_corrigido: float, sigma: float) -> float:
    """Phi(gap / sigma), em [0, 1]."""
    if sigma <= 0:
        return 1.0 if gap_corrigido > 0 else 0.0
    return _phi(gap_corrigido / sigma)


def calcular_probabilidades(gap_corrigido: float) -> Dict[str, float]:
    """Para cada cenario de sigma, retorna P(Lula) em pp (0-100)."""
    return {
        nome: round(prob_lula(gap_corrigido, sigma) * 100, 1)
        for nome, sigma in CENARIOS_SIGMA.items()
    }


if __name__ == "__main__":
    # smoke test
    for gap in [-5, -2, 0, 2, 5, 10]:
        probs = calcular_probabilidades(gap)
        print(f"gap {gap:+.1f}: {probs}")
