import dash
from dash import html, dcc

dash.register_page(__name__, path="/", name="Inicio")

layout = html.Div(
    style={
        "display": "flex",
        "flexDirection": "column",
        "gap": "30px",
        "padding": "20px",
        "backgroundColor": "rgba(255,255,255,0.8)",
        "borderRadius": "12px",
        "boxShadow": "0 3px 8px rgba(0,0,0,0.2)",
        "marginTop": "20px"
    },
    children=[

        # Presentación personal
        html.Div(
            style={
                "textAlign": "center",
                "padding": "20px",
                "backgroundColor": "rgba(255,255,255,0.9)",
                "borderRadius": "10px",
                "boxShadow": "0 2px 6px rgba(0,0,0,0.15)"
            },
            children=[
                html.H2("Presentación", style={"color": "#b0344e", "fontSize": "2rem"}),
                html.P("Hola, soy Jardiny Irazhova Guerra Velásquez.", style={"fontSize": "1.25rem"}),
                html.P("Este espacio forma parte del curso Técnicas de Modelamiento Matemático.", style={"fontSize": "1.25rem"}),
                html.P("Universidad Nacional Mayor de San Marcos.", style={"fontSize": "1.25rem"}),
            ]
        ),

        # Introducción más natural
        html.Div(
            style={
                "padding": "20px",
                "backgroundColor": "rgba(255,255,255,0.9)",
                "borderRadius": "10px",
                "boxShadow": "0 2px 6px rgba(0,0,0,0.15)",
                "fontSize": "1.15rem",
                "lineHeight": "1.7",
                "textAlign": "justify"
            },
            children=[
                dcc.Markdown("""
Este dashboard reúne de manera sencilla varios de los modelos que hemos trabajado a lo largo del curso.  
La idea es tener un espacio donde podamos visualizar, ajustar parámetros y entender mejor cómo se comportan los sistemas dinámicos, sobre todo los relacionados con el crecimiento poblacional y la propagación de enfermedades.

No es un repositorio teórico, sino un lugar para *explorar*, probar y comparar.
                """)
            ]
        ),

        # Contenido del dashboard (orgánico, natural)
        html.Div(
            style={
                "padding": "20px",
                "backgroundColor": "rgba(255,255,255,0.9)",
                "borderRadius": "10px",
                "boxShadow": "0 2px 6px rgba(0,0,0,0.15)",
                "fontSize": "1.15rem",
                "lineHeight": "1.7"
            },
            children=[
                dcc.Markdown("""
### ¿Qué encontrarás aquí?

- Simulaciones del modelo **SIR**, donde se puede ver cómo evoluciona una epidemia según los parámetros.
- El modelo **SEIR**, que añade la etapa de exposición antes de contagiar.
- Algunos casos prácticos relacionados con vacunación, control epidemiológico y curvas de contagio.
- Otros modelos vistos en clase que nos ayudan a entender cómo se comportan poblaciones o sistemas con crecimiento limitado.

La navegación está arriba, así que simplemente elige el modelo que quieres revisar.
                """)
            ]
        ),
    ]
)
