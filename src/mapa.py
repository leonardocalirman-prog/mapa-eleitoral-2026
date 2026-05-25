"""Geração do mapa interativo com Plotly."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
GEOJSON_PATH = ROOT / "data" / "br_states.geojson"

# Convenção visual brasileira:
# esquerda em vermelho, direita em azul.
COLOR_MAP = {
    "Sólido esquerda": "#991B1B",
    "Provável esquerda": "#F87171",
    "Competitivo": "#B8B8B8",
    "Provável direita": "#93C5FD",
    "Sólido direita": "#1D4ED8",
}

CATEGORY_ORDER = [
    "Sólido esquerda",
    "Provável esquerda",
    "Competitivo",
    "Provável direita",
    "Sólido direita",
]


def carregar_geojson(path: str | Path = GEOJSON_PATH) -> dict:
    """Carrega a malha estadual em GeoJSON."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"GeoJSON não encontrado: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def gerar_mapa(df: pd.DataFrame, swing_nacional: float = -5.0):
    """Cria o choropleth interativo por UF."""
    geojson = carregar_geojson()

    fig = px.choropleth(
        df,
        geojson=geojson,
        locations="uf",
        featureidkey="properties.sigla",
        color="label",
        color_discrete_map=COLOR_MAP,
        category_orders={"label": CATEGORY_ORDER},
        custom_data=[
            "nome",
            "uf",
            "lula_pct_fmt",
            "bolsonaro_pct_fmt",
            "margem_2022_fmt",
            "swing_nacional",
            "ajuste_estadual",
            "margem_estimada_fmt",
            "label",
        ],
        title=f"Mapa Eleitoral 2026: nowcasting por UF | swing nacional {swing_nacional:+.1f} pp",
    )

    fig.update_traces(
        marker_line_width=0.7,
        marker_line_color="white",
        hovertemplate=(
            "<b>%{customdata[0]} (%{customdata[1]})</b><br>"
            "Lula 2022: %{customdata[2]}<br>"
            "Bolsonaro 2022: %{customdata[3]}<br>"
            "Margem 2022: %{customdata[4]}<br>"
            "Swing nacional: %{customdata[5]:+.1f} pp<br>"
            "Ajuste estadual: %{customdata[6]:+.1f} pp<br>"
            "<b>Margem estimada: %{customdata[7]}</b><br>"
            "Classificação: %{customdata[8]}"
            "<extra></extra>"
        ),
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
    )

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=90, b=35),
        height=760,
        legend_title_text="Classificação",
        title=dict(
            x=0.02,
            xanchor="left",
            font=dict(size=21),
        ),
        annotations=[
            dict(
                text=(
                    "Exercício analítico de portfólio. Não é previsão eleitoral. "
                    "Margem = Lula - Bolsonaro, em pontos percentuais."
                ),
                x=0,
                y=-0.04,
                xref="paper",
                yref="paper",
                showarrow=False,
                align="left",
                font=dict(size=12, color="#555"),
            )
        ],
    )

    return fig


def exportar(fig, path: str = "output/mapa_eleitoral.html") -> Path:
    """Exporta o mapa para HTML."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(output_path, include_plotlyjs="cdn", full_html=True)
    print(f"Mapa exportado: {output_path}")
    return output_path
