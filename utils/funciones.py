import plotly.graph_objects as go
import numpy as np

def grafica_logistica(p0, r, k, t_max):

    t = np.linspace(0, t_max, 100)
    poblacion = k / (1 + ((k - p0) / p0) * np.exp(-r * t))

    # --- Marcadores cada 5 puntos ---
    marker_positions = np.arange(0, len(t), 5)

    # --- Curva suave ---
    trace_linea = go.Scatter(
        x=t,
        y=poblacion,
        mode='lines',
        name='Población P(t)',
        line=dict(color='black', width=2),
        hoverinfo='skip'
    )

    # --- Marcadores separados ---
    trace_markers = go.Scatter(
        x=t[marker_positions],
        y=poblacion[marker_positions],
        mode='markers',
        name='Puntos muestreados',
        marker=dict(
            size=8,
            symbol='circle',
            color='blue',
            line=dict(width=1, color='white')
        ),
        hovertemplate="t: %{x:.2f}<br>P(t): %{y:.2f}<extra></extra>"
    )

    # Línea horizontal de K
    trace_capacidad = go.Scatter(
        x=[0, t_max],
        y=[k, k],
        mode='lines',
        name='Capacidad de Carga (K)',
        line=dict(color='red', width=3, dash='dot'),
        hovertemplate="K: %{y}<extra></extra>"
    )

    fig = go.Figure(data=[trace_linea, trace_markers, trace_capacidad])

    fig.update_layout(
        title="Modelo Logístico de Crecimiento Poblacional",
        title_x=0.5,
        xaxis_title="Tiempo (t)",
        yaxis_title="Población P(t)",
        font=dict(family="Caveat Brush", size=18, color="#75232c"),
        
        plot_bgcolor="rgba(255,255,255,1)",
        paper_bgcolor="rgba(255,255,255,0)",
        
        xaxis=dict(
            showgrid=True,
            gridcolor="lightgrey",
            zeroline=True,
            zerolinecolor="black"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="lightgrey",
            zeroline=True,
            zerolinecolor="black"
        ),

        height=450,
        margin=dict(t=60, b=40, l=50, r=40)
    )

    return fig


def grafica_sir(t, S, I, R, t_max):

    fig = go.Figure()

    # --- Curvas principales (mismo estilo y colores consistentes) ---
    fig.add_trace(go.Scatter(
        x=t, y=S,
        mode='lines',
        name='Susceptibles (S)',
        line=dict(color='blue', width=2),
        hoverinfo='skip'
    ))

    fig.add_trace(go.Scatter(
        x=t, y=I,
        mode='lines',
        name='Infectados (I)',
        line=dict(color='red', width=2),
        hoverinfo='skip'
    ))

    fig.add_trace(go.Scatter(
        x=t, y=R,
        mode='lines',
        name='Recuperados (R)',
        line=dict(color='green', width=2),
        hoverinfo='skip'
    ))

    # === Estilo idéntico a grafica_logistica ===
    fig.update_layout(
        title="Evolución del Modelo SIR",
        title_x=0.5,

        xaxis_title="Tiempo (días)",
        yaxis_title="Número de personas",

        font=dict(family="Caveat Brush", size=18, color="#75232c"),

        plot_bgcolor="rgba(255,255,255,1)",
        paper_bgcolor="rgba(255,255,255,0)",

        xaxis=dict(
            showgrid=True,
            gridcolor="lightgrey",
            zeroline=True,
            zerolinecolor="black",
            range=[0, t_max]
        ),

        yaxis=dict(
            showgrid=True,
            gridcolor="lightgrey",
            zeroline=True,
            zerolinecolor="black"
        ),

        height=450,
        margin=dict(t=60, b=40, l=50, r=40),

        legend=dict(
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="lightgrey",
            borderwidth=1
        )
    )

    return fig


def grafica_seir(t, S, E, I, R):

    # --- Curvas SEIR ---
    trace_S = go.Scatter(
        x=t, y=S,
        mode='lines',
        name='S(t)',
        line=dict(color='blue', width=2),
        hovertemplate="t: %{x:.2f}<br>S: %{y:.2f}<extra></extra>"
    )

    trace_E = go.Scatter(
        x=t, y=E,
        mode='lines',
        name='E(t)',
        line=dict(color='orange', width=2),
        hovertemplate="t: %{x:.2f}<br>E: %{y:.2f}<extra></extra>"
    )

    trace_I = go.Scatter(
        x=t, y=I,
        mode='lines',
        name='I(t)',
        line=dict(color='red', width=2),
        hovertemplate="t: %{x:.2f}<br>I: %{y:.2f}<extra></extra>"
    )

    trace_R = go.Scatter(
        x=t, y=R,
        mode='lines',
        name='R(t)',
        line=dict(color='green', width=2),
        hovertemplate="t: %{x:.2f}<br>R: %{y:.2f}<extra></extra>"
    )

    fig = go.Figure(data=[trace_S, trace_E, trace_I, trace_R])

    # --- MISMO ESTILO QUE LOGISTICA Y SIR ---
    fig.update_layout(
        title="Modelo SEIR",
        title_x=0.5,
        xaxis_title="Tiempo (t)",
        yaxis_title="Población",
        font=dict(family="Caveat Brush", size=18, color="#75232c"),

        plot_bgcolor="rgba(255,255,255,1)",
        paper_bgcolor="rgba(255,255,255,0)",

        xaxis=dict(
            showgrid=True,
            gridcolor="lightgrey",
            zeroline=True,
            zerolinecolor="black"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="lightgrey",
            zeroline=True,
            zerolinecolor="black"
        ),

        height=450,
        margin=dict(t=60, b=40, l=50, r=40)
    )

# utils/funciones.py
import requests
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# ---------------------------
# Datos históricos (por país)
# ---------------------------
def obtener_datos_covid(pais, lastdays="all"):
    """
    Devuelve DataFrame con columnas: fecha (datetime), casos, muertes, recuperados, nuevos, nuevas_muertes
    Usa disease.sh: /historical/{pais}?lastdays=all
    """
    url = f"https://disease.sh/v3/covid-19/historical/{pais}?lastdays={lastdays}"
    r = requests.get(url, timeout=10)

    if r.status_code != 200:
        # algunos países devuelven 404 o estructura distinta -> manejar desde el caller
        return None

    data = r.json()
    if "timeline" not in data:
        return None

    timeline = data["timeline"]
    # timeline["cases"] es dict fecha->valor (strings de fecha)
    df = pd.DataFrame({
        "fecha": list(timeline["cases"].keys()),
        "casos": list(timeline["cases"].values()),
        "muertes": list(timeline["deaths"].values()),
        "recuperados": list(timeline.get("recovered", {}).values()) if isinstance(timeline.get("recovered"), dict) else [0]*len(timeline["cases"])
    })

    # intentamos parsear fechas robustamente
    # fechas suelen venir como "M/D/YY" desde disease.sh; intentar ese formato explícitamente
    try:
        df["fecha"] = pd.to_datetime(df["fecha"], format="%m/%d/%y", errors="raise")
    except (ValueError, TypeError):
        # si no coincide, intentar formato ISO "YYYY-MM-DD"
        try:
            df["fecha"] = pd.to_datetime(df["fecha"], format="%Y-%m-%d", errors="raise")
        except (ValueError, TypeError):
            # último recurso: dejar que dateutil parsee entradas mixtas, convirtiendo errores a NaT
            df["fecha"] = pd.to_datetime(df["fecha"], dayfirst=False, errors="coerce")
    df = df.sort_values("fecha").reset_index(drop=True)

    df["nuevos"] = df["casos"].diff().fillna(0).astype(int)
    df["nuevas_muertes"] = df["muertes"].diff().fillna(0).astype(int)

    return df

# ---------------------------
# Lista de países con coordenadas y casos (global)
# ---------------------------
def obtener_lista_paises():
    """
    Retorna lista de nombres de países (ordenada).
    """
    url = "https://disease.sh/v3/covid-19/countries"
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        return []
    data = r.json()
    return sorted([x.get("country", "") for x in data if x.get("country")])


def obtener_datos_globales_dataframe():
    """
    Retorna DataFrame con columnas: country, cases, deaths, recovered, lat, long
    Usado para el mapa.
    """
    url = "https://disease.sh/v3/covid-19/countries"
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        return pd.DataFrame(columns=["country","cases","deaths","recovered","lat","long"])
    data = r.json()
    df = pd.DataFrame([{
        "country": c.get("country"),
        "cases": c.get("cases", 0),
        "deaths": c.get("deaths", 0),
        "recovered": c.get("recovered", 0),
        "lat": c.get("countryInfo", {}).get("lat", None),
        "long": c.get("countryInfo", {}).get("long", None)
    } for c in data])
    # filtrar sin coordenadas
    df = df.dropna(subset=["lat","long"]).reset_index(drop=True)
    return df

# ---------------------------
# Gráfica de series (estilo SIR/SEIR)
# ---------------------------
def figura_lineal_covid(df, pais, t_max=None):
    """
    Recibe df con 'fecha','casos','muertes','recuperados' y devuelve figura Plotly estilizada.
    """
    fig = go.Figure()

    if df is None or df.empty:
        # figura vacía con ejes
        x = pd.date_range(start=pd.Timestamp.now(), periods=2)
        fig.add_trace(go.Scatter(x=x, y=[0,0], mode="lines", name="No data"))
        fig.update_layout(
            title=f"Evolución COVID-19 en {pais}",
            font=dict(family="Caveat Brush", size=16, color="#75232c"),
            plot_bgcolor="white", paper_bgcolor="rgba(255,255,255,0)"
        )
        return fig

    # trazas
    fig.add_trace(go.Scatter(
        x=df["fecha"], y=df["casos"], mode="lines", name="Casos Totales",
        line=dict(color="orange", width=3)
    ))

    fig.add_trace(go.Scatter(
        x=df["fecha"], y=df["muertes"], mode="lines", name="Muertes Totales",
        line=dict(color="red", width=3)
    ))

    # opcional: recuperados si existen
    if "recuperados" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["fecha"], y=df["recuperados"], mode="lines", name="Recuperados",
            line=dict(color="green", width=2, dash="dash")
        ))

    # estilo similar al resto de tu proyecto
    x_range = None
    if t_max is not None:
        # si t_max es número de días, podemos limitar el eje x a las últimas t_max filas
        x_range = [df["fecha"].iloc[0], df["fecha"].iloc[-1]]

    fig.update_layout(
        title=f"Evolución COVID-19 en {pais}",
        title_x=0.5,
        xaxis_title="Fecha",
        yaxis_title="Número de personas",
        font=dict(family="Caveat Brush", size=16, color="#75232c"),
        plot_bgcolor="white",
        paper_bgcolor="rgba(255,255,255,0)",
        xaxis=dict(showgrid=True, gridcolor="lightgrey"),
        yaxis=dict(showgrid=True, gridcolor="lightgrey"),
        height=430,
        margin=dict(t=60, b=40, l=50, r=40),
        legend=dict(x=0.02, y=0.98)
    )
    return fig

# ---------------------------
# Mapa global (burbuja) — usa la misma fuente y colores
# ---------------------------
def mapa_covid_global():
    df = obtener_datos_globales_dataframe()
    if df is None or df.empty:
        return go.Figure()

    # escala de tamaños (suavizada)
    max_cases = df["cases"].replace(0, np.nan).max()
    if pd.isna(max_cases) or max_cases == 0:
        max_cases = 1
    sizes = (df["cases"] / max_cases) * 40
    sizes = sizes.clip(lower=4)

    fig = go.Figure()

    fig.add_trace(go.Scattergeo(
        lon=df["long"],
        lat=df["lat"],
        text=df["country"] + "<br>Casos: " + df["cases"].map("{:,}".format).astype(str),
        marker=dict(
            size=sizes,
            color=df["cases"],
            colorscale="Reds",
            opacity=0.75,
            line=dict(width=0.3, color="black"),
            showscale=True,
            colorbar=dict(title="Casos", tickformat=",")
        ),
        hoverinfo="text",
        mode="markers"
    ))

    fig.update_layout(
        title="Mapa Global de Casos COVID-19",
        title_x=0.5,
        geo=dict(
            showland=True,
            landcolor="rgb(245,245,245)",
            showcountries=True,
            countrycolor="rgb(200,200,200)",
            projection_type="natural earth"
        ),
        font=dict(family="Caveat Brush", size=16, color="#75232c"),
        paper_bgcolor="rgba(255,255,255,0)",
        margin=dict(t=60, b=20, l=0, r=0)
    )

    return fig
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from functools import lru_cache

# ============================================================
# SESIÓN GLOBAL DE REQUESTS (acelera x4)
# ============================================================
session = requests.Session()


# ============================================================
# API: Países SIN clima (rápido)
# ============================================================
def get_countries():
    """
    Carga lista de países desde RESTCountries sin pedir clima.
    Evita 250 llamadas API lentas. Ultra rápido (<200ms).
    """
    url = "https://restcountries.com/v3.1/all?fields=name,latlng"
    r = session.get(url, timeout=10)

    if r.status_code != 200:
        return pd.DataFrame(columns=["country", "lat", "lon"])

    data = r.json()
    rows = []

    for c in data:
        if "latlng" not in c or len(c["latlng"]) < 2:
            continue
        rows.append({
            "country": c["name"]["common"],
            "lat": c["latlng"][0],
            "lon": c["latlng"][1]
        })

    df = pd.DataFrame(rows)
    df = df.sort_values("country")
    return df


# ============================================================
# API: Clima Open-Meteo cacheado
# ============================================================
@lru_cache(maxsize=300)
def get_weather(lat, lon):
    """
    Consulta Open-Meteo y devuelve temperaturas horarias.
    Cacheado por país (rápido en 50 ms).
    """

    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&hourly=temperature_2m"
    )

    r = session.get(url, timeout=10).json()

    hours = r["hourly"]["time"]
    temps = r["hourly"]["temperature_2m"]

    df = pd.DataFrame({"time": hours, "temperature": temps})
    df["time"] = pd.to_datetime(df["time"])

    return df


# ============================================================
# Gráfico de Líneas
# ============================================================
def clima_line_plot(df, country):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["time"],
        y=df["temperature"],
        mode="lines",
        line=dict(color="black", width=2),
        name="Temperatura"
    ))

    fig.update_layout(
        title=f"Temperatura Horaria — {country}",
        title_x=0.5,
        font=dict(family="Caveat Brush", size=20),
        xaxis_title="Tiempo",
        yaxis_title="Temperatura (°C)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=40, r=20, t=50, b=40)
    )

    return fig


# ============================================================
# Mapa Mundial — sin pedir clima (rápido)
# ============================================================
def clima_world_map(df):
    """
    Mapa global simple (solo posiciones), NO usa sensación térmica.
    rápido y suficiente para mostrar países.
    """

    fig = px.scatter_geo(
        df,
        lat="lat",
        lon="lon",
        hover_name="country",
        opacity=0.6,
        projection="natural earth",
        title="Mapa Mundial (Ubicación de Países)"
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        geo=dict(
            showcountries=True,
            showcoastlines=True,
            landcolor="rgb(230,230,230)"
        )
    )

    return fig
