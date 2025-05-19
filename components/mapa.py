import plotly.express as px
from dash import dcc

import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon

def extraer_centroides_departamentos(geojson_path):
    """
    Extrae los centroides (lat, lon) de cada departamento a partir de un archivo GeoJSON.
    Retorna un DataFrame con columnas: DEPARTAMENTO, LATITUD, LONGITUD
    """
    gdf = gpd.read_file(geojson_path)
    # Asegura nombre consistente
    gdf['DEPARTAMENTO'] = gdf['NOMBRE_DPT'].str.upper().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    # Reproyecta a EPSG:3857 para calcular centroides correctamente
    gdf_proj = gdf.to_crs(epsg=3857)
    gdf['centroid'] = gdf_proj.geometry.centroid.to_crs(epsg=4326)
    gdf['LATITUD'] = gdf['centroid'].y
    gdf['LONGITUD'] = gdf['centroid'].x
    return gdf[['DEPARTAMENTO', 'LATITUD', 'LONGITUD']]

def generar_mapa(df_no_fetal, df_divipola, genero='Total'):
    from dash import html
    import pandas as pd
    import os

    # Si faltan lat/lon en divipola, los genera automáticamente desde el geojson
    if not {'LATITUD', 'LONGITUD'}.issubset(df_divipola.columns):
        geojson_path = os.path.join(os.path.dirname(__file__), '../data/colombia.geo.json')
        if os.path.exists(geojson_path):
            df_centroides = extraer_centroides_departamentos(geojson_path)
            # Normaliza nombres para merge robusto
            df_divipola['DEPARTAMENTO_NORM'] = df_divipola['DEPARTAMENTO'].str.upper().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
            df_divipola = df_divipola.merge(df_centroides, left_on='DEPARTAMENTO_NORM', right_on='DEPARTAMENTO', how='left')
            df_divipola.drop(['DEPARTAMENTO_NORM', 'DEPARTAMENTO_y'], axis=1, inplace=True, errors='ignore')
            df_divipola.rename(columns={'DEPARTAMENTO_x': 'DEPARTAMENTO'}, inplace=True)
        else:
            return html.Div([
                html.H4("No se pueden mostrar los marcadores: faltan columnas de latitud/longitud en divipola y no se encontró el archivo GeoJSON.")
            ])

    # Verifica que divipola tenga lat/lon y cod_departamento
    if not {'LATITUD', 'LONGITUD', 'COD_DEPARTAMENTO', 'DEPARTAMENTO'}.issubset(df_divipola.columns):
        return html.Div([
            html.H4("No se pueden mostrar los marcadores: faltan columnas de latitud/longitud en divipola.")
        ])

    df = df_no_fetal.copy()
    # Filtro por género si corresponde
    if genero in ['Hombre', 'Mujer']:
        # Normaliza columna SEXO si es numérica
        if df['SEXO'].dtype in ['int64', 'float64'] or df['SEXO'].dtype == 'int':
            df['SEXO'] = df['SEXO'].astype(str)
        # Mapeo de valores posibles
        sexo_map = {'Hombre': ['1', 1, 'Hombre'], 'Mujer': ['2', 2, 'Mujer']}
        df = df[df['SEXO'].isin(sexo_map[genero])]
    # Si es Total, no se filtra

    if 'COD_DEPARTAMENTO' not in df.columns:
        if 'COD_DANE' in df.columns and 'COD_DANE' in df_divipola.columns:
            df = df.merge(df_divipola[['COD_DANE', 'COD_DEPARTAMENTO']], how='left', on='COD_DANE')
    if 'COD_DEPARTAMENTO' not in df.columns:
        return html.Div([
            html.H4("No se encontró la columna COD_DEPARTAMENTO en los datos."),
        ])
    if df.empty:
        return html.Div([
            html.H4("No hay datos para mostrar en el mapa con los filtros seleccionados.")
        ])

    df_grouped = df.groupby("COD_DEPARTAMENTO").size().reset_index(name="Total")
    # Merge con lat/lon y nombre departamento
    df_grouped = df_grouped.merge(df_divipola[['COD_DEPARTAMENTO', 'DEPARTAMENTO', 'LATITUD', 'LONGITUD']].drop_duplicates(), on='COD_DEPARTAMENTO', how='left')
    df_grouped = df_grouped[df_grouped['LATITUD'].notnull() & df_grouped['LONGITUD'].notnull()]

    # --- Sumar las muertes de Bogotá a Cundinamarca y mostrar círculo de Bogotá ---
    # Bogotá: COD_DEPARTAMENTO = 11, Cundinamarca: COD_DEPARTAMENTO = 25
    bogota_cod = 11
    cundinamarca_cod = 25

    # Fuerza tipos correctos
    df_grouped['COD_DEPARTAMENTO'] = pd.to_numeric(df_grouped['COD_DEPARTAMENTO'], errors='coerce').astype('Int64')
    df_divipola['COD_DEPARTAMENTO'] = pd.to_numeric(df_divipola['COD_DEPARTAMENTO'], errors='coerce').astype('Int64')

    existe_bogota = (df_grouped['COD_DEPARTAMENTO'] == bogota_cod).any()
    existe_cundinamarca = (df_grouped['COD_DEPARTAMENTO'] == cundinamarca_cod).any()

    # Sumar las muertes de Bogotá a Cundinamarca y eliminar Bogotá del DataFrame para que NO se muestre el círculo
    fila_bogota = df_divipola[df_divipola['COD_DEPARTAMENTO'] == bogota_cod]
    tiene_coord_bogota = not fila_bogota.empty and pd.notnull(fila_bogota.iloc[0]['LATITUD']) and pd.notnull(fila_bogota.iloc[0]['LONGITUD'])

    # Sumar las muertes de Bogotá a Cundinamarca y eliminar Bogotá del DataFrame para que NO se muestre el círculo
    if existe_bogota and existe_cundinamarca:
        muertes_bogota = df_grouped.loc[df_grouped['COD_DEPARTAMENTO'] == bogota_cod, 'Total'].sum()
        df_grouped.loc[df_grouped['COD_DEPARTAMENTO'] == cundinamarca_cod, 'Total'] += muertes_bogota
        # Eliminar Bogotá del DataFrame para que no se grafique
        df_grouped = df_grouped[df_grouped['COD_DEPARTAMENTO'] != bogota_cod]
    elif existe_cundinamarca and not existe_bogota:
        # Si Bogotá no está en df_grouped, no se agrega círculo ni suma
        pass
    # Si no existe Cundinamarca, no se hace nada especial

    # Si no existe Cundinamarca, no se hace nada especial
    # --------------------------------------------------------------------------

    if df_grouped.empty:
        return html.Div([
            html.H4("No hay coordenadas disponibles para mostrar en el mapa.")
        ])

    # Centrar el mapa en Colombia
    center_lat = 4.5709
    center_lon = -74.2973
    api_key = "AIzaSyByB_U2H-NJCGXKB7W0mO9GGfa5yeigwls"

    # Construir los marcadores y círculos proporcionales a la cantidad de muertes
    total_min = df_grouped['Total'].min()
    total_max = df_grouped['Total'].max()
    # Evita radio 0
    def scale_radius(value, min_r=20000, max_r=130000):
        if total_max == total_min:
            return (min_r + max_r) / 2
        return min_r + (max_r - min_r) * (value - total_min) / (total_max - total_min)

    markers_js = ""
    for _, row in df_grouped.iterrows():
        departamento = row['DEPARTAMENTO'].replace("'", " ")
        total = int(row['Total'])
        lat = row['LATITUD']
        lon = row['LONGITUD']
        radius = int(scale_radius(total))
        # Círculo y listener encapsulados para evitar bug de referencias
        markers_js += f'''
        (function() {{
            var circle = new google.maps.Circle({{
                strokeColor: '#FF0000',
                strokeOpacity: 0.7,
                strokeWeight: 2,
                fillColor: '#FF0000',
                fillOpacity: 0.25,
                map: map,
                center: {{lat: {lat}, lng: {lon}}},
                radius: {radius}
            }});
            var marker = new google.maps.Marker({{
                position: {{lat: {lat}, lng: {lon}}},
                map: map,
                title: '{departamento} ({total} muertes)',
                icon: {{}}, // invisible marker to keep InfoWindow
                visible: false
            }});
            var infowindow = new google.maps.InfoWindow({{
                content: '<strong>{departamento}</strong><br>Total muertes: <b>{total}</b>'
            }});
            circle.addListener('click', function() {{
                infowindow.setPosition(circle.getCenter());
                infowindow.open(map);
            }});
        }})();
        '''

    # HTML para el mapa con leyenda
    html_map = f"""
    <div style='margin-bottom:10px; text-align:center;'>
        <b>Visualización de la distribución total de muertes por departamento en Colombia para el año 2019.</b><br>
        <span style='color:#555;'>Haz clic en cada círculo para ver el total de muertes en ese departamento. El tamaño del círculo es proporcional a la cantidad de muertes.</span>
    </div>
    <div id='map' style='height:500px;width:100%'></div>
    <script src='https://maps.googleapis.com/maps/api/js?key={api_key}'></script>
    <script>
      function initMap() {{
        var center = {{lat: {center_lat}, lng: {center_lon}}};
        var map = new google.maps.Map(document.getElementById('map'), {{
          zoom: 5,
          center: center
        }});
        {markers_js}
      }}
      window.initMap = initMap;
      if (window.google && window.google.maps) {{ initMap(); }}
      else {{
        var script = document.createElement('script');
        script.src = 'https://maps.googleapis.com/maps/api/js?key={api_key}&callback=initMap';
        document.head.appendChild(script);
      }}
    </script>
    """
    return html.Iframe(srcDoc=html_map, width="100%", height="520", style={"border": "none"})

