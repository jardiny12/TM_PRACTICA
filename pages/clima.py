import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

import pandas as pd
from functools import lru_cache

from utils.funciones import (
    get_countries,
    get_weather,
    clima_line_plot,
    clima_world_map
)

dash.register_page(__name__, path="/clima", name="Clima Global")

# ============================================================
# DATA
# ============================================================
df_countries = get_countries()

# ============================================================
# CACHE DE CLIMA (ACELERA MUCHÍSIMO)
# ============================================================
@lru_cache(maxsize=200)
def cached_weather(lat, lon):
    """Cachea el clima de cada coordenada para evitar recargar datos."""
    return get_weather(lat, lon)

# ============================================================
# LAYOUT
# ============================================================
layout = html.Div(
    style={"padding": "20px", "fontFamily": "Caveat Brush"},
    children=[

        html.H1("Dashboard Climático Global", style={"textAlign": "center"}),

        html.Br(),

        dbc.Row([
            dbc.Col([
                html.Label("Selecciona un país:"),
                dcc.Dropdown(
                    id="dropdown-country",
                    options=[{"label": c, "value": c} for c in df_countries["country"]],
                    value="Peru",
                    clearable=False
                )
            ], width=4),

            dbc.Col([
                html.Br(),
                dbc.Button("Actualizar Clima", id="btn-update", color="primary")
            ], width=2)
        ]),

        html.Br(),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id="clima-mapa")
            ], width=12)
        ]),

        html.Br(),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id="clima-line")
            ], width=12)
        ]),
    ]
)

# ============================================================
# CALLBACKS OPTIMIZADOS
# ============================================================

# --- Mapa: SOLO se actualiza al presionar el botón ---
@dash.callback(
    Output("clima-mapa", "figure"),
    Input("btn-update", "n_clicks"),
    prevent_initial_call=True
)
def update_mapa(_):
    """Genera mapa global una sola vez cuando el usuario lo pide."""
    return clima_world_map(df_countries)


# --- Línea de tiempo: cambia al seleccionar país o presionar botón ---
@dash.callback(
    Output("clima-line", "figure"),
    Input("dropdown-country", "value"),
    Input("btn-update", "n_clicks")
)
def update_line(country, _):
    """Carga el clima cacheado y genera la línea de tiempo."""
    row = df_countries[df_countries["country"] == country].iloc[0]
    df_weather = cached_weather(row.lat, row.lon)
    return clima_line_plot(df_weather, country)
