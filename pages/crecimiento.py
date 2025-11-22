import dash
from dash import html, dcc
import plotly.express as px
import numpy as np
import pandas as pd

dash.register_page(__name__, path="/crecimiento", name="Modelo de Crecimiento")

# --- Datos del modelo de crecimiento exponencial ---
P0 = 100
r = 0.03
t = np.linspace(0, 100, 50)
P = P0 * np.exp(r * t)
df = pd.DataFrame({"Tiempo (t)": t, "Población P(t)": P})

# --- Figura ---
fig = px.line(
    df, x="Tiempo (t)", y="Población P(t)",
    title="Crecimiento de la población (modelo exponencial)",
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
    
    className="contenedor-principal",
    children=[
        html.Div(
            className="contenedor-izquierdo",
            children=[
                html.H2("Crecimiento de la población y capacidad de carga"),
                dcc.Markdown(r"""
Para modelar el **crecimiento de la población** mediante una ecuación diferencial, primero tenemos que introducir algunas variables y términos relevantes.

La variable $t$ representará el **tiempo**. Las unidades de tiempo pueden ser horas, días, semanas, meses o incluso años, y deben especificarse en cada problema en particular.  
La variable $P$ representará la **población**. Como la población varía con el tiempo, se entiende que es una función del tiempo, es decir, usamos la notación $P(t)$.

Si $P(t)$ es una función diferenciable, entonces su derivada

$$\frac{dP}{dt}$$

representa la **tasa instantánea de cambio** de la población en función del tiempo.

---

En el tema de **Crecimiento y decaimiento exponencial**, se estudia cómo las poblaciones o sustancias radiactivas cambian con el tiempo según el modelo:

$$P(t) = P_0 e^{rt}$$  

donde:
- $P(t)$ es la población en el instante $t$  
- $P_0$ es la población inicial ($t=0$)  
- $r > 0$ es la **tasa de crecimiento**  

Por ejemplo, con $P_0 = 100$ y $r = 0.03$, obtenemos la función:

$$P(t) = 100 e^{0.03t}$$

La siguiente figura muestra la evolución de la población con el tiempo.
                """, mathjax=True)
            ]
        ),

        html.Div(
            className="contenedor-derecho",
            children=[
                html.H3("Modelo de Crecimiento Exponencial", style={"textAlign": "center", "color": "#d0021b"}),
                dcc.Graph(
                    id="grafico-crecimiento",
                    figure=fig,
                    style={"height": "480px"}
                )
            ]
        )
    ]
)
