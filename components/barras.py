import plotly.express as px
from dash import dcc

def generar_barras(df_no_fetal, df_divipola):
    from dash import html
    import plotly.express as px
    import pandas as pd
    
    codigos_violentos = ['X95', 'X93', 'X99']
    # Validar columnas necesarias
    required_columns = {'COD_MUERTE', 'COD_DANE'}
    if not required_columns.issubset(df_no_fetal.columns):
        print(f"[ERROR] Faltan columnas en df_no_fetal: {df_no_fetal.columns.tolist()}")
        return html.Div([
            html.H4("No se pueden calcular las barras: faltan columnas en los datos de muertes."),
            html.P(f"Columnas presentes: {', '.join(df_no_fetal.columns)}")
        ])
    if 'MUNICIPIO' not in df_divipola.columns:
        print(f"[ERROR] Falta la columna MUNICIPIO en df_divipola: {df_divipola.columns.tolist()}")
        return html.Div([
            html.H4("No se pueden calcular las barras: falta la columna MUNICIPIO en divipola."),
            html.P(f"Columnas presentes: {', '.join(df_divipola.columns)}")
        ])
    # Filtrar valores nulos antes de aplicar .str.startswith
    df_no_fetal = df_no_fetal[df_no_fetal['COD_MUERTE'].notnull()]
    if df_no_fetal.empty:
        print("[ERROR] df_no_fetal está vacío tras filtrar nulos en COD_MUERTE.")
        return html.Div([
            html.H4("No hay datos de muertes violentas para mostrar en las barras.")
        ])
    df_filtrado = df_no_fetal[df_no_fetal['COD_MUERTE'].str.startswith(tuple(codigos_violentos))]
    if df_filtrado.empty:
        print("[ERROR] df_filtrado está vacío tras filtrar por códigos violentos.")
        return html.Div([
            html.H4("No hay muertes violentas registradas para mostrar en las barras.")
        ])
    df_ciudades = df_filtrado.groupby('COD_DANE').size().reset_index(name='Muertes')
    df_ciudades['COD_DANE'] = df_ciudades['COD_DANE'].astype(str).str.zfill(5)
    df_ciudades = df_ciudades.merge(df_divipola[['COD_DANE', 'MUNICIPIO']], on='COD_DANE', how='left')
    df_ciudades = df_ciudades[df_ciudades['MUNICIPIO'].notnull()]
    if df_ciudades.empty:
        print("[ERROR] df_ciudades está vacío tras el merge con MUNICIPIO.")
        return html.Div([
            html.H4("No hay ciudades con muertes violentas registradas para mostrar.")
        ])
    top5 = df_ciudades.sort_values(by='Muertes', ascending=False).head(5)
    print("[DEBUG] top5 ciudades para barras:")
    print(top5)
    if top5.empty or not {'MUNICIPIO', 'Muertes'}.issubset(top5.columns):
        print("[ERROR] top5 vacío o faltan columnas para graficar.")
        return html.Div([
            html.H4("No hay datos suficientes para mostrar la gráfica de barras.")
        ])
    try:
        fig = px.bar(top5, x='MUNICIPIO', y='Muertes', title="Top 5 Ciudades más Violentas por Homicidio", template="plotly")
        return dcc.Graph(figure=fig)
    except Exception as e:
        print(f"[ERROR] Error al crear la gráfica de barras: {e}")
        return html.Div([
            html.H4("Error al generar la gráfica de barras."),
            html.P(str(e))
        ])
