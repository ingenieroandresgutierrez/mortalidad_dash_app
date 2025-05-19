import plotly.express as px
from dash import dcc

def generar_pastel(df_no_fetal, df_divipola):
    df_ciudades = df_no_fetal.groupby('COD_DANE').size().reset_index(name='Muertes')
    df_ciudades['COD_DANE'] = df_ciudades['COD_DANE'].astype(str).str.zfill(5)
    df_ciudades = df_ciudades.merge(df_divipola[['COD_DANE', 'MUNICIPIO']], on='COD_DANE', how='left')
    # Filtrar valores nulos en MUNICIPIO antes de graficar
    df_ciudades = df_ciudades[df_ciudades['MUNICIPIO'].notnull()]
    top10_menor = df_ciudades.sort_values(by='Muertes').head(10)
    fig = px.pie(top10_menor, names='MUNICIPIO', values='Muertes', title="10 Ciudades con Menor Mortalidad", hole=0.4)
    return dcc.Graph(figure=fig)
