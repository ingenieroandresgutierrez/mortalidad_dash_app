import pandas as pd


def cargar_datos(path_no_fetal, path_codigos, path_divipola):
    """
    Carga y limpia los tres archivos base en formato Excel.

    Args:
        path_no_fetal (str): Ruta al archivo de muertes no fetales.
        path_codigos (str): Ruta al archivo de códigos CIE-10.
        path_divipola (str): Ruta al archivo DIVIPOLA.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: (no_fetal, codigos, divipola)
    """
    import os
    import pandas as pd

    try:
        no_fetal = pd.read_excel(path_no_fetal, dtype={'COD_DANE': str})
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo de muertes no fetales: {path_no_fetal}. Verifica la ruta y que el archivo exista.")
    try:
        codigos = pd.read_excel(path_codigos)
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo de códigos CIE-10: {path_codigos}. Verifica la ruta y que el archivo exista.")
    try:
        divipola = pd.read_excel(path_divipola, dtype={'COD_DANE': str})
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo DIVIPOLA: {path_divipola}. Verifica la ruta y que el archivo exista.")

    # Normalización básica
    no_fetal['COD_DANE'] = no_fetal['COD_DANE'].str.zfill(5)
    divipola['COD_DANE'] = divipola['COD_DANE'].str.zfill(5)

    no_fetal['MANERA_MUERTE'] = no_fetal['MANERA_MUERTE'].str.strip().str.title()
    no_fetal['COD_MUERTE'] = no_fetal['COD_MUERTE'].str.upper().str.strip()

    no_fetal['FECHA'] = pd.to_datetime({
        'year': no_fetal['AÑO'],
        'month': no_fetal['MES'],
        'day': 1
    }, errors='coerce')

    return no_fetal, codigos, divipola
