# Arquitectura de Ruteador Perú

```
+--------------------+     +--------------------+     +--------------------+
|    data_loader.py  |     |   graph_module.py  |     |   map_module.py    |
|                    |     |                    |     |                    |
|  - Carga CSV datos |<--->|  - Construye grafo |<--->| - Visualiza mapa   |
|  - Extrae regiones |     |  - Ejecuta Dijkstra|     | - Dibuja ruta      |
|  - Gestiona coords |     |  - Calcula ruta    |     | - Genera gráficos  |
+--------------------+     +--------------------+     +--------------------+
          ^                         ^                         ^
          |                         |                         |
          v                         v                         v
+-----------------------------------------------------------------------+
|                             main.py                                    |
|                                                                       |
| - Inicializa componentes                                              |
| - Crea interfaz gráfica con PyQt5/PySide2                             |
| - Conecta eventos                                                     |
| - Gestiona la lógica de la aplicación                                 |
+-----------------------------------------------------------------------+
          ^
          |
          v
+--------------------+
|      utils.py      |
|                    |
| - Funciones de UI  |
| - Manejo de errores|
| - Formateo de datos|
+--------------------+
```

## Flujo de trabajo

1. **Inicialización**:
   - `main.py` crea instancias de los componentes principales
   - `data_loader.py` carga datos de regiones y distancias
   - `graph_module.py` construye el grafo inicial

2. **Interacción del usuario**:
   - Usuario selecciona origen y destino
   - Al hacer clic en "Calcular Ruta":
     - `graph_module.py` ejecuta algoritmo de Dijkstra
     - `map_module.py` visualiza la ruta en el mapa
     - `main.py` actualiza la tabla de resultados

3. **Visualización**:
   - `map_module.py` dibuja el mapa base con matplotlib
   - Superpone el grafo completo en color gris
   - Resalta la ruta óptima en rojo

## Compatibilidad

El proyecto se diseñó para soportar diferentes entornos:
- Interfaz principal con **PyQt5**
- Alternativa con **PySide2**
- Scripts de ejecución para distintos entornos
- Manejo de errores y fallbacks automáticos
