import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint

dash.register_page(
    __name__,
    path="/adoptando",
    name="Adoptantes Pasivos R(t)"
)

# --------------------------
# 🎨 PALETA (LIGHT THEME)
# --------------------------
COLOR_LINEA_PRINCIPAL = '#0077cc'
COLOR_TITULO = '#6a1b9a'
COLOR_TEXTO_SECUNDARIO = '#333'
COLOR_FONDO_GRAFICO = '#ffffff'
COLOR_FONDO_PAPEL = '#ffffff'
COLOR_GRID = '#cccccc'

# --------------------------
# 📌 MODELO SIR
# --------------------------
def modelo_sir(y, t, b, g):
    S, I, R = y
    return [
        -b * S * I,
        b * S * I - g * I,
        g * I
    ]

# --------------------------
# 📌 PARÁMETROS
# --------------------------
N = 10000.0
I0 = 10.0
S0 = N - I0
y0 = [S0, I0, 0.0]
t = np.linspace(0, 100, 100)

gamma_base = 0.25
R0_base = 2.5
beta_base = R0_base * gamma_base / N

# --------------------------
# 📌 CURVAS
# --------------------------
def calcular_curva(beta, gamma):
    sol = odeint(modelo_sir, y0, t, args=(beta, gamma))
    return sol[:, 2]

R1 = calcular_curva(beta_base, gamma_base)
R2 = calcular_curva(beta_base * 2, gamma_base)
R3 = calcular_curva(beta_base, gamma_base * 2)

# --------------------------
# 📌 GRÁFICOS
# --------------------------
def crear_grafico_adopters(tiempo, datos_r, titulo, y_max=None):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=tiempo, y=datos_r, mode='lines',
        name='R(t)',
        line=dict(color=COLOR_LINEA_PRINCIPAL, width=2.5)
    ))

    fig.update_layout(
        title=dict(text=f"<b>{titulo}</b>", x=0.5,
                   font=dict(size=15, color=COLOR_TITULO)),
        xaxis_title="Días",
        yaxis_title="Personas",
        paper_bgcolor=COLOR_FONDO_PAPEL,
        plot_bgcolor=COLOR_FONDO_GRAFICO,
        font=dict(color=COLOR_TEXTO_SECUNDARIO, size=11),
        height=300,
        margin=dict(l=40, r=20, t=50, b=40),
    )

    fig.update_xaxes(
        showgrid=True,
        gridwidth=1, gridcolor=COLOR_GRID,
        zeroline=False,
        linecolor='#444'
    )

    yaxis_cfg = dict(
        showgrid=True, gridwidth=1,
        gridcolor=COLOR_GRID,
        zeroline=False,
        linecolor='#444'
    )
    if y_max is not None:
        yaxis_cfg['range'] = [0, y_max]

    fig.update_yaxes(yaxis_cfg)
    return fig

# Figuras
fig_base = crear_grafico_adopters(t, R1, "R(t) - baseline", y_max=9500)
fig_b_double = crear_grafico_adopters(t, R2, "R(t) - β doble", y_max=10200)
fig_k_double = crear_grafico_adopters(t, R3, "R(t) - γ doble", y_max=4000)

# --------------------------
# 📌 LAYOUT (LIGHT)
# --------------------------
layout = html.Div([

    html.H1("Adoptantes Pasivos R(t): Acumulados",
            style={
                'textAlign': 'center',
                'color': COLOR_TITULO,
                'paddingBottom': '20px',
                'fontSize': '26px'
            }),

    # Contenedor
    html.Div([

        # Fila 1
        html.Div([
            html.Div(
                dcc.Graph(figure=fig_base, config={'displayModeBar': False}),
                style={'flex': '1', 'minWidth': '300px', 'padding': '10px'}
            ),

            html.Div(
                dcc.Graph(figure=fig_b_double, config={'displayModeBar': False}),
                style={'flex': '1', 'minWidth': '300px', 'padding': '10px'}
            ),

        ], style={
            'display': 'flex',
            'flexWrap': 'wrap',
            'justifyContent': 'center',
            'width': '100%'
        }),

        # Fila 2
        html.Div([
            html.Div(
                dcc.Graph(figure=fig_k_double, config={'displayModeBar': False}),
                style={'width': '60%', 'minWidth': '300px',
                       'margin': '0 auto', 'padding': '10px'}
            )
        ])

    ], style={
        'backgroundColor': '#ffffff',
        'borderRadius': '10px',
        'padding': '20px',
        'border': '1px solid #ddd'
    }),

    # Interpretación
    html.Div([
        html.H4("Interpretación: Acumulación de Adoptantes",
                style={'color': COLOR_LINEA_PRINCIPAL}),

        dcc.Markdown(r'''
Los gráficos muestran el número acumulado de **Adoptantes Pasivos** $R(t)$:

1. **Baseline:** Crecimiento estándar, ~90% de adopción.
2. **β doble:** La adopción se acelera llegando casi al 100%.
3. **γ doble:** Aumenta la “recuperación” → solo ~3700 adoptantes.
        ''', mathjax=True, style={'color': '#333'})
    ],
        style={'marginTop': '30px', 'maxWidth': '800px',
               'marginLeft': 'auto', 'marginRight': 'auto'})
],
    style={
        'backgroundColor': '#f7f7f7',
        'minHeight': '100vh',
        'padding': '20px',
        'fontFamily': 'sans-serif'
    })
