# Ruteador Perú

Una aplicación de escritorio que encuentra la ruta más corta entre dos regiones de Perú utilizando el algoritmo de Dijkstra y la muestra en un mapa interactivo.

## Características

- Interfaz gráfica intuitiva desarrollada con PyQt5
- Visualización de rutas en mapa usando matplotlib
- Cálculo de la ruta más corta entre regiones utilizando el algoritmo de Dijkstra
- Tabla de resultados con secuencia de regiones y distancias
- Visualización completa del grafo de regiones

## Requisitos

- Python 3.8 o superior
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clone o descargue este repositorio
2. Instale las dependencias necesarias:

### Opción 1: Usando pip
```bash
pip install -r requirements.txt
```

### Opción 2: Usando Anaconda (recomendado)
Si tiene problemas con la instalación de PyQt5, use Anaconda:
```bash
conda install -c anaconda pyqt matplotlib pandas networkx
conda install -c conda-forge geopandas folium shapely
```

## Uso

Para iniciar la aplicación, tiene varias opciones:

### Opción 1: Scripts de ejecución automática (Windows)
Utilice uno de los siguientes scripts incluidos:

- **ejecutar.bat**: Script de ejecución general
- **ejecutar_con_conda.bat**: Script específico para entornos Anaconda
- **ejecutar.ps1**: Script PowerShell avanzado para diagnósticos

### Opción 2: Ejecución directa por línea de comandos
```bash
python main.py
```

Si la ejecución directa falla, puede probar con la versión alternativa:
```bash
python main_pyside2.py
```

### Cómo utilizar:

1. Seleccione una región de origen en el primer menú desplegable
2. Seleccione una región de destino en el segundo menú desplegable
3. Presione el botón "Calcular Ruta"
4. La ruta más corta se mostrará en el mapa y los detalles aparecerán en la tabla lateral

## Estructura del proyecto

- `main.py`: Punto de entrada de la aplicación, inicializa la GUI y conecta los componentes
- `data_loader.py`: Funciones para cargar los datos CSV y extraer información para el grafo
- `graph_module.py`: Construcción del grafo y algoritmo de ruta más corta
- `map_module.py`: Visualización del mapa y rutas usando matplotlib
- `utils.py`: Funciones auxiliares varias
- `data/`: Directorio que contiene los archivos CSV de datos de las regiones

## Datos

La aplicación utiliza dos archivos CSV:
- `regiones.csv`: Contiene los nombres y coordenadas de las 25 regiones del Perú
- `distancias_regionales_peru_enriquecido.csv`: Contiene las distancias entre regiones conectadas
