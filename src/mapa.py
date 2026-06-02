"""
mapa.py — Geração do mapa interativo com Plotly.
"""

import os
import json
import requests
import pandas as pd
import plotly.graph_objects as go

GEOJSON_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "br_states.geojson")
IBGE_API     = "https://servicodados.ibge.gov.br/api/v3/malhas/estados?formato=application/vnd.geo+json"
FALLBACK_URL = "https://raw.githubusercontent.com/giuliano-macedo/geodata-br-states/main/geojson/br_states.json"

IBGE_CODE_TO_UF = {
    "11":"RO","12":"AC","13":"AM","14":"RR","15":"PA","16":"AP","17":"TO",
    "21":"MA","22":"PI","23":"CE","24":"RN","25":"PB","26":"PE","27":"AL","28":"SE","29":"BA",
    "31":"MG","32":"ES","33":"RJ","35":"SP",
    "41":"PR","42":"SC","43":"RS",
    "50":"MS","51":"MT","52":"GO","53":"DF",
}


def _get_geojson() -> dict:
    if os.path.exists(GEOJSON_PATH):
        with open(GEOJSON_PATH) as f:
            return json.load(f)

    print("Baixando malha estadual do IBGE...")
    try:
        r = requests.get(IBGE_API, timeout=30)
        r.raise_for_status()
        data = r.json()
        for feature in data["features"]:
            code = feature["properties"].get("codarea", "")
            feature["id"] = IBGE_CODE_TO_UF.get(code, code)
    except Exception as e:
        print(f"  IBGE indisponivel ({e.__class__.__name__}). Tentando fallback...")
        r = requests.get(FALLBACK_URL, timeout=30)
        r.raise_for_status()
        data = r.json()
        for feature in data["features"]:
            props = feature.get("properties", {})
            sigla = (props.get("SIGLA") or props.get("sigla") or
                     props.get("UF")   or props.get("uf")    or
                     props.get("PK_sigla"))
            feature["id"] = sigla

    os.makedirs(os.path.dirname(GEOJSON_PATH), exist_ok=True)
    with open(GEOJSON_PATH, "w") as f:
        json.dump(data, f)
    print(f"  Salvo em {GEOJSON_PATH}")
    return data


def gerar_mapa(df: pd.DataFrame, titulo: str = "Temperatura Eleitoral 2026 - Brasil por UF", swing_nacional: float = 0.0) -> go.Figure:
    geojson = _get_geojson()

    COLOR_SCALE = [
        [0.00, "#993C1D"],
        [0.25, "#F0997B"],
        [0.50, "#B4B2A9"],
        [0.75, "#85B7EB"],
        [1.00, "#185FA5"],
    ]

    vmin, vmax = -60, 60
    df = df.copy()
    df["margem_norm"] = (df["margem_estimada"].clip(vmin, vmax) - vmin) / (vmax - vmin)

    hover_text = df.apply(lambda r: (
        f"<b>{r['nome']} ({r['uf']})</b><br>"
        f"Margem estimada: {r['margem_estimada']:+.1f} pp<br>"
        f"Base 2022: {r['margem_2022']:+d} pp<br>"
        f"Lula 2022: {r['lula_2022']}% | Bolso 2022: {r['bolso_2022']}%<br>"
        f"<i>{r['label']}</i>"
    ), axis=1)

    fig = go.Figure(go.Choropleth(
        geojson=geojson,
        locations=df["uf"],
        featureidkey="id",
        z=df["margem_norm"],
        colorscale=COLOR_SCALE,
        zmin=0, zmax=1,
        text=hover_text,
        hoverinfo="text",
        showscale=False,
        marker_line_color="white",
        marker_line_width=0.6,
    ))

    sign = "+" if swing_nacional >= 0 else ""
    subtitulo = f"Base: 1o turno 2022 | Swing nacional aplicado: {sign}{swing_nacional:.0f} pp"

    fig.update_layout(
        title=dict(text=f"<b>{titulo}</b><br><sup>{subtitulo}</sup>", x=0.5, xanchor="center"),
        geo=dict(fitbounds="locations", visible=False, bgcolor="rgba(0,0,0,0)"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=600,
        margin=dict(l=0, r=0, t=80, b=40),
        font=dict(family="Inter, sans-serif", size=12),
    )

    legenda = [
        ("Solido esquerda (>+20pp)",        "#185FA5"),
        ("Provavel esquerda (+5 a +20pp)",  "#85B7EB"),
        ("Competitivo (+/-5pp)",            "#B4B2A9"),
        ("Provavel direita (-5 a -20pp)",   "#F0997B"),
        ("Solido direita (<-20pp)",         "#993C1D"),
    ]
    for label, color in legenda:
        fig.add_trace(go.Scattergeo(
            lon=[None], lat=[None],
            mode="markers",
            marker=dict(size=10, color=color, symbol="square"),
            name=label,
            showlegend=True,
        ))

    fig.update_layout(legend=dict(
        title="Classificacao",
        orientation="v",
        x=1.01, y=0.5,
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#ddd",
        borderwidth=1,
    ))

    return fig


def exportar(fig: go.Figure, path: str = "output/mapa_eleitoral.html") -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.write_html(path, include_plotlyjs="cdn", full_html=True)
    print(f"Mapa exportado: {path}")
