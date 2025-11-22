import dash
from dash import html, dcc, callback, Input, Output, State
import numpy as np
from scipy.integrate import solve_ivp

from utils.funciones import grafica_seir   # ⬅️ IMPORTAMOS EL ESTILO UNIFICADO

dash.register_page(__name__, path='/seir', name='Modelo SEIR')


# -------------------------------------------------------------
# LAYOUT — 3 CONTENEDORES
# -------------------------------------------------------------
layout = html.Div(className='contenedor-principal', children=[

    # ---------- PANEL IZQUIERDO ----------
    html.Div(className='panel-izquierdo', children=[
        html.H2("Modelo SEIR - Con Incubación", className="titulo"),

        html.Label("Población Total (N):", className='input-label'),
        dcc.Input(id='input-N-seir', type='number', value=1000, className='input-field'),

        html.Label("Tasa de transmisión (β):", className='input-label'),
        dcc.Input(id='input-beta-seir', type='number', value=0.5, step=0.01, className='input-field'),

        html.Label("Tasa de recuperación (γ):", className='input-label'),
        dcc.Input(id='input-gamma-seir', type='number', value=0.1, step=0.01, className='input-field'),

        html.Label("Tasa de incubación (σ):", className='input-label'),
        dcc.Input(id='input-sigma-seir', type='number', value=0.2, step=0.01, className='input-field'),

        html.Label("Infectados iniciales (I₀):", className='input-label'),
        dcc.Input(id='input-I0-seir', type='number', value=1, className='input-field'),

        html.Label("Expuestos iniciales (E₀):", className='input-label'),
        dcc.Input(id='input-E0-seir', type='number', value=0, className='input-field'),

        html.Label("Tiempo de simulación (días):", className='input-label'),
        dcc.Input(id='input-tiempo-seir', type='number', value=100, className='input-field'),

        html.Button('Simular Epidemia SEIR', id='btn-simular-seir',
                    n_clicks=0, className='btn-generar'),
    ]),

    # ---------- PANEL DERECHO ----------
    html.Div(className='panel-derecho', children=[
        dcc.Graph(id='graph-seir-evolucion',
                  style={"height": "450px", "width": "100%"})
    ]),

    # ---------- PANEL DE TEORÍA ----------
    html.Div(className='panel-teoria', children=[
        dcc.Markdown(r"""
### Modelo SEIR – Fundamentos

El modelo SEIR añade un compartimento importante al SIR clásico:

- **S:** Susceptibles  
- **E:** Expuestos (infectados pero *no infecciosos*)  
- **I:** Infectados (transmiten la enfermedad)  
- **R:** Recuperados  

### Ecuaciones diferenciales

$$
\begin{aligned}
\frac{dS}{dt} &= - \frac{\\beta S I}{N} \\\\
\frac{dE}{dt} &= \frac{\\beta S I}{N} - \sigma E \\\\
\frac{dI}{dt} &= \sigma E - \\gamma I \\\\
\frac{dR}{dt} &= \\gamma I
\end{aligned}
$$

Donde:

- **N:** Población total  
- **β:** Tasa de transmisión  
- **γ:** Tasa de recuperación  
- **σ:** Tasa de incubación  
""", mathjax=True)
    ])
])


# -------------------------------------------------------------
# CALLBACK GENERAL
# -------------------------------------------------------------
@callback(
    Output('graph-seir-evolucion', 'figure'),
    Input('btn-simular-seir', 'n_clicks'),
    State('input-N-seir', 'value'),
    State('input-beta-seir', 'value'),
    State('input-gamma-seir', 'value'),
    State('input-sigma-seir', 'value'),
    State('input-I0-seir', 'value'),
    State('input-E0-seir', 'value'),
    State('input-tiempo-seir', 'value')
)
def update_seir_graph(n_clicks, N, beta, gamma, sigma, I0, E0, t_max):

    # Primera carga: gráfico vacío pero con estilo
    if n_clicks == 0:
        t = np.linspace(0, t_max, 500)
        return grafica_seir(t, np.zeros_like(t), np.zeros_like(t),
                            np.zeros_like(t), np.zeros_like(t))

    # Condiciones iniciales
    R0 = 0
    S0 = N - I0 - E0
    y0 = [S0, E0, I0, R0]

    # Sistema SEIR
    def seir_model(t, y):
        S, E, I, R = y
        return [
            -(beta * S * I) / N,
            (beta * S * I) / N - sigma * E,
            sigma * E - gamma * I,
            gamma * I
        ]

    t_eval = np.linspace(0, t_max, 500)
    sol = solve_ivp(seir_model, [0, t_max], y0, t_eval=t_eval)

    S, E, I, R = sol.y
    t = sol.t

    # Usamos la función externa con el estilo unificado
    return grafica_seir(t, S, E, I, R)
