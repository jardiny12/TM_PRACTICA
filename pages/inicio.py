import dash
from dash import html, dcc
import plotly.express as px
import numpy as np
import pandas as pd

# Datos del modelo
P0 = 100
r = 0.03
t = np.linspace(0, 100, 50)
P = P0 * np.exp(r * t)
df = pd.DataFrame({"Tiempo (t)": t, "Población P(t)": P})

dash.register_page(__name__, path="/", name="Inicio")

# Figura
fig = px.line(
    df, x="Tiempo (t)", y="Población P(t)",
    title="Crecimiento de la población",
    markers=True, line_shape="spline"
)
fig.update_layout(
    title_x=0.5,
    title_font=dict(size=22, color="#d0021b", family="Caveat Brush"),
    xaxis_title="Tiempo (t)",
    yaxis_title="Población P(t)",
    plot_bgcolor="rgba(250,250,250,1)",
    paper_bgcolor="rgba(255,255,255,1)",
    font=dict(size=16, family="Caveat Brush"),
    margin=dict(t=80, b=60, l=60, r=60)
)

layout = html.Div(
    style={
        "display": "flex",
        "gap": "30px",
        "padding": "20px",
        "backgroundColor": "rgba(255,255,255,0.8)",
        "borderRadius": "12px",
        "boxShadow": "0 3px 8px rgba(0,0,0,0.2)",
        "marginTop": "20px"
    },
    children=[
        html.Div(style={"flex": "1", "textAlign": "justify"}, children=[
            html.H2("Crecimiento de la población y capacidad de carga"),
            dcc.Markdown(r"""
Para modelar el crecimiento de la población mediante una ecuación diferencial, primero introducimos variables relevantes.  
Sea $t$ el **tiempo** y $P(t)$ la **población** en función del tiempo.

Si $P(t)$ es diferenciable, entonces:

$$\frac{dP}{dt}$$

representa la **tasa instantánea de cambio** de la población.

Un ejemplo clásico es el **modelo de crecimiento exponencial**:

$$P(t) = P_0 e^{rt}$$  

donde:  
- $P_0 = 100$ es la población inicial  
- $r = 0.03$ es la tasa de crecimiento  
---
            """, mathjax=True)
        ]),

        html.Div(style={"flex": "1"}, children=[
            html.H2("Gráfica", style={"textAlign": "center", "color": "#d0021b"}),
            dcc.Graph(
                id="grafico-crecimiento",
                figure=fig,
                style={"height": "450px"}
            )
        ])
    ]
)
