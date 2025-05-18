import networkx as nx

class GraphBuilder:
    def __init__(self, data_loader):
        """
        Inicializa el constructor del grafo utilizando el cargador de datos proporcionado
        
        Args:
            data_loader: Instancia de DataLoader que proporciona los datos necesarios
        """
        self.data_loader = data_loader
        self.graph = None
        self.build_graph()
    
    def build_graph(self):
        """
        Construye un grafo no dirigido a partir de los datos de distancias
        """
        # Crear un grafo no dirigido
        self.graph = nx.Graph()
        
        # Obtener las aristas del cargador de datos
        edges = self.data_loader.get_edges_for_graph()
        
        # Agregar aristas al grafo
        self.graph.add_edges_from(edges)
        
        return self.graph
    
    def get_graph(self):
        """
        Devuelve el grafo construido
        """
        if self.graph is None:
            self.build_graph()
        return self.graph
    
    def calculate_shortest_path(self, origin, destination):
        """
        Calcula la ruta más corta entre dos regiones utilizando el algoritmo de Dijkstra
        
        Args:
            origin: Región de origen
            destination: Región de destino
            
        Returns:
            path: Lista de regiones que forman la ruta más corta
            total_distance: Distancia total de la ruta en kilómetros
            distances: Distancias parciales entre cada par de regiones en la ruta
        """
        if self.graph is None:
            self.build_graph()
        
        # Verificar si el origen es igual al destino
        if origin == destination:
            return None, 0, []
        
        # Verificar si tanto origen como destino están en el grafo
        if origin not in self.graph.nodes or destination not in self.graph.nodes:
            return None, 0, []
        
        try:
            # Calcular la ruta más corta utilizando Dijkstra
            path = nx.shortest_path(self.graph, origin, destination, weight='weight')
            
            # Calcular la distancia total
            total_distance = 0
            distances = []
            
            # Calcular distancias parciales
            for i in range(len(path) - 1):
                start = path[i]
                end = path[i + 1]
                distance = self.graph[start][end]['weight']
                total_distance += distance
                distances.append((start, end, distance))
            
            return path, total_distance, distances
        
        except nx.NetworkXNoPath:
            # No hay ruta entre el origen y el destino
            return None, 0, []
    
    def get_all_edges(self):
        """
        Devuelve todas las aristas del grafo
        """
        if self.graph is None:
            self.build_graph()
        
        return list(self.graph.edges(data=True))
    
    def get_all_nodes(self):
        """
        Devuelve todos los nodos del grafo
        """
        if self.graph is None:
            self.build_graph()
        
        return list(self.graph.nodes())
