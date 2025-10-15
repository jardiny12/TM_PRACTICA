import dash
from dash import dcc, html, Input, Output, State, callback
import numpy as np
import plotly.graph_objs as go

# Registrar nueva página
dash.register_page(__name__, path="/clase2", name="Clase 2")

# ------------------------
# Layout
layout = html.Div(
    className="contenedor-principal",
    children=[

        # Contenedor izquierdo
        html.Div(
            className="contenedor-izquierdo",
            children=[
                html.H2("Parámetros del modelo", className="titulo"),

                html.Div([
                    html.Label("Población inicial (P₀):"),
                    dcc.Input(
                        id="input-p0", type="number", value=200,
                        min=1, step=1, className="input-field"
                    ),
                ]),
                html.Div([
                    html.Label("Tasa de crecimiento (r):"),
                    dcc.Input(
                        id="input-r", type="number", value=0.04,
                        min=0, step=0.01, className="input-field"
                    ),
                ]),
                html.Div([
                    html.Label("Capacidad de carga (K):"),
                    dcc.Input(
                        id="input-k", type="number", value=1000,
                        min=1, step=1, className="input-field"
                    ),
                ]),
                html.Div([
                    html.Label("Tiempo máximo (t):"),
                    dcc.Input(
                        id="input-t", type="number", value=100,
                        min=1, step=1, className="input-field"
                    ),
                ]),
                html.Button(
                    "Generar gráfico",
                    id="btn-generar",
                    n_clicks=0,
                    className="btn-generar"
                ),
            ]
        ),

        # Contenedor derecho
        html.Div(
            className="contenedor-derecho",
            children=[
                html.H3("Gráfico de crecimiento poblacional",
                        style={"textAlign": "center", "color": "#d0021b"}),
                dcc.Graph(
                    id="grafica-poblacion",
                    style={"height": "420px", "width": "100%"}
                )
            ]
        )
    ]
)

# ------------------------
# Callback
@callback(
    Output("grafica-poblacion", "figure"),
    Input("btn-generar", "n_clicks"),
    State("input-p0", "value"),
    State("input-r", "value"),
    State("input-k", "value"),
    State("input-t", "value"),
    prevent_initial_call=False
)
def actualizar_grafico(n_clicks, P0, r, K, t_max):
    # Generar los valores del tiempo
    t = np.linspace(0, t_max, 20)

    # Modelo logístico
    P = (K * P0 * np.exp(r * t)) / (K + P0 * (np.exp(r * t) - 1))

    # Gráfica de la población
    trace_poblacion = go.Scatter(
        x=t,
        y=P,
        mode='lines+markers',
        name='Población P(t)',
        line=dict(color='black', width=2),
        marker=dict(
            size=7,
            color='blue',
            symbol='circle',
            line=dict(width=1, color='white')  # borde blanco para destacar los puntos
        ),
        hovertemplate="t: %{x:.2f}<br>P(t): %{y:.2f}<extra></extra>"
    )

    # Línea de capacidad de carga
    trace_capacidad = go.Scatter(
        x=[0, t_max],
        y=[K, K],
        mode='lines',
        name='Capacidad de carga (K)',
        line=dict(color='red', width=3, dash='dot'),
        hovertemplate="K: %{y:.2f}<extra></extra>"
    )

    fig = go.Figure(data=[trace_poblacion, trace_capacidad])
    fig.update_layout(
        title="Modelo logístico de crecimiento poblacional",
        title_x=0.5,
        title_y=0.93,
        xaxis_title="Tiempo (t)",
        yaxis_title="Población P(t)",
        font=dict(family="Caveat Brush", size=18, color="#75232c"),
        plot_bgcolor="rgba(255,255,255,1)",
        paper_bgcolor="rgba(255,255,255,1)",
        margin=dict(t=60, b=40, l=50, r=40)
    )

    return fig
