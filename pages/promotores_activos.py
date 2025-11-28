import dash 
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint

dash.register_page(
    __name__, 
    path="/promotores_activos", 
    name="Evolución Promotores Activos"
)

# ======================================================
# 🎨 PALETA DE COLORES — MODO CLARO
# ======================================================
COLOR_SUCEPTIBLES = "#0077CC"
COLOR_INFECTADOS = "#581D1D"
COLOR_RECUPERADOS = "#009933"

COLOR_TITULO = "#4A148C"
COLOR_TEXTO_SECUNDARIO = "#333333"

COLOR_FONDO_GRAFICO = "#FFFFFF"
COLOR_FONDO_PAPEL = "#F8F9FA"
COLOR_GRID = "#DDDDDD"

# ======================================================
# MODELO SIR
# ======================================================
def modelo_sir(y, t, b, g):
    S, I, R = y
    dS_dt = -b * S * I
    dI_dt = b * S * I - g * I
    dR_dt = g * I
    return [dS_dt, dI_dt, dR_dt]

N = 10000.0
I0 = 10.0
S0 = N - I0
R0_init = 0.0
y0 = [S0, I0, R0_init]

t = np.linspace(0, 100, 100)

gamma_base = 0.25
R0_base = 2.5
beta_base = R0_base * gamma_base / N

sol1 = odeint(modelo_sir, y0, t, args=(beta_base, gamma_base))
I1 = sol1[:, 1]

beta_double = beta_base * 2
sol2 = odeint(modelo_sir, y0, t, args=(beta_double, gamma_base))
I2 = sol2[:, 1]

gamma_double = gamma_base * 2
sol3 = odeint(modelo_sir, y0, t, args=(beta_base, gamma_double))
I3 = sol3[:, 1]

# ======================================================
# GRÁFICO — VERSIÓN LIMPIA MODO CLARO
# ======================================================
def crear_grafico_infectados(tiempo, datos_i, titulo, y_max=None):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=tiempo, y=datos_i, mode="lines",
        name="I(t)",
        line=dict(color=COLOR_INFECTADOS, width=2.5)
    ))

    fig.update_layout(
        title=dict(text=f"<b>{titulo}</b>", x=0.5, font=dict(size=14, color=COLOR_TITULO)),
        xaxis_title="Días",
        yaxis_title="Personas",
        paper_bgcolor=COLOR_FONDO_PAPEL,
        plot_bgcolor=COLOR_FONDO_GRAFICO,
        font=dict(color="#333333", size=10),
        margin=dict(l=40, r=20, t=50, b=40),
        height=300
    )

    fig.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor=COLOR_GRID,
        zeroline=False,
        linecolor="#555",
        mirror=True
    )

    yaxis_cfg = dict(
        showgrid=True,
        gridwidth=1,
        gridcolor=COLOR_GRID,
        zeroline=False,
        linecolor="#555",
        mirror=True
    )

    if y_max:
        yaxis_cfg["range"] = [0, y_max]

    fig.update_yaxes(yaxis_cfg)

    return fig


fig_base = crear_grafico_infectados(t, I1, "I(t) - baseline (escenario)", y_max=2500)
fig_b_double = crear_grafico_infectados(t, I2, "I(t) - β duplicado", y_max=5000)
fig_k_double = crear_grafico_infectados(t, I3, "I(t) - γ duplicado", y_max=300)

# ======================================================
# LAYOUT MODO CLARO
# ======================================================
layout = html.Div([

    html.H1(
        "Dinámica de Infectados I(t): Análisis de Parámetros",
        style={
            "textAlign": "center",
            "color": COLOR_TITULO,
            "paddingBottom": "20px",
            "fontSize": "26px"
        }
    ),

    html.Div([
        html.Div([
            html.Div([dcc.Graph(figure=fig_base, config={"displayModeBar": False})],
                     style={"flex": "1", "minWidth": "300px", "padding": "10px"}),

            html.Div([dcc.Graph(figure=fig_b_double, config={"displayModeBar": False})],
                     style={"flex": "1", "minWidth": "300px", "padding": "10px"}),
        ], style={
            "display": "flex",
            "flexWrap": "wrap",
            "justifyContent": "center",
            "width": "100%"
        }),

        html.Div([
            html.Div([dcc.Graph(figure=fig_k_double, config={"displayModeBar": False})],
                     style={"width": "60%", "minWidth": "300px", "margin": "0 auto", "padding": "10px"})
        ], style={"width": "100%", "marginTop": "10px"}),
    ], style={
        "backgroundColor": "#FFFFFF",
        "borderRadius": "12px",
        "padding": "20px",
        "boxShadow": "0 2px 10px rgba(0,0,0,0.1)"
    }),

    # ======================================================
    # TEXTO EXPLICATIVO
    # ======================================================
    html.Div([
        html.H4("Interpretación de los Escenarios", style={"color": "#004488"}),

        dcc.Markdown(r"""
        Los gráficos muestran la evolución de los **infectados** \(I(t)\) bajo tres escenarios:

        1. **Baseline:** Comportamiento estándar con \(R_0 \approx 2.5\).  
        2. **β duplicado:** Aumenta la transmisión. El pico aparece **antes** y es **mucho mayor**.  
        3. **γ duplicado:** Incrementa la recuperación. La curva se **aplana fuertemente**.

        Estos resultados permiten evaluar cómo la propagación depende de los parámetros de transmisión y remoción.
        """, mathjax=True, style={"color": "#333"})
    ], style={
        "marginTop": "30px",
        "maxWidth": "800px",
        "marginLeft": "auto",
        "marginRight": "auto"
    })

], style={
    "backgroundColor": "#F5F6FA",
    "minHeight": "100vh",
    "padding": "20px",
    "fontFamily": "Inter, sans-serif"
})
