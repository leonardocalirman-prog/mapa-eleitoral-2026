"""
main.py — Ponto de entrada do Mapa Eleitoral 2026.

Uso:
    python main.py                        # swing padrão = -5pp
    python main.py --swing -8             # swing customizado
    python main.py --swing -5 --no-open   # não abre browser automaticamente
    python main.py --ajustes SP=-3,MG=2   # ajustes estaduais específicos
    python main.py --tabela               # imprime tabela no terminal
"""

import argparse
import webbrowser
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from src.modelo import calcular_margens, resumo
from src.mapa   import gerar_mapa, exportar


def parse_ajustes(s: str) -> dict:
    """Converte 'SP=-3,MG=2' em {'SP': -3.0, 'MG': 2.0}"""
    result = {}
    for item in s.split(","):
        uf, val = item.strip().split("=")
        result[uf.strip().upper()] = float(val)
    return result


def main():
    parser = argparse.ArgumentParser(description="Mapa Eleitoral 2026 — nowcasting por UF")
    parser.add_argument("--swing",   type=float, default=-5.0,
                        help="Swing nacional em pp (positivo=esq, negativo=dir). Padrão: -5")
    parser.add_argument("--ajustes", type=str,   default="",
                        help="Ajustes estaduais: ex. 'SP=-3,MG=2'")
    parser.add_argument("--output",  type=str,   default="output/mapa_eleitoral.html",
                        help="Caminho do HTML de saída")
    parser.add_argument("--no-open", action="store_true",
                        help="Não abre o browser automaticamente")
    parser.add_argument("--tabela",  action="store_true",
                        help="Imprime tabela de margens no terminal")
    args = parser.parse_args()

    ajustes = parse_ajustes(args.ajustes) if args.ajustes else {}

    print(f"\n── Mapa Eleitoral 2026 ──────────────────")
    print(f"  Swing nacional : {args.swing:+.1f} pp")
    if ajustes:
        print(f"  Ajustes locais : {ajustes}")
    print()

    df = calcular_margens(swing_nacional=args.swing, ajustes_estaduais=ajustes)

    if args.tabela:
        print(df[["uf","nome","margem_2022","margem_estimada","label"]].to_string(index=False))
        print()

    r = resumo(df)
    print(f"  Prováveis esquerda : {r['total_esq']:2d} UFs  "
          f"(sólido: {r['solido_esq']}, provável: {r['provavel_esq']})")
    print(f"  Competitivos       : {r['competitivo']:2d} UFs")
    print(f"  Prováveis direita  : {r['total_dir']:2d} UFs  "
          f"(provável: {r['provavel_dir']}, sólido: {r['solido_dir']})")
    print()

    fig = gerar_mapa(df, swing_nacional=args.swing)
    exportar(fig, path=args.output)

    if not args.no_open:
        webbrowser.open(f"file://{os.path.abspath(args.output)}")


if __name__ == "__main__":
    main()
