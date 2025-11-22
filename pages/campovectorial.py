import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__, path="/campovectorial", name="Campo Vectorial")

# ======================================================
# =====================   LAYOUT   =====================
# ======================================================

layout = html.Div(
    className='contenedor-principal',
    children=[

        # ------------------ IZQUIERDA ------------------
        html.Div(className='contenedor-izquierdo', children=[
            html.H2("Campo Vectorial 2D", className="titulo"),

            html.Label("Seleccionar ejemplo:", className="input-label"),
            dcc.Dropdown(
                id='dropdown-ejemplos',
                options=[
                    {"label": "Flujo circular: dx=-y, dy=x", "value": "circular"},
                    {"label": "Punto de silla: dx=x, dy=-y", "value": "silla"},
                    {"label": "Flujo logístico: dx=x*(1-x), dy=y", "value": "logistico"},
                    {"label": "Sin/Cos: dx=sin(x), dy=cos(y)", "value": "sincos"},
                    {"label": "Lotka-Volterra", "value": "lotka"},
                ],
                value="circular",
                className='input-field'
            ),

            html.Label("dx/dt = f(x,y):", className='input-label'),
            dcc.Input(id='input-dxdt', type='text', value='-y', className='input-field'),

            html.Label("dy/dt = g(x,y):", className='input-label'),
            dcc.Input(id='input-dydt', type='text', value='x', className='input-field'),

            html.Label("Rango X (±):", className='input-label'),
            dcc.Input(id='input-range-x', type='number', value=3, className='input-field'),

            html.Label("Rango Y (±):", className='input-label'),
            dcc.Input(id='input-range-y', type='number', value=3, className='input-field'),

            html.Label("Mallado:", className='input-label'),
            dcc.Input(id='input-mallado', type='number', value=20, className='input-field'),

            html.Button("Generar Campo", id="btn-generar-campo", n_clicks=0, className="btn-generar"),
        ]),

        # ------------------ DERECHA ------------------
        html.Div(className='contenedor-derecho', children=[
            html.H2("Visualización del Campo Vectorial", className="titulo"),

            html.Div(
                id='error-output-campo',
                style={'color': 'red', 'fontWeight': 'bold', 'marginBottom': '10px'}
            ),

            dcc.Graph(id='graph-campo-vectorial')
        ])
    ]
)

# ======================================================
# ==== CALLBACK 1 : Cargar ecuaciones por ejemplo ======
# ======================================================

@callback(
    Output('input-dxdt', 'value'),
    Output('input-dydt', 'value'),
    Input('dropdown-ejemplos', 'value')
)
def cargar_ejemplo(ejemplo):
    """Actualiza dx/dt y dy/dt al elegir un ejemplo."""

    if ejemplo == "circular":
        return "-y", "x"

    if ejemplo == "silla":
        return "x", "-y"

    if ejemplo == "logistico":
        return "x*(1-x)", "y"

    if ejemplo == "sincos":
        return "np.sin(x)", "np.cos(y)"

    if ejemplo == "lotka":
        return "0.1*x - 0.2*x*y", "-0.1*y + 0.1*x*y"

    return "", ""


# ======================================================
# === CALLBACK 2 : Generar el gráfico del campo =========
# ======================================================

@callback(
    Output('graph-campo-vectorial', 'figure'),
    Output('error-output-campo', 'children'),
    Input('btn-generar-campo', 'n_clicks'),
    Input('input-dxdt', 'value'),
    Input('input-dydt', 'value'),
    State('input-range-x', 'value'),
    State('input-range-y', 'value'),
    State('input-mallado', 'value'),
)
def update_vector_field(n_clicks, eq_dxdt, eq_dydt, range_x, range_y, mallado):
    """Genera el campo vectorial."""
    
    fig = go.Figure()

    if n_clicks == 0:
        return fig, ""

    try:
        range_x = float(range_x)
        range_y = float(range_y)
        mallado = max(5, int(mallado))

        x_vals = np.linspace(-range_x, range_x, mallado)
        y_vals = np.linspace(-range_y, range_y, mallado)
        x, y = np.meshgrid(x_vals, y_vals)

        safe = {
            "np": np,
            "x": x,
            "y": y,
            "sin": np.sin,
            "cos": np.cos,
            "exp": np.exp,
            "sqrt": np.sqrt,
            "log": np.log
        }

        u = eval(eq_dxdt, {"__builtins__": None}, safe)
        v = eval(eq_dydt, {"__builtins__": None}, safe)

        # Normalización
        mag = np.sqrt(u**2 + v**2) + 1e-9
        u_norm = u / mag
        v_norm = v / mag

        L = (range_x * 2 / mallado) * 0.4
        x_end = x + u_norm * L
        y_end = y + v_norm * L

        XO, YO = [], []
        for i in range(mallado):
            for j in range(mallado):
                XO += [x[i,j], x_end[i,j], None]
                YO += [y[i,j], y_end[i,j], None]

        fig.add_trace(go.Scatter(x=XO, y=YO, mode="lines", line=dict(width=1.2, color="blue")))
        fig.add_trace(go.Scatter(x=x.flatten(), y=y.flatten(), mode="markers", marker=dict(size=2, color="red")))

        fig.update_layout(
            xaxis=dict(range=[-range_x, range_x], scaleanchor="y"),
            yaxis=dict(range=[-range_y, range_y]),
            plot_bgcolor="white"
        )

        return fig, ""

    except Exception as e:
        return fig, f"ERROR: {e}"
