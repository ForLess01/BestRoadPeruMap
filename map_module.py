import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx
import numpy as np
import matplotlib.image as mpimg
import os
import matplotlib.transforms as transforms

class MapVisualizer:
    def __init__(self, data_loader, graph_builder):
        """
        Inicializa el visualizador de mapas
        
        Args:
            data_loader: Instancia de DataLoader con los datos cargados
            graph_builder: Instancia de GraphBuilder con el grafo construido
        """
        self.data_loader = data_loader
        self.graph_builder = graph_builder
        self.figure = plt.figure(figsize=(10, 8))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        
    def draw_base_map(self):
        """
        Dibuja el mapa base con todas las regiones
        """
        self.ax.clear()
        
        # Cargar y mostrar la imagen de fondo
        background_img = mpimg.imread(os.path.join('resources', 'PeruMap.png'))
        t = transforms.Affine2D().rotate_deg(0).scale(1) + self.ax.transData
        self.ax.imshow(background_img, extent=[-82.1, -68.5, -19.3, 1.0], transform=t, zorder=0, alpha=0.3)
        self.ax.set_xlim(-82.1, -68.5)
        self.ax.set_ylim(-19.3, 1.0)
        
        self.data_loader.generate_dummy_peru_map(self.ax)
        
        # Obtener coordenadas de las regiones
        region_coords = self.data_loader.get_region_coordinates()
        
        # Dibujar todas las aristas del grafo
        self._draw_all_edges(region_coords, linewidth=2, color='blue',alpha=0.4)
        
        self.canvas.draw()
        return self.canvas
    
    def _draw_all_edges(self, region_coords, **kwargs):
        """
        Dibuja todas las aristas del grafo
        """
        graph = self.graph_builder.get_graph()
        for u, v, data in graph.edges(data=True):
            if u in region_coords and v in region_coords:
                x1, y1 = region_coords[u][1], region_coords[u][0]  # Invertir latitud y longitud
                x2, y2 = region_coords[v][1], region_coords[v][0]  # Invertir latitud y longitud
                self.ax.plot([x1, x2], [y1, y2], **kwargs)
    
    def highlight_path(self, path):
        """
        Resalta una ruta específica en el mapa
        
        Args:
            path: Lista de regiones que forman la ruta
        """
        if not path:
            return
            
        region_coords = self.data_loader.get_region_coordinates()
        
        # Dibujar las aristas de la ruta con un color destacado
        for i in range(len(path) - 1):
            start = path[i]
            end = path[i + 1]
            
            if start in region_coords and end in region_coords:
                x1, y1 = region_coords[start][1], region_coords[start][0]  # Invertir latitud y longitud
                x2, y2 = region_coords[end][1], region_coords[end][0]  # Invertir latitud y longitud
                self.ax.plot([x1, x2], [y1, y2], linewidth=2.5, color='red', zorder=4)
        
        # Destacar los nodos de la ruta
        for region in path:
            if region in region_coords:
                x, y = region_coords[region][1], region_coords[region][0]  # Invertir latitud y longitud
                self.ax.scatter(x, y, color='red', s=100, zorder=5, edgecolors='black')
        
        self.canvas.draw()
    
    def visualize_route(self, origin, destination):
        """
        Visualiza la ruta más corta entre dos regiones
        
        Args:
            origin: Región de origen
            destination: Región de destino
            
        Returns:
            path: Lista de regiones que forman la ruta
            total_distance: Distancia total de la ruta
            distances: Lista de distancias parciales
        """
        # Calcular la ruta más corta
        path, total_distance, distances = self.graph_builder.calculate_shortest_path(origin, destination)
        
        # Dibujar el mapa base
        self.draw_base_map()
        
        # Resaltar la ruta si existe
        if path:
            self.highlight_path(path)
        
        return path, total_distance, distances
    
    def get_canvas(self):
        """
        Devuelve el canvas de matplotlib para integrarlo en PyQt
        """
        return self.canvas
