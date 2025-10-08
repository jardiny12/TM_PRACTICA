import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path="/clase1", name="Clase 1")

df = pd.DataFrame({
    "Tiempo (min)": [0, 5, 10, 15, 20],
    "Temperatura (°C)": [200, 75, 65, 55, 48]
})

fig = px.line(
    df, x="Tiempo (min)", y="Temperatura (°C)",
    title="Curva de enfriamiento",
    markers=True, line_shape="spline"
)
fig.update_layout(
    title_x=0.5,
    title_font=dict(size=22, color="#d0021b", family="Caveat Brush"),
    font=dict(family="Caveat Brush", size=16),
    plot_bgcolor="rgba(250,250,250,1)",
    paper_bgcolor="rgba(255,255,255,1)"
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
            html.H2("Enfriamiento"),
            dcc.Markdown(r"""
Se pide el instante en que $T(t) = 65^\circ C$:

---

**Hipótesis:**  
- A los 10 minutos se coloca una tapa.  
- El coeficiente de enfriamiento se reduce a $0.6k$.  
- La temperatura inicial de esta etapa es $T(10)$.  
---
            """, mathjax=True)
        ]),

        html.Div(style={"flex": "1"}, children=[
            html.H2("Gráfica", style={"textAlign": "center", "color": "#d0021b"}),
            dcc.Graph(
                id="grafico-enfriamiento",
                figure=fig,
                style={"height": "450px"}
            )
        ])
    ]
)
