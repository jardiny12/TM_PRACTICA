import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

# Registrar nueva página
dash.register_page(__name__, path="/tarea", name="Clase 2")

# --- Modelo logístico ---
r = 0.2   # tasa de crecimiento
k = 150   # capacidad de carga
P0 = 10   # población inicial

t = np.linspace(0, 60, 200)
P = k / (1 + ((k - P0) / P0) * np.exp(-r * t))

# --- Figura ---
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=t, y=P, mode='lines', name='Ecuación Logística',
    line=dict(color='blue', width=2)
))

# Línea de capacidad de carga
fig.add_trace(go.Scatter(
    x=t, y=[k]*len(t), mode='lines', name='Capacidad de carga',
    line=dict(color='red', width=3, dash='dash')
))

# Configuración general
fig.update_layout(
    title="Campo de vectores de dP/dt = rP(1 - P/k)",
    title_x=0.5,
    xaxis_title="Tiempo (t)",
    yaxis_title="Población (P)",
    font=dict(family="Caveat Brush", size=18),
    plot_bgcolor="rgba(255,255,255,1)",
    paper_bgcolor="rgba(255,255,255,1)",
    legend=dict(x=0.02, y=0.98)
)

# --- Layout ---
layout = html.Div(
    style={
        "display": "flex",
        "gap": "30px",
        "padding": "20px",
        "backgroundColor": "rgba(255,255,255,0.9)",
        "borderRadius": "12px",
        "boxShadow": "0 3px 8px rgba(0,0,0,0.2)",
        "marginTop": "20px"
    },
    children=[

        # Bloque de teoría
        html.Div(
            style={"flex": "1", "textAlign": "justify"},
            children=[
                html.H2("Modelo Logístico de Crecimiento Poblacional"),
                dcc.Markdown(r"""
El **modelo logístico** describe el crecimiento de una población
cuando existe una **capacidad de carga** $k$, que limita el número máximo de individuos
que el ambiente puede sostener.

La ecuación diferencial que rige el modelo es:

$$\frac{dP}{dt} = rP\left(1 - \frac{P}{k}\right)$$

donde:  
- $r$ es la **tasa de crecimiento intrínseca**,  
- $k$ es la **capacidad de carga**,  
- $P(t)$ es la **población en el tiempo**.

A medida que $P(t)$ se aproxima a $k$, el crecimiento se **ralentiza**, tendiendo
a un valor estable.
                """, mathjax=True)
            ]
        ),

        # Gráfica
        html.Div(
            style={"flex": "1"},
            children=[
                html.H2("Gráfica", style={"textAlign": "center"}),
                dcc.Graph(
                    id="grafico-logistico",
                    figure=fig,
                    style={"height": "480px"}
                )
            ]
        )
    ]
)
