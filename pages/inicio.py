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
            className="content-box",
            style={
                "textAlign": "center",
                "padding": "20px",
                "backgroundColor": "rgba(255,255,255,0.9)",
                "borderRadius": "10px",
                "boxShadow": "0 2px 6px rgba(0,0,0,0.15)"
            },
            children=[
                html.H2("Presentación", style={"color": "#d0021b", "fontSize": "2rem"}),
                html.P("Nombre: Jardiny Irazhova Guerra Velásquez", style={"fontSize": "1.3rem"}),
                html.P("Curso: Técnicas de Modelamiento", style={"fontSize": "1.3rem"}),
                html.P("Universidad: Universidad Nacional Mayor de San Marcos", style={"fontSize": "1.3rem"})
            ]
        ),

        # Mensaje introductorio o cita
        html.Div(
            className="content-box",
            style={"textAlign": "center", "fontSize": "1.2rem"},
            children=[
                dcc.Markdown("""
Bienvenido/a al entorno interactivo del curso **Técnicas de Modelamiento Matemático**.  
Aquí encontrarás ejemplos visuales y aplicaciones de modelos diferenciales vistos en clase.
---
                """)
            ]
        )
    ]
)
