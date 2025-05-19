import plotly.express as px
from dash import dcc

def generar_apiladas(df_no_fetal, df_divipola):
    df = df_no_fetal.copy()
    df['SEXO'] = df['SEXO'].map({1: 'Hombre', 2: 'Mujer'})
    df_grouped = df.groupby(['COD_DEPARTAMENTO', 'SEXO']).size().reset_index(name='Muertes')
    # Asegura que ambas columnas sean string y tengan el mismo formato
    df_grouped['COD_DEPARTAMENTO'] = df_grouped['COD_DEPARTAMENTO'].astype(str).str.zfill(2)
    df_divipola = df_divipola.copy()
    if 'COD_DEPARTAMENTO' in df_divipola.columns:
        df_divipola['COD_DEPARTAMENTO'] = df_divipola['COD_DEPARTAMENTO'].astype(str).str.zfill(2)
    df_grouped = df_grouped.merge(df_divipola[['COD_DEPARTAMENTO', 'DEPARTAMENTO']].drop_duplicates(), on='COD_DEPARTAMENTO', how='left')
    fig = px.bar(df_grouped, x='DEPARTAMENTO', y='Muertes', color='SEXO', barmode='stack',
                 title='Muertes por Sexo en Cada Departamento')
    return dcc.Graph(figure=fig)
