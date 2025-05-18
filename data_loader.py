import pandas as pd
import os
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class DataLoader:
    def __init__(self):
        self.regiones_df = None
        self.distancias_df = None
        self.geo_data = None
        
    def load_regiones(self, file_path=None):
        """
        Carga el archivo CSV de regiones
        """
        if file_path is None:
            file_path = os.path.join('data', 'regiones.csv')
        
        self.regiones_df = pd.read_csv(file_path)
        return self.regiones_df
    
    def load_distancias(self, file_path=None):
        """
        Carga el archivo CSV de distancias entre regiones
        """
        if file_path is None:
            file_path = os.path.join('data', 'distancias_regionales_peru_enriquecido.csv')
        
        self.distancias_df = pd.read_csv(file_path)
        return self.distancias_df
    
    def get_region_names(self):
        """
        Obtiene la lista de nombres de todas las regiones
        """
        if self.regiones_df is None:
            self.load_regiones()
        
        return sorted(self.regiones_df['region'].unique())
    
    def get_region_coordinates(self):
        """
        Retorna un diccionario con las coordenadas de cada región
        """
        if self.regiones_df is None:
            self.load_regiones()
        
        coords = {}
        for _, row in self.regiones_df.iterrows():
            coords[row['region']] = (row['latitude'], row['longitude'])
        
        return coords
    
    def create_peru_gdf(self):
        """
        Crea un GeoDataFrame para visualizar el mapa de Perú
        """
        if self.regiones_df is None:
            self.load_regiones()
        
        # Crear geometría con las coordenadas
        geometry = [Point(xy) for xy in zip(self.regiones_df['longitude'], self.regiones_df['latitude'])]
        
        # Crear GeoDataFrame
        gdf = gpd.GeoDataFrame(self.regiones_df, geometry=geometry)
        
        # Establecer sistema de coordenadas (WGS 84)
        gdf.crs = "EPSG:4326"
        
        self.geo_data = gdf
        return gdf
    
    def get_edges_for_graph(self):
        """
        Obtiene las aristas para construir el grafo a partir del archivo de distancias.
        Asegura que el grafo sea realmente no dirigido (ambos sentidos).
        """
        if self.distancias_df is None:
            self.load_distancias()
        
        edges = set()
        for _, row in self.distancias_df.iterrows():
            a = row['region_origen']
            b = row['region_destino']
            w = row['distancia_km']
            # Usar tupla ordenada para evitar duplicados
            key = tuple(sorted([a, b]))
            edges.add((key[0], key[1], w))
        # Convertir a formato de networkx
        return [(a, b, {'weight': w}) for a, b, w in edges]
    
    def get_edge_coordinates(self):
        """
        Obtiene las coordenadas de inicio y fin de cada arista para dibujar en el mapa
        """
        if self.distancias_df is None:
            self.load_distancias()
        
        if self.regiones_df is None:
            self.load_regiones()
        
        # Crear diccionario de coordenadas
        coords = self.get_region_coordinates()
        
        # Crear lista de coordenadas para cada arista
        edge_coords = []
        for _, row in self.distancias_df.iterrows():
            origen = row['region_origen']
            destino = row['region_destino']
            
            if origen in coords and destino in coords:
                coord_origen = coords[origen]
                coord_destino = coords[destino]
                edge_coords.append((coord_origen, coord_destino))
        
        return edge_coords
    
    def generate_dummy_peru_map(self, ax):
        """
        Genera un mapa dummy de Perú con los puntos de las regiones
        """
        if self.regiones_df is None:
            self.load_regiones()
        
        # Dibujar los puntos para cada región
        ax.scatter(self.regiones_df['longitude'], self.regiones_df['latitude'], 
                   color='blue', s=50, zorder=3)
        
        # Añadir nombres de regiones
        for _, row in self.regiones_df.iterrows():
            ax.annotate(row['region'], 
                       (row['longitude'], row['latitude']),
                       xytext=(3, 3),
                       textcoords='offset points',
                       fontsize=8)
        
        # Configurar límites del mapa para Perú (aproximados)
        ax.set_xlim(-84, -68)
        ax.set_ylim(-19, 0)
        
        # Configurar título y etiquetas
        ax.set_title('Mapa de Regiones de Perú')
        ax.set_xlabel('Longitud')
        ax.set_ylabel('Latitud')
        
        # Añadir grilla
        ax.grid(True, linestyle='--', alpha=0.7)
        
        return ax
