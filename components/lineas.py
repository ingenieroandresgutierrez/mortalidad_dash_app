import plotly.express as px
from dash import dcc

def generar_lineas(df_no_fetal, tipo="Natural", sexo="Todos"):
    df = df_no_fetal.copy()
    # Normaliza el campo SEXO para comparar correctamente
    if 'SEXO' in df.columns:
        df = df[df['SEXO'].notnull()]
        if isinstance(sexo, str) and sexo != "Todos":
            # Si el usuario pasa "Hombre" o "Mujer" en vez de 1/2
            sexo_map = {'Hombre': 1, 'Mujer': 2, '1': 1, '2': 2}
            sexo_val = sexo_map.get(str(sexo), sexo)
            df = df[df["SEXO"] == sexo_val]
        elif sexo != "Todos":
            df = df[df["SEXO"] == sexo]
    df = df[df["MANERA_MUERTE"] == tipo]
    # Filtra valores nulos en MES para evitar errores en el gráfico
    df = df[df["MES"].notnull()]
    df_mes = df.groupby("MES").size().reset_index(name="Muertes").sort_values("MES")
    fig = px.line(df_mes, x="MES", y="Muertes", markers=True,
                  title=f"Muertes por Mes - {tipo} ({'Ambos' if sexo == 'Todos' else 'Hombre' if sexo==1 else 'Mujer'})",
                  labels={"MES": "Mes", "Muertes": "Número de muertes"})
    return dcc.Graph(figure=fig)
