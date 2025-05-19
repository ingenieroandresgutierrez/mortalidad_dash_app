import plotly.express as px

SEXO_MAP = {1: 'Hombre', 2: 'Mujer', 3: 'N/A', '1': 'Hombre', '2': 'Mujer', '3': 'N/A'}
from dash import dcc

import plotly.io as pio
pio.templates.default = "plotly"

def generar_histograma(df_no_fetal):
    grupos = {
        0: '0-4', 1: '0-4', 2: '5-9', 3: '5-9', 4: '10-14', 5: '10-14',
        6: '15-19', 7: '15-19', 8: '20-24', 9: '20-24', 10: '25-29',
        11: '25-29', 12: '30-34', 13: '30-34', 14: '35-39', 15: '35-39',
        16: '40-44', 17: '40-44', 18: '45-49', 19: '45-49', 20: '50-54',
        21: '50-54', 22: '55-59', 23: '60-64', 24: '65-69', 25: '70-74',
        26: '75-79', 27: '80-84', 28: '85+'
    }
    df_copy = df_no_fetal.copy()
    df_copy.loc[:, 'GRUPO_QUINQUENAL'] = df_copy['GRUPO_EDAD1'].map(grupos)
    # Asignar 'Desconocido' a valores fuera del mapeo
    df_copy.loc[:, 'GRUPO_QUINQUENAL'] = df_copy['GRUPO_QUINQUENAL'].fillna('Desconocido')
    # Filtrar valores nulos en SEXO si es necesario
    df_plot = df_copy[df_copy['SEXO'].notnull()].copy()
    # Mapear valores de sexo a 'Hombre' y 'Mujer' para la gráfica
    df_plot = df_plot.copy()
    df_plot['SEXO'] = df_plot['SEXO'].astype('object')  # Fuerza tipo object para strings
    df_plot.loc[:, 'SEXO'] = df_plot['SEXO'].map(SEXO_MAP).fillna(df_plot['SEXO'])
    orden_edades = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85+', 'Desconocido']
    fig = px.histogram(
        df_plot,
        x='GRUPO_QUINQUENAL',
        color='SEXO',
        barmode='group',
        title='Muertes por Rangos de Edad',
        category_orders={"GRUPO_QUINQUENAL": orden_edades}
    )
    fig.update_layout(
        xaxis_title="Grupo de Edad",
        yaxis_title="Cantidad de personas"
    )
    return dcc.Graph(figure=fig)
