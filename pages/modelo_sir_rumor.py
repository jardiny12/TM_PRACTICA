import dash 
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint

dash.register_page(__name__, path="/modelo_sir_rumor", name="Modelo SIR - Rumor")

# ======================================================
# 🎨 PALETA CLARA (tema blanco)
# ======================================================
COLOR_ACCENT = "#6A3ECB"       # morado elegante
COLOR_TEXT = "#333333"         # gris oscuro
COLOR_CARD_BG = "#ffffff"      # tarjetas blancas
COLOR_BG = "#f5f6fa"           # fondo general claro
COLOR_GRID = "#dadada"         # líneas suaves

COLOR_S = "#1976D2"            # azul fuerte
COLOR_I = "#D32F2F"            # rojo fuerte
COLOR_R = "#388E3C"            # verde fuerte


# ======================================================
# Modelo del rumor
# ======================================================
def modelo_rumor(y, t, b, k):
    S, I, R = y
    dS_dt = -b * S * I
    dI_dt = (b * S * I) - (k * I * R)
    dR_dt = k * I * R
    return [dS_dt, dI_dt, dR_dt]


# Parámetros iniciales
S0, I0, R0 = 266.0, 1.0, 8.0
y0 = [S0, I0, R0]
N = S0 + I0 + R0
b = 0.004
t = np.linspace(0, 15, 150)

# Soluciones
k1, k2 = 0.01, 0.02
sol1 = odeint(modelo_rumor, y0, t, args=(b, k1))
sol2 = odeint(modelo_rumor, y0, t, args=(b, k2))
S1, I1, R1 = sol1.T
S2, I2, R2 = sol2.T


# ======================================================
# Función para crear gráficos (tema claro)
# ======================================================
def crear_grafico(tiempo, s, i, r, titulo):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=tiempo, y=s, mode="lines", name="Susceptibles (S)",
        line=dict(color=COLOR_S, width=2)
    ))
    fig.add_trace(go.Scatter(
        x=tiempo, y=i, mode="lines", name="Infectados (I)",
        line=dict(color=COLOR_I, width=3),
        fill="tozeroy", fillcolor="rgba(211,47,47,0.15)"
    ))
    fig.add_trace(go.Scatter(
        x=tiempo, y=r, mode="lines", name="Racionales (R)",
        line=dict(color=COLOR_R, width=2)
    ))

    fig.update_layout(
        title=dict(text=f"{titulo}", x=0.5, font=dict(color=COLOR_ACCENT, size=18)),
        paper_bgcolor=COLOR_CARD_BG,
        plot_bgcolor="#ffffff",
        font=dict(color=COLOR_TEXT),
        margin=dict(l=20, r=20, t=50, b=20),
        height=380,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    fig.update_xaxes(showgrid=True, gridcolor=COLOR_GRID, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor=COLOR_GRID)

    return fig


fig_k1 = crear_grafico(t, S1, I1, R1, "Evolución del Rumor — k = 0.01")
fig_k2 = crear_grafico(t, S2, I2, R2, "Evolución del Rumor — k = 0.02")


# ======================================================
# Textos
# ======================================================
texto_ecuaciones = r"""
### 📘 Modelo Matemático

\[
\frac{dS}{dt} = -bSI
\]

\[
\frac{dI}{dt} = bSI - kIR
\]

\[
\frac{dR}{dt} = kIR
\]

✔ El grupo racional **reduce la propagación del rumor**.
"""

texto_parametros = f"""
### 🔧 Parámetros Utilizados
- **S₀ = {int(S0)}**
- **I₀ = {int(I0)}**
- **R₀ = {int(R0)}**
- **b = {b}**
- **k₁ = 0.01**  
- **k₂ = 0.02**
"""


# ======================================================
# Layout final — Tema claro
# ======================================================
layout = html.Div([

    html.H1(
        "Modelo SIR Aplicado a Rumores",
        className="titulo-seccion",
        style={"textAlign": "center", "color": COLOR_ACCENT, "padding": "20px 0"}
    ),

    html.Div([
        # Gráficos
        html.Div([
            html.Div(dcc.Graph(figure=fig_k1), className="card"),
            html.Div(dcc.Graph(figure=fig_k2), className="card"),
        ], style={
            "flex": "2",
            "display": "flex",
            "flexDirection": "column",
            "gap": "20px"
        }),

        # Explicaciones
        html.Div([
            html.Div([dcc.Markdown(texto_ecuaciones, mathjax=True)], className="card"),
            html.Div([dcc.Markdown(texto_parametros, mathjax=True)], className="card"),
            html.Div([
                html.P(
                    "El parámetro k mide cuán efectivos son los racionales "
                    "para detener la propagación del rumor.",
                    style={"fontSize": "0.9em", "color": "#555"}
                )
            ], className="card")
        ], style={"flex": "1", "paddingLeft": "20px"})

    ], style={
        "display": "flex",
        "padding": "20px",
        "gap": "20px"
    })

], style={
    "backgroundColor": COLOR_BG,
    "minHeight": "100vh"
})
