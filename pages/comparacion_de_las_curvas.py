import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint

dash.register_page(__name__, path="/comparacion_de_las_curvas", name="Comparación I(t)")

# === PALETA DE COLORES CLAROS ===
COLOR_BASELINE = '#0077CC'
COLOR_BETA_HIGH = '#FF8800'
COLOR_GAMMA_HIGH = '#00AA44'

COLOR_TITULO = '#5B2A86'
COLOR_TEXTO = '#2A2A2A'
COLOR_FONDO = '#F5F7FA'
COLOR_CONTAINER = '#FFFFFF'
COLOR_BORDER = '#E0E0E0'
COLOR_GRID = '#CCCCCC'


# === MODELO SIR ===
def modelo_sir(y, t, b, g):
    S, I, R = y
    dS_dt = -b * S * I
    dI_dt = b * S * I - g * I
    dR_dt = g * I
    return [dS_dt, dI_dt, dR_dt]


# === PARÁMETROS ===
N = 10000.0
I0 = 10.0
S0 = N - I0
R0_init = 0.0
y0 = [S0, I0, R0_init]
t = np.linspace(0, 100, 100)

gamma_base = 0.25
R0_base = 2.5
beta_base = R0_base * gamma_base / N

# === SOLUCIONES ===
sol1 = odeint(modelo_sir, y0, t, args=(beta_base, gamma_base))
I_base = sol1[:, 1]

beta_double = beta_base * 2
sol2 = odeint(modelo_sir, y0, t, args=(beta_double, gamma_base))
I_beta = sol2[:, 1]

gamma_double = gamma_base * 2
sol3 = odeint(modelo_sir, y0, t, args=(beta_base, gamma_double))
I_gamma = sol3[:, 1]


# === GRÁFICO COMPARATIVO ===
def crear_grafico_comparativo(tiempo, i_base, i_beta, i_gamma):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=tiempo, y=i_base, mode='lines',
                             name='baseline', line=dict(color=COLOR_BASELINE, width=3)))

    fig.add_trace(go.Scatter(x=tiempo, y=i_beta, mode='lines',
                             name='b_double', line=dict(color=COLOR_BETA_HIGH, width=3)))

    fig.add_trace(go.Scatter(x=tiempo, y=i_gamma, mode='lines',
                             name='k_double', line=dict(color=COLOR_GAMMA_HIGH, width=3)))

    fig.update_layout(
        title=dict(text="<b>Comparación de I(t) entre escenarios</b>",
                   x=0.5, font=dict(size=20, color=COLOR_TITULO)),
        xaxis_title="Días",
        yaxis_title="Personas",
        paper_bgcolor=COLOR_CONTAINER,
        plot_bgcolor="#FAFAFA",
        font=dict(color=COLOR_TEXTO, size=13),
        margin=dict(l=50, r=40, t=70, b=50),
        height=430,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.7)"
        )
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=COLOR_GRID)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=COLOR_GRID)

    return fig


fig_comparacion = crear_grafico_comparativo(t, I_base, I_beta, I_gamma)


# === LAYOUT EN TONOS CLAROS CON CONTENEDORES ===
layout = html.Div([

    # TÍTULO PRINCIPAL
    html.H1("Comparación de Dinámicas de Difusión",
            style={
                'textAlign': 'center',
                'color': COLOR_TITULO,
                'fontSize': '32px',
                'marginBottom': '25px'
            }),

    # ==============================
    #      CONTENEDORES SEPARADOS
    # ==============================

    html.Div([
        # COLUMNA IZQUIERDA – TEXTO
        html.Div([
            html.Div([
                html.H3("Análisis Descriptivo de Parámetros",
                        style={'color': COLOR_BASELINE, 'fontSize': '22px'}),

                dcc.Markdown(r'''
                Este estudio compara la dinámica temporal de los individuos en el estado
                **Infectados / Promotores Activos** bajo tres configuraciones del modelo SIR.

                **1. Baseline (Azul):**  
                Escenario con parámetros originales.  
                La curva presenta un pico estable cerca del día **25**.

                **2. b_double (Naranja):**  
                El parámetro de transmisión $\beta$ se duplica.  
                Esto provoca una difusión **mucho más rápida y con un pico mayor**.

                **3. k_double (Verde):**  
                El parámetro de recuperación/desinterés $\gamma$ se duplica.  
                La curva se vuelve **más plana**, con una reducción drástica del pico.
                ''',
                mathjax=True,
                style={'color': COLOR_TEXTO, 'fontSize': '16px', 'lineHeight': '1.6'})
            ],
            style={
                'backgroundColor': COLOR_CONTAINER,
                'border': f'1px solid {COLOR_BORDER}',
                'borderRadius': '12px',
                'padding': '25px',
                'boxShadow': '0 2px 6px rgba(0,0,0,0.08)',
            })
        ],
        style={'width': '45%'}),

        # COLUMNA DERECHA – GRÁFICO
        html.Div([
            html.Div([
                dcc.Graph(
                    figure=fig_comparacion,
                    config={'displayModeBar': False},
                    style={'height': '430px'}
                )
            ],
            style={
                'backgroundColor': COLOR_CONTAINER,
                'border': f'1px solid {COLOR_BORDER}',
                'borderRadius': '12px',
                'padding': '20px',
                'boxShadow': '0 2px 6px rgba(0,0,0,0.08)',
            })
        ],
        style={'width': '55%'}),

    ],
    style={
        'display': 'flex',
        'flexDirection': 'row',
        'justifyContent': 'space-between',
        'alignItems': 'flex-start',
        'gap': '25px',
        'maxWidth': '1200px',
        'margin': '0 auto'
    }),

],
style={
    'backgroundColor': COLOR_FONDO,
    'minHeight': '100vh',
    'padding': '40px 20px',
    'fontFamily': 'Segoe UI, sans-serif'
})
