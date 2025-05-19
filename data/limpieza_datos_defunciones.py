import pandas as pd
import os

# --- 1. LIMPIEZA DEL ARCHIVO PRINCIPAL: Muertes No Fetales 2019 ---
def limpiar_muertes_no_fetales(filepath, output_path):
    if not os.path.exists(filepath):
        print(f"No se encontró el archivo: {filepath}. Verifica la ruta y que el archivo exista.")
        return
    try:
        df = pd.read_csv(filepath, encoding='utf-8-sig')
        df.rename(columns={'ï»¿COD_DANE': 'COD_DANE', 'AÃ±O': 'AÑO'}, inplace=True)
        df.dropna(how='all', inplace=True)
        df['AÑO'] = pd.to_numeric(df['AÑO'], errors='coerce')
        df['MES'] = pd.to_numeric(df['MES'], errors='coerce')
        df['HORA'] = pd.to_numeric(df['HORA'], errors='coerce')
        df['MINUTOS'] = pd.to_numeric(df['MINUTOS'], errors='coerce')
        df['SEXO'] = df['SEXO'].astype('Int64')
        df['COD_DANE'] = df['COD_DANE'].astype(str).str.zfill(5)
        df['MANERA_MUERTE'] = df['MANERA_MUERTE'].str.strip().str.title()
        df['COD_MUERTE'] = df['COD_MUERTE'].str.strip().str.upper()
        df = df[df['COD_MUERTE'].notnull()]
        df['FECHA'] = pd.to_datetime({
            'year': df['AÑO'],
            'month': df['MES'],
            'day': 1
        }, errors='coerce')
        df.drop_duplicates(inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
    except pd.errors.EmptyDataError:
        print(f"El archivo {filepath} está vacío.")
    except pd.errors.ParserError:
        print(f"Error al parsear el archivo {filepath}. Verifica que el archivo esté en el formato correcto.")

# --- 2. LIMPIEZA DEL ARCHIVO DE CÓDIGOS DE MUERTE ---
def limpiar_codigos_muerte(filepath, output_path):
    import os
    import pandas as pd
    if not os.path.exists(filepath):
        print(f"No se encontró el archivo: {filepath}. Verifica la ruta y que el archivo exista.")
        return
    df = pd.read_csv(filepath, encoding='utf-8-sig', sep=',')
    df = df.dropna(how='all')
    if df.shape[1] == 1:
        df = df.iloc[:, 0].str.split(';', expand=True)
    df.columns = [
        'Capitulo',
        'Nombre Capitulo',
        'Codigo_CIE10_3',
        'Descripcion_3',
        'Codigo_CIE10_4',
        'Descripcion_4'
    ]
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype(str).str.strip()
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

# --- 3. LIMPIEZA DEL ARCHIVO DIVIPOLA ---
def limpiar_divipola(filepath, output_path):
    import os
    import pandas as pd
    if not os.path.exists(filepath):
        print(f"No se encontró el archivo: {filepath}. Verifica la ruta y que el archivo exista.")
        return
    df = pd.read_csv(filepath, encoding='utf-8-sig', sep=',')
    df['COD_DANE'] = df['COD_DANE'].astype(str).str.zfill(5)
    df['MUNICIPIO'] = df['MUNICIPIO'].str.strip().str.title()
    df['DEPARTAMENTO'] = df['DEPARTAMENTO'].str.strip().str.title()
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

# --- Ejecutar Limpiezas ---
limpiar_muertes_no_fetales("Muertes_No_Fetales_2019_Corregido.csv", "Muertes_No_Fetales_2019_Limpio.csv")
limpiar_codigos_muerte("Codigos_Muerte_Corregido.csv", "Codigos_Muerte_Limpio.csv")
limpiar_divipola("Divipola_Corregido.csv", "Divipola_Limpio.csv")
