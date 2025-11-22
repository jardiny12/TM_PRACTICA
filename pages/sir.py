import dash
from dash import html, dcc, callback, Input, Output, State
import numpy as np
from scipy.integrate import solve_ivp
from utils.funciones import grafica_sir   # ← usa el mismo estilo

dash.register_page(__name__, path='/sir', name='Modelo SIR')

# ---------------------------------------------------------------------
# LAYOUT — MISMO DISEÑO QUE EL SEIR
# ---------------------------------------------------------------------
layout = html.Div(className='contenedor-principal', children=[

    # ================= PANEL IZQUIERDO =================
    html.Div(className='panel-izquierdo', children=[

        html.H2("Modelo SIR - Epidemiología", className='titulo'),

        html.Label("Población Total (N):", className='input-label'),
        dcc.Input(id='input-N-sir', type='number', value=1000, className='input-field'),

        html.Label("Tasa de transmisión (β):", className='input-label'),
        dcc.Input(id='input-beta-sir', type='number', value=0.3, step=0.01, className='input-field'),

        html.Label("Tasa de recuperación (γ):", className='input-label'),
        dcc.Input(id='input-gamma-sir', type='number', value=0.1, step=0.01, className='input-field'),

        html.Label("Infectados iniciales (I₀):", className='input-label'),
        dcc.Input(id='input-I0-sir', type='number', value=1, className='input-field'),

        html.Label("Tiempo total (días):", className='input-label'),
        dcc.Input(id='input-tiempo-sir', type='number', value=100, className='input-field'),

        html.Button("Simular Modelo SIR",
            id="btn-simular-sir",
            className="btn-generar"
        )
    ]),

    # ================= PANEL DERECHO (GRÁFICO) =================
    html.Div(className='panel-derecho', children=[
        dcc.Graph(id='graph-sir-evolucion',
                  style={"height": "450px", "width": "100%"})
    ]),

    # ================= PANEL DE TEORÍA =================
    html.Div(className='panel-teoria', children=[

        dcc.Markdown(r"""
###  Modelo SIR – Fundamentos

El modelo SIR divide a la población en:
- **S:** Susceptibles  
- **I:** Infectados  
- **R:** Recuperados  

### ➤ Ecuaciones diferenciales

$$
\frac{dS}{dt} = -\frac{\beta S I}{N}
$$

$$
\frac{dI}{dt} = \frac{\beta S I}{N} - \gamma I
$$

$$
\frac{dR}{dt} = \gamma I
$$

Donde:

- **β:** Tasa de transmisión  
- **γ:** Tasa de recuperación  
- **N:** Población total
""", mathjax=True)
    ])
])

# ---------------------------------------------------------------------
# CALLBACK
# ---------------------------------------------------------------------
@callback(
    Output('graph-sir-evolucion', 'figure'),
    Input('btn-simular-sir', 'n_clicks'),
    State('input-N-sir', 'value'),
    State('input-beta-sir', 'value'),
    State('input-gamma-sir', 'value'),
    State('input-I0-sir', 'value'),
    State('input-tiempo-sir', 'value')
)
def update_sir_graph(n_clicks, N, beta, gamma, I0, t_max):

    if not n_clicks:
        t = np.linspace(0, t_max, 500)
        S = I = R = np.zeros_like(t)
        return grafica_sir(t, S, I, R, t_max)

    # Condiciones iniciales
    R0 = 0
    S0 = N - I0
    y0 = [S0, I0, R0]

    # Sistema SIR
    def sir_model(t, y):
        S, I, R = y
        return [
            -beta * S * I / N,
            beta * S * I / N - gamma * I,
            gamma * I
        ]

    t_eval = np.linspace(0, t_max, 500)
    sol = solve_ivp(sir_model, [0, t_max], y0, t_eval=t_eval)

    S, I, R = sol.y
    t = sol.t

    return grafica_sir(t, S, I, R, t_max)
