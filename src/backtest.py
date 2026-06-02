"""
backtest.py - Valida o modelo aplicando 2018 -> 2022 com duas baselines.

Duas premissas testadas:

  (A) Swing NACIONAL uniforme:
      margem_uf(2022) = margem_uf(2018) + swing_nacional_observado

  (B) Swing REGIONAL observado:
      margem_uf(2022) = margem_uf(2018) + swing_regiao_observado[regiao_da_uf]

Comparando o erro residual (MAE) das duas baselines mede o quanto a
heterogeneidade regional adiciona na precisao do modelo.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.resultados_2018 import RESULTADOS_2018, MARGEM_NACIONAL_2018
from data.resultados_2022 import RESULTADOS_2022

MARGEM_NACIONAL_2022 = 5.2


def _margem_ponderada(ufs_data: dict, ufs_subset: list) -> float:
    """Margem ponderada por votos validos sobre um subconjunto de UFs."""
    peso = sum(RESULTADOS_2022[u]["votos_validos"] for u in ufs_subset)
    soma = sum(ufs_data[u]["margem"] * RESULTADOS_2022[u]["votos_validos"]
               for u in ufs_subset)
    return soma / peso if peso else 0.0


def calcular_swings_regionais() -> dict:
    """Para cada regiao, swing observado = margem_regional_2022 - margem_regional_2018."""
    regioes = sorted(set(d["regiao"] for d in RESULTADOS_2022.values()))
    out = {}
    for reg in regioes:
        ufs = [u for u, d in RESULTADOS_2022.items() if d["regiao"] == reg]
        m22 = _margem_ponderada(RESULTADOS_2022, ufs)
        m18 = _margem_ponderada(RESULTADOS_2018, ufs)
        out[reg] = {
            "margem_regional_2018": round(m18, 1),
            "margem_regional_2022": round(m22, 1),
            "swing_observado":      round(m22 - m18, 1),
            "ufs":                  ufs,
        }
    return out


def rodar() -> dict:
    """Backtest com as duas baselines."""
    swing_nacional = MARGEM_NACIONAL_2022 - MARGEM_NACIONAL_2018  # ~+21.9
    swings_reg     = calcular_swings_regionais()
    erros_uf       = []

    for uf in RESULTADOS_2022:
        if uf not in RESULTADOS_2018:
            continue
        m18 = RESULTADOS_2018[uf]["margem"]
        m22 = RESULTADOS_2022[uf]["margem"]
        reg = RESULTADOS_2022[uf]["regiao"]

        # Baseline (A): swing nacional uniforme
        m22_est_nac = m18 + swing_nacional
        erro_nac    = m22 - m22_est_nac

        # Baseline (B): swing regional observado
        m22_est_reg = m18 + swings_reg[reg]["swing_observado"]
        erro_reg    = m22 - m22_est_reg

        erros_uf.append({
            "uf": uf,
            "nome": RESULTADOS_2022[uf]["nome"],
            "regiao": reg,
            "margem_2018": m18,
            "margem_2022_real": m22,
            # Modelo A
            "estim_nacional":  round(m22_est_nac, 1),
            "erro_nacional":   round(erro_nac, 1),
            "erro_abs_nacional": round(abs(erro_nac), 1),
            # Modelo B
            "estim_regional":  round(m22_est_reg, 1),
            "erro_regional":   round(erro_reg, 1),
            "erro_abs_regional": round(abs(erro_reg), 1),
        })

    n = len(erros_uf)

    def _metricas(key_abs, key_sign):
        abs_v = [r[key_abs]  for r in erros_uf]
        sign  = [r[key_sign] for r in erros_uf]
        return {
            "mae_pp":          round(sum(abs_v) / n, 1),
            "rmse_pp":         round((sum(e**2 for e in abs_v) / n) ** 0.5, 1),
            "max_erro_abs":    max(abs_v),
            "ufs_positivos":   sum(1 for e in sign if e > 0),
            "ufs_negativos":   sum(1 for e in sign if e < 0),
        }

    return {
        "swing_nacional_observado": round(swing_nacional, 1),
        "margem_nacional_2018":     MARGEM_NACIONAL_2018,
        "margem_nacional_2022":     MARGEM_NACIONAL_2022,
        "n_ufs": n,
        "swings_regionais": swings_reg,
        "modelo_A_nacional": _metricas("erro_abs_nacional", "erro_nacional"),
        "modelo_B_regional": _metricas("erro_abs_regional", "erro_regional"),
        "erros_por_uf":     sorted(erros_uf, key=lambda r: -r["erro_abs_nacional"]),
    }


if __name__ == "__main__":
    r = rodar()
    print("==== BACKTEST 2018 -> 2022 ====\n")

    print("Swings regionais observados (ponderados por votos):")
    print(f"{'Reg':5} {'2018':>8} {'2022':>8} {'swing':>8}")
    for reg, d in r["swings_regionais"].items():
        print(f"{reg:5} {d['margem_regional_2018']:>+8} {d['margem_regional_2022']:>+8} {d['swing_observado']:>+8}")
    print()

    print(f"{'Modelo':25} {'MAE':>8} {'RMSE':>8} {'Max':>8}")
    A = r["modelo_A_nacional"]
    B = r["modelo_B_regional"]
    print(f"{'A) Swing nacional':25} {A['mae_pp']:>8} {A['rmse_pp']:>8} {A['max_erro_abs']:>8}")
    print(f"{'B) Swing regional':25} {B['mae_pp']:>8} {B['rmse_pp']:>8} {B['max_erro_abs']:>8}")
    melhora_mae  = round(A["mae_pp"]  - B["mae_pp"],  1)
    melhora_rmse = round(A["rmse_pp"] - B["rmse_pp"], 1)
    print(f"{'  ganho (A - B)':25} {melhora_mae:>8} {melhora_rmse:>8}")
    print()

    print("Top 10 UFs onde modelo A errou mais (e quanto B melhora):")
    print(f"{'UF':4} {'Reg':4} {'real':>6} {'A est':>7} {'A err':>7} {'B est':>7} {'B err':>7}")
    for u in r["erros_por_uf"][:10]:
        print(f"{u['uf']:4} {u['regiao']:4} {u['margem_2022_real']:>+6} "
              f"{u['estim_nacional']:>+7} {u['erro_nacional']:>+7} "
              f"{u['estim_regional']:>+7} {u['erro_regional']:>+7}")
