import dash 
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint

dash.register_page(__name__, path="/proyecto", name="Proyecto Modelo SIR")

# ============================
# 🎨 PALETA CLARA
# ============================
COLOR_SUCEPTIBLES = '#0077cc'
COLOR_INFECTADOS = '#d11a2a'
COLOR_RECUPERADOS = '#009944'

COLOR_TITULO = '#5a2a2a'
COLOR_TEXTO = '#333'

# ============================
# 📌 MODELO SIR
# ============================
def modelo_sir(y, t, b, g):
    S, I, R = y 
    if S < 0: S = 0
    if I < 0: I = 0
    dS_dt = -b*S*I
    dI_dt = b*S*I - g*I
    dR_dt = g*I
    return [dS_dt, dI_dt, dR_dt]

# ============================
# 📌 PARÁMETROS
# ============================
beta = 1.0 / 7138.0
gamma = 0.40

S0 = 7137.0
I0 = 1.0
R0 = 0.0
y0 = [S0, I0, R0]

t = np.linspace(0, 40, 400) 

solucion = odeint(modelo_sir, y0, t, args=(beta, gamma))
S, I, R = solucion.T

# Valor I(6)
t_6 = np.linspace(0, 6, 100)
sol_6 = odeint(modelo_sir, y0, t_6, args=(beta, gamma))
I_6 = sol_6.T[1]
valor_I_6 = I_6[-1]

# ============================
# 📌 GRÁFICO PRINCIPAL
# ============================
fig = go.Figure()

fig.add_trace(go.Scatter(x=t, y=S, mode='lines',
                         name='Susceptibles S(t)',
                         line=dict(color=COLOR_SUCEPTIBLES, width=2.5)))

fig.add_trace(go.Scatter(x=t, y=I, mode='lines',
                         name='Infectados I(t)',
                         line=dict(color=COLOR_INFECTADOS, width=3),
                         fill='tozeroy',
                         fillcolor='rgba(209,26,42,0.20)'))

fig.add_trace(go.Scatter(x=t, y=R, mode='lines',
                         name='Recuperados R(t)',
                         line=dict(color=COLOR_RECUPERADOS, width=2.5)))

fig.update_layout(
    title=dict(
        text="<b>Modelo SIR - Universidad de San Marcos</b>",
        x=0.5,
        font=dict(size=17, color=COLOR_TITULO)
    ),
    xaxis_title="Tiempo (días)",
    yaxis_title="Número de personas",
    paper_bgcolor="white",
    plot_bgcolor="#fafafa",
    font=dict(color=COLOR_TEXTO),
    margin=dict(l=40, r=40, t=60, b=60)
)

fig.update_xaxes(showgrid=True, gridcolor="#ddd")
fig.update_yaxes(showgrid=True, gridcolor="#ddd")

# ============================
# 📌 TEXTOS
# ============================
texto_intro = r"""
$$
\frac{dS}{dt} = -\beta S I
$$
$$
\frac{dI}{dt} = \beta S I - \gamma I
$$
$$
\frac{dR}{dt} = \gamma I
$$
"""

texto_intro = r"""
$$
\frac{dS}{dt} = -\beta S I
$$
$$
\frac{dI}{dt} = \beta S I - \gamma I
$$
$$
\frac{dR}{dt} = \gamma I
$$
"""

texto_condiciones = rf"""
**Condiciones iniciales**

- $S_0 = {S0}$
- $I_0 = {I0}$
- $R_0 = {R0}$
- $\beta = \frac{{1}}{{7138}}$
- $\gamma = 0.40$
"""

texto_p5 = rf"""
**Infectados en el día 6**

$I(6) \approx {valor_I_6:.2f}$
"""



# ============================
# 📌 LAYOUT (ADAPTADO A TU CSS)
# ============================
layout = html.Div([

    html.Div([

        # IZQUIERDA = TEXTO
        html.Div([
            html.H2("Datos del Modelo", className="title"),
            dcc.Markdown(texto_intro, mathjax=True, className="text-content"),
            dcc.Markdown(texto_condiciones, mathjax=True, className="text-content"),
            dcc.Markdown(texto_p5, mathjax=True, className="text-content"),
        ],
        className="content-sidebar"),

        # DERECHA = GRÁFICO
        html.Div([
            html.H2("Simulación del Modelo SIR", className="title"),
            dcc.Graph(figure=fig)
        ],
        className="content-graph"),

    ], className="page-container-grid")

], style={"backgroundColor": "white", "minHeight": "100vh"})
