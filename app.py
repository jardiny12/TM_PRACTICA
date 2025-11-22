import dash
from dash import html, dcc, page_container

app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True   # <<< AGREGA ESTO
)

server = app.server

app.layout = html.Div(className='app-container', children=[
    html.Div(className='app-header', children=[
        html.H1("Técnicas de Modelamiento Matemático")
    ]),

    html.Div(className='navigation', children=[
        html.Div(className='nav-links', children=[
            dcc.Link(
                page["name"],
                href=page["relative_path"],
                style={
                    "backgroundColor": "#b35c5c",
                    "padding": "6px 14px",
                    "borderRadius": "6px",
                    "color": "white",
                    "textDecoration": "none",
                    "fontWeight": "bold"
                }
            )
            for page in dash.page_registry.values()
        ])
    ]),

    page_container
])

if __name__ == "__main__":
    app.run(debug=True)
