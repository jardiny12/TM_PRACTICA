# pages/covid.py
import dash
from dash import html, dcc, Input, Output, State
import pandas as pd
import requests

from utils.funciones import (
    obtener_datos_covid,
    obtener_lista_paises,
    figura_lineal_covid,
    mapa_covid_global
)

dash.register_page(__name__, path="/covid", name="COVID 19")

# precarga de lista de países (si falla, lista vacía)
try:
    PAISES = obtener_lista_paises()
except Exception:
    PAISES = []

# LAYOUT (dos columnas: izquierda controles, derecha tarjetas+gráficos)
layout = html.Div(className="covid-contenedor", children=[

    # panel izquierdo: controles
    html.Div(className="covid-panel-izquierdo", children=[
        html.H2("Dashboard COVID-19", className="titulo-panel"),

        html.Label("Seleccione el país:", className="label"),
        dcc.Dropdown(
            id="pais-dropdown",
            options=[{"label": p, "value": p} for p in PAISES],
            value="Peru" if "Peru" in PAISES else (PAISES[0] if PAISES else None),
            className="dropdown",
            clearable=False
        ),

        html.Label("Días histórico (últimos N):", className="label"),
        dcc.Dropdown(
            id="dias-dropdown",
            options=[
                {"label": "Últimos 30 días", "value": 30},
                {"label": "Últimos 90 días", "value": 90},
                {"label": "Últimos 180 días", "value": 180},
                {"label": "Todo el histórico", "value": "all"},
            ],
            value="all",
            className="dropdown",
            clearable=False
        ),

        html.Button("Actualizar Datos", id="btn-actualizar", n_clicks=0, className="btn-actualizar"),
        html.Div(id="texto-actualizacion", className="texto-actualizacion")
    ]),

    # panel derecho: tarjetas + gráfico + mapa debajo
    html.Div(className="covid-panel-derecho", children=[

        # tarjetas
        html.Div(className="covid-estadisticas", children=[
            html.Div(className="card", children=[html.H4("Total casos"), html.H3(id="card-total-casos")]),
            html.Div(className="card", children=[html.H4("Casos nuevos"), html.H3(id="card-casos-nuevos")]),
            html.Div(className="card", children=[html.H4("Total muertes"), html.H3(id="card-total-muertes")]),
            html.Div(className="card", children=[html.H4("Recuperados"), html.H3(id="card-total-recuperados")]),
        ]),

        # gráfico lineal
        dcc.Graph(id="grafico-covid", style={"height": "430px", "width": "100%"}),

        # mapa global
        dcc.Graph(id="grafico-mapa", style={"height": "560px", "width": "100%", "marginTop": "18px"})
    ])
])


# CALLBACK: actualiza gráfico, mapa y tarjetas
@dash.callback(
    Output("grafico-covid", "figure"),
    Output("grafico-mapa", "figure"),
    Output("card-total-casos", "children"),
    Output("card-casos-nuevos", "children"),
    Output("card-total-muertes", "children"),
    Output("card-total-recuperados", "children"),
    Output("texto-actualizacion", "children"),
    Input("btn-actualizar", "n_clicks"),
    State("pais-dropdown", "value"),
    State("dias-dropdown", "value")
)
def actualizar_dashboard(n_clicks, pais, dias):
    # seguridad: si no hay país seleccionado
    if not pais:
        empty_fig = figura_lineal_covid(None, "")
        return empty_fig, mapa_covid_global(), "?", "?", "?", "?", "Selecciona un país."

    # obtener históricos
    df = obtener_datos_covid(pais)
    if df is None or df.empty:
        return figura_lineal_covid(None, pais), mapa_covid_global(), "?", "?", "?", "?", f"No hay datos para {pais}."

    # filtrar por días si corresponde
    if dias != "all":
        try:
            dias_n = int(dias)
            df = df.tail(dias_n).reset_index(drop=True)
        except Exception:
            pass

    # construir figuras
    fig_line = figura_lineal_covid(df, pais)
    fig_map = mapa_covid_global()

    # tarjetas
    total_casos = f"{int(df['casos'].iloc[-1]):,}"
    casos_nuevos = f"{int(df['nuevos'].iloc[-1]):,}"
    total_muertes = f"{int(df['muertes'].iloc[-1]):,}"
    recuperados = f"{int(df['recuperados'].iloc[-1]):,}" if "recuperados" in df.columns else "N/A"

    texto = f"Datos actualizados para {pais}."

    return fig_line, fig_map, total_casos, casos_nuevos, total_muertes, recuperados, texto
