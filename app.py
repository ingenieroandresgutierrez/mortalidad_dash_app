# Estructura base de la aplicación Dash para el análisis de mortalidad en Colombia 2019

# --- app.py ---
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from utils.preprocessing import cargar_datos
from components.mapa import generar_mapa
from components.lineas import generar_lineas
from components.barras import generar_barras
from components.pastel import generar_pastel
from components.tabla import generar_tabla
from components.histograma import generar_histograma

# Diccionario global de grupos de edad para filtros y visualizaciones
GRUPOS_EDAD = {
    0: '0-4', 1: '0-4', 2: '5-9', 3: '5-9', 4: '10-14', 5: '10-14',
    6: '15-19', 7: '15-19', 8: '20-24', 9: '20-24', 10: '25-29',
    11: '25-29', 12: '30-34', 13: '30-34', 14: '35-39', 15: '35-39',
    16: '40-44', 17: '40-44', 18: '45-49', 19: '45-49', 20: '50-54',
    21: '50-54', 22: '55-59', 23: '60-64', 24: '65-69', 25: '70-74',
    26: '75-79', 27: '80-84', 28: '85+'
}

from components.apiladas import generar_apiladas


# Inicialización de la aplicación
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Mortalidad Colombia 2019"
server = app.server

# Cargar datos
no_fetal, codigos, divipola = cargar_datos("data/NoFetal2019.xlsx", "data/CodigosDeMuerte.xlsx", "data/Divipola.xlsx")

# Layout de la aplicación
app.layout = dbc.Container([
    html.H1("Análisis de Mortalidad en Colombia - 2019", className="text-center my-4"),

    html.Div([
        "Actividad 4: Aplicación web interactiva para el análisis de mortalidad en Colombia",
        html.Br(),
        "Aplicaciones web analíticas con Python y Dash",
        html.Br(),
        "Andrés Camilo Gutiérrez Escobar",
        html.Br(),
        "2025-1_APLICACIONES I G1",
        html.Br(),
        "Maestría en Inteligencia Artificial",
        html.Br(),
        "19 de mayo de 2025"
    ], style={"textAlign": "left", "marginBottom": "2rem"}),

    # Mapa
    dbc.Row([
        dbc.Col([
            html.H4("Distribución de muertes por departamento", style={"display": "inline-block", "margin-right": "20px"}),
            dcc.Dropdown(
                id="filtro-genero-global",
                options=[
                    {"label": "Todos", "value": "Todos"},
                    {"label": "Hombre", "value": 1},
                    {"label": "Mujer", "value": 2}
                ],
                value="Todos",
                clearable=False,
                style={"width": "200px", "display": "inline-block", "verticalAlign": "middle"}
            ),
            dcc.Interval(id="interval-mapa", interval=1000, n_intervals=0, max_intervals=1, disabled=False),
            dcc.Loading(id="loading-mapa", children=[html.Div(id="output-mapa")], type="circle")
        ], md=12)
    ], className="mb-4"),

    # Líneas (por mes y sexo)
    dbc.Row([
        dbc.Col([
            html.H4("Muertes por mes por sexo"),
            html.Label("Sexo", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id="sexo-lineas-dropdown",
                options=[
                    {"label": "Todos", "value": "Todos"},
                    {"label": "Hombre", "value": 1},
                    {"label": "Mujer", "value": 2}
                ],
                value="Todos",
                clearable=False
            ),

            html.Div(id="lineas-output")
        ], md=6),
        # Top 5 ciudades por homicidios con filtro de departamento
        dbc.Col([
            html.H4("Top 5 ciudades por homicidios"),
            html.Label("Departamento", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id="filtro-depto-barras",
                options=[{"label": "Todos", "value": "Todos"}] + [{"label": d, "value": d} for d in sorted(divipola['DEPARTAMENTO'].dropna().unique())],
                value="Todos",
                clearable=False
            ),
            html.Div(id="barras-output")
        ], md=6)
    ], className="mb-4"),

    # 10 ciudades con menor mortalidad con filtro de departamento
    dbc.Row([
        dbc.Col([
            html.H4("10 ciudades con menor mortalidad"),
            html.Label("Departamento", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id="filtro-depto-pastel",
                options=[{"label": "Todos", "value": "Todos"}] + [{"label": d, "value": d} for d in sorted(divipola['DEPARTAMENTO'].dropna().unique())],
                value="Todos",
                clearable=False
            ),
            html.Div(id="pastel-output")
        ], md=6),
        # Principales causas de muerte con filtro de clasificación
        dbc.Col([
            html.H4("Principales causas de muerte"),
            html.Label("Clasificación", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id="filtro-clasificacion-tabla",
                options=[{"label": "Todos", "value": "Todos"}] + [{"label": c, "value": c} for c in sorted(no_fetal['COD_MUERTE'].dropna().unique())],
                value="Todos",
                clearable=False
            ),
            html.Div(id="tabla-output")
        ], md=6)
    ], className="mb-4"),

    # Grupos de edad y apiladas (sexo por departamento/ciudad)
    dbc.Row([
        dbc.Col([
            html.H4("Muertes por grupos de edad"),
            html.Label("Rango de edad", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id="filtro-edad-histograma",
                # Mostrar el nombre descriptivo del rango de edad
                # Mapeo de ID de grupo a etiqueta real (rango de edad)
                # Usar solo los rangos únicos (sin duplicados)
                options=[{"label": "Todos", "value": "Todos"}] + [
                    {"label": rango, "value": rango}
                    for rango in list(dict.fromkeys(GRUPOS_EDAD.values()))
                ],
                value="Todos",
                clearable=False
            ),
            html.Div(id="histograma-output")
        ], md=6),
        dbc.Col([
            html.H4("Muertes por sexo por departamento"),
            html.Label("Departamento", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id="filtro-depto-apiladas",
                options=[{"label": "Todos", "value": "Todos"}] + [{"label": d, "value": d} for d in sorted(divipola['DEPARTAMENTO'].dropna().unique())],
                value="Todos",
                clearable=False
            ),

            html.Div(id="apiladas-output")
        ], md=6)
    ], className="mb-4"),

], fluid=True)

# Callbacks para los filtros avanzados
from dash.dependencies import Input, Output, State

@app.callback(
    Output("output-mapa", "children"),
    [Input("interval-mapa", "n_intervals"), Input("filtro-genero-global", "value")]
)
def actualizar_mapa(_, genero):
    # El filtro puede ser 1, 2 o 'Todos'. Lo convertimos a 'Hombre', 'Mujer' o 'Total'
    if genero == 1:
        genero_str = 'Hombre'
    elif genero == 2:
        genero_str = 'Mujer'
    else:
        genero_str = 'Total'
    return generar_mapa(no_fetal, divipola, genero=genero_str)


@app.callback(
    Output("lineas-output", "children"),
    [Input("sexo-lineas-dropdown", "value"), Input("filtro-genero-global", "value")]
)
def update_lineas(sexo, genero):
    df = no_fetal
    if genero != "Todos":
        df = df[df["SEXO"] == genero]
    if sexo != "Todos":
        df = df[df["SEXO"] == sexo]
    return generar_lineas(df)

@app.callback(
    Output("barras-output", "children"),
    [Input("filtro-depto-barras", "value"), Input("filtro-genero-global", "value")]
)
def update_barras(depto, genero):
    df = no_fetal
    if genero != "Todos":
        df = df[df["SEXO"] == genero]
    if depto == "Todos":
        return generar_barras(df, divipola)
    else:
        codigos = divipola[divipola["DEPARTAMENTO"] == depto]["COD_DANE"].tolist()
        return generar_barras(df[df["COD_DANE"].isin(codigos)], divipola)

@app.callback(
    Output("pastel-output", "children"),
    [Input("filtro-depto-pastel", "value"), Input("filtro-genero-global", "value")]
)
def update_pastel(depto, genero):
    df = no_fetal
    if genero != "Todos":
        df = df[df["SEXO"] == genero]
    if depto == "Todos":
        return generar_pastel(df, divipola)
    else:
        codigos = divipola[divipola["DEPARTAMENTO"] == depto]["COD_DANE"].tolist()
        return generar_pastel(df[df["COD_DANE"].isin(codigos)], divipola)

@app.callback(
    Output("tabla-output", "children"),
    [Input("filtro-clasificacion-tabla", "value"), Input("filtro-genero-global", "value")]
)
def update_tabla(clasificacion, genero):
    df = no_fetal
    if genero != "Todos":
        df = df[df["SEXO"] == genero]
    if clasificacion == "Todos":
        return generar_tabla(df, codigos)
    else:
        return generar_tabla(df[df["COD_MUERTE"] == clasificacion], codigos)

@app.callback(
    Output("histograma-output", "children"),
    [Input("filtro-edad-histograma", "value"), Input("filtro-genero-global", "value")]
)
def update_histograma(rango, genero):
    df = no_fetal.copy()
    if genero != "Todos":
        df = df[df["SEXO"] == genero]
    # Asegura que la columna de rango esté creada y filtrable
    df["GRUPO_QUINQUENAL"] = df["GRUPO_EDAD1"].map(GRUPOS_EDAD)
    if rango == "Todos":
        return generar_histograma(df)
    else:
        return generar_histograma(df[df["GRUPO_QUINQUENAL"] == rango])


@app.callback(
    Output("apiladas-output", "children"),
    [Input("filtro-depto-apiladas", "value"), Input("filtro-genero-global", "value")]
)
def update_apiladas(depto, genero):
    df = no_fetal.copy()
    # Merge para obtener el nombre del departamento
    if 'DEPARTAMENTO' not in df.columns:
        df = df.merge(divipola[['COD_DANE', 'DEPARTAMENTO']], how='left', left_on='COD_DANE', right_on='COD_DANE')
    if genero != "Todos":
        df = df[df["SEXO"] == genero]
    if depto != "Todos":
        df = df[df["DEPARTAMENTO"] == depto]
    return generar_apiladas(df, divipola)

# Ejecutar app
if __name__ == '__main__':
    app.run_server(debug=True)
