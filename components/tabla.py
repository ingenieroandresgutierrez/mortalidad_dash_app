from dash import dash_table

def generar_tabla(df_no_fetal, df_codigos):
    df = df_no_fetal.groupby("COD_MUERTE").size().reset_index(name="Muertes")
    # Verifica que las columnas requeridas existan
    if 'Codigo_CIE10_4' not in df_codigos.columns or 'Descripcion_4' not in df_codigos.columns:
        return dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in ['Código', 'Descripción', 'Muertes']],
            data=[{"Código": "Error", "Descripción": "Columnas faltantes en df_codigos", "Muertes": 0}],
            page_size=10
        )
    df = df.merge(df_codigos, left_on="COD_MUERTE", right_on="Codigo_CIE10_4", how="left")
    # Filtra valores nulos en Descripcion_4 antes de mostrar la tabla
    df = df[df['Descripcion_4'].notnull()]
    df = df[['COD_MUERTE', 'Descripcion_4', 'Muertes']].sort_values(by='Muertes', ascending=False).head(10)
    df.columns = ['Código', 'Descripción', 'Muertes']
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        sort_action="native",
        filter_action="native"
    )
