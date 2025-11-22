import dash
from dash import html, dcc, callback, Input, Output, State

from utils.funciones import grafica_logistica

# Registro de página
dash.register_page(
    __name__,
    path="/llamado",
    name="Modelo con llamado"
)

# Layout con el diseño del dashboard
layout = html.Div(
    className="contenedor-principal",
    children=[

        # ------------------------
        # COLUMNA IZQUIERDA
        # ------------------------
        html.Div(
            className="contenedor-izquierdo",
            children=[
                html.H2("Parámetros del modelo (Refactorizado)", className="titulo"),

                html.Div([
                    html.Label("Población inicial P₀:", className="input-label"),
                    dcc.Input(
                        id="input-p0-ref",
                        type="number",
                        value=200,
                        className="input-field"
                    ),
                ]),

                html.Div([
                    html.Label("Tasa de crecimiento r:", className="input-label"),
                    dcc.Input(
                        id="input-r-ref",
                        type="number",
                        value=0.04,
                        className="input-field"
                    ),
                ]),

                html.Div([
                    html.Label("Capacidad de carga K:", className="input-label"),
                    dcc.Input(
                        id="input-k-ref",
                        type="number",
                        value=750,
                        className="input-field"
                    ),
                ]),

                html.Div([
                    html.Label("Tiempo máximo t:", className="input-label"),
                    dcc.Input(
                        id="input-t-ref",
                        type="number",
                        value=100,
                        className="input-field"
                    ),
                ]),

                html.Button(
                    "Generar gráfico",
                    id="btn-generar-ref",
                    n_clicks=0,
                    className="btn-generar"
                )
            ]
        ),

        # ------------------------
        # COLUMNA DERECHA
        # ------------------------
        html.Div(
            className="contenedor-derecho",
            children=[
                html.H3(
                    "Modelo Logístico Generado con Función Externa",
                    style={"textAlign": "center", "color": "#d0021b"}
                ),
                dcc.Graph(
                    id="graph-logistico-refactorizado",
                    style={"height": "430px", "width": "100%"}
                )
            ]
        )
    ]
)


# --------------------------------
# CALLBACK
# --------------------------------
@callback(
    Output("graph-logistico-refactorizado", "figure"),
    Input("btn-generar-ref", "n_clicks"),
    State("input-p0-ref", "value"),
    State("input-r-ref", "value"),
    State("input-k-ref", "value"),
    State("input-t-ref", "value"),
    prevent_initial_call=False
)
def update_graph_refactorizado(n_clicks, p0, r, k, t_max):
    # Simplemente llamamos la función del archivo funciones.py
    fig = grafica_logistica(p0, r, k, t_max)
    return fig
