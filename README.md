# Aplicación Web Interactiva para el Análisis de Mortalidad en Colombia (2019)

**Autor:** Andrés Camilo Gutiérrez Escobar  
**Curso:** Aplicaciones -> Aplicaciones web analíticas con Python y Dash  
**Fecha:** 19 de mayo de 2025

## Descripción General

Este proyecto es una aplicación web interactiva desarrollada con **Dash** y **Plotly** para analizar la mortalidad en Colombia durante el año 2019. Permite visualizar, filtrar y explorar datos de muertes a nivel nacional, departamental y municipal, utilizando diversos gráficos, mapas y tablas dinámicas.

---

## Estructura del Proyecto

```
mortalidad_dash_app/
│
├── app.py
├── requirements.txt
├── Procfile
├── README.md
│
├── components/
│   ├── apiladas.py
│   ├── barras.py
│   ├── histograma.py
│   ├── lineas.py
│   ├── mapa.py
│   ├── pastel.py
│   └── tabla.py
│
├── utils/
│   └── preprocessing.py
│
├── data/
│   ├── CodigosDeMuerte.xlsx
│   ├── Divipola.xlsx
│   ├── NoFetal2019.xlsx
│   ├── PoblacionDANE.xlsx
│   ├── colombia.geo.json
│   └── limpieza_datos_defunciones.py
└──
```

---

## Archivos Principales

### 1. `app.py`
- **Propósito:** Archivo principal de la aplicación Dash.
- **Responsabilidades:**
  - Inicializa la app y el servidor.
  - Carga los datos base (muertes, códigos CIE-10, DIVIPOLA).
  - Define el layout: títulos, filtros, y disposición de todos los gráficos y tablas.
  - Implementa todos los callbacks de Dash para la interactividad (mapa, líneas, barras, pastel, tabla, histograma, apiladas).
  - Gestiona la lógica de filtrado global por género y otros filtros por departamento, clasificación, edad, etc.
  - Es el punto de entrada para ejecutar la aplicación.

### 2. `requirements.txt`
- **Propósito:** Lista de dependencias necesarias para ejecutar el proyecto.
- **Contenido típico:** dash, dash-bootstrap-components, pandas, plotly, geopandas, shapely, openpyxl, etc.

---

## Carpeta `components/` (Visualizaciones y Tablas)

Cada archivo implementa un tipo de visualización o tabla específica:

- **`mapa.py`**
  - Genera el mapa interactivo de Colombia usando Google Maps vía HTML+JS.
  - Dibuja círculos proporcionales a la cantidad de muertes por departamento.
  - Permite filtrar por género.
  - Incluye lógica para extraer centroides de departamentos desde un GeoJSON si faltan coordenadas.
  - Maneja errores de datos y muestra mensajes amigables si faltan columnas o datos.

- **`barras.py`**
  - Crea un gráfico de barras con el top 5 de ciudades más violentas por homicidio.
  - Filtra y valida los datos de muertes violentas y realiza joins con la información de municipios.

- **`apiladas.py`**
  - Genera un gráfico de barras apiladas mostrando muertes por sexo en cada departamento.
  - Realiza agrupación y merge con los nombres de departamento.

- **`histograma.py`**
  - Construye un histograma de muertes por grupo de edad y sexo.
  - Permite visualizar la distribución etaria y filtrar por género.

- **`lineas.py`**
  - Produce una gráfica de líneas de muertes por mes, permitiendo filtrar por tipo de muerte y sexo.

- **`pastel.py`**
  - Muestra un gráfico de pastel (pie) con las 10 ciudades con menor mortalidad.

- **`tabla.py`**
  - Presenta una tabla interactiva con las principales causas de muerte, mostrando código, descripción y número de muertes.
  - Permite orden y filtrado nativo en la tabla.

---

## Carpeta `utils/` (Utilidades y Preprocesamiento)

- **`preprocessing.py`**
  - Define la función `cargar_datos` que carga y limpia los archivos base de Excel.
  - Realiza normalización de columnas, conversión de tipos y manejo de fechas.
  - Devuelve los DataFrames listos para ser usados por la app.

---

## Carpeta `data/` (Datos y Scripts de Limpieza)

- **Archivos `.xlsx`**
  - `NoFetal2019.xlsx`: Datos principales de muertes no fetales en Colombia 2019.
  - `CodigosDeMuerte.xlsx`: Códigos CIE-10 y descripciones de causas de muerte.
  - `Divipola.xlsx`: Información geográfica y administrativa de municipios y departamentos.
  - `PoblacionDANE.xlsx`: Datos poblacionales.

- **`colombia.geo.json`**
  - GeoJSON con los polígonos de los departamentos de Colombia, usado para calcular centroides y coordenadas.

- **`limpieza_datos_defunciones.py`**
  - Script de preprocesamiento para limpiar y transformar los archivos de datos originales (CSV) a un formato adecuado para análisis.
  - Incluye funciones para limpiar el archivo de muertes, códigos de muerte y DIVIPOLA, y guardar los resultados en nuevos archivos.

---

## Ejecución Local

1. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verifica que los archivos de datos estén en la carpeta `data/`.**

3. **Ejecuta la aplicación:**
   ```bash
   python app.py
   ```

4. **Abre tu navegador en:**  
   - [http://localhost:8050]

5. **Para ver la prueba de funcionamiento en tiempo real, ingresa al siguiente link:**  
   [https://southern-idea-452214-h7.ue.r.appspot.com/](https://southern-idea-452214-h7.ue.r.appspot.com/)

   Implementada en Google Cloud - App Engine (Plataforma de apps administrada)

---

## Notas Técnicas

- El mapa se implemetó con API de Google Maps válida.
- El sistema es robusto ante datos faltantes: muestra mensajes claros si faltan columnas o archivos.
- El layout es completamente responsivo gracias a Dash Bootstrap Components.
- El filtrado por género, edad, departamento y clasificación es dinámico y afecta a todas las visualizaciones correspondientes.

---

## Créditos y Licencia

Desarrollado para la Maestría en Inteligencia Artificial
Universidad de La Salle, 2025-1.  
Uso académico y educativo.


Esta aplicación web interactiva permite explorar los datos de mortalidad no fetal en Colombia durante el año 2019 a través de múltiples visualizaciones.

## Estructura del Proyecto

```
mortalidad_dash_app/
├── app.py
├── assets/
├── components/
│   ├── mapa.py
│   ├── lineas.py
│   ├── barras.py
│   ├── pastel.py
│   ├── tabla.py
│   ├── histograma.py
│   └── apiladas.py
├── data/
│   ├── NoFetal2019.xlsx
│   ├── CodigosDeMuerte.xlsx
│   └── Divipola.xlsx
├── utils/
│   └── preprocessing.py
├── requirements.txt
├── Procfile
└── README.md
```

## Ejecución Local

1. Clona este repositorio.
2. Instala los requerimientos:

```bash
pip install -r requirements.txt
```

3. Ejecuta la app:

```bash
python app.py
```

4. Abre tu navegador en `http://127.0.0.1:8050`

## Despliegue en Render o Railway

### Render

1. Crea una nueva aplicación web.
2. Conecta tu repositorio.
3. Añade un `build command` (opcional): `pip install -r requirements.txt`
4. Añade un `start command`: `python app.py`

### Railway

1. Inicia un nuevo proyecto.
2. Sube el repositorio o conecta GitHub.
3. Añade variables si es necesario.
4. Establece el comando de inicio: `python app.py`

---
