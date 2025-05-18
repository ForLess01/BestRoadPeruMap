import sys
import os
import warnings

# Intentar importar PyQt5
qt_backend = None
try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QComboBox, QPushButton,
        QVBoxLayout, QHBoxLayout, QLabel, QWidget,
        QTableWidget, QTableWidgetItem, QHeaderView, QSplitter
    )
    from PyQt5.QtCore import Qt
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
    print("✓ Usando PyQt5 para la interfaz gráfica")
    qt_backend = "PyQt5"
except ImportError:
    print("ERROR: No se pudo importar PyQt5.\nPor favor, instala PyQt5 ejecutando: pip install PyQt5")
    sys.exit(1)

from data_loader import DataLoader
from graph_module import GraphBuilder
from map_module import MapVisualizer
import utils

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Título y tamaño de la ventana
        self.setWindowTitle("Ruteador Perú")
        self.resize(1200, 800)
        
        # Inicializar componentes
        self.data_loader = DataLoader()
        self.data_loader.load_regiones()
        self.data_loader.load_distancias()
        
        self.graph_builder = GraphBuilder(self.data_loader)
        self.map_visualizer = MapVisualizer(self.data_loader, self.graph_builder)
        
        # Configurar la interfaz gráfica
        self.setup_ui()
    
    def setup_ui(self):
        """
        Configura la interfaz gráfica de usuario
        """
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        
        # Splitter para dividir el panel de control y el mapa
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Panel de control (izquierda)
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        
        # Título
        title_label = QLabel("Ruteador Perú")
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        control_layout.addWidget(title_label)
        
        # Descripción
        desc_label = QLabel("Busca la ruta más corta entre dos regiones de Perú")
        desc_label.setAlignment(Qt.AlignCenter)
        control_layout.addWidget(desc_label)
        
        control_layout.addSpacing(20)
        
        # Selector de región de origen
        origin_layout = QHBoxLayout()
        origin_label = QLabel("Origen:")
        self.origin_combo = QComboBox()
        origin_layout.addWidget(origin_label)
        origin_layout.addWidget(self.origin_combo)
        control_layout.addLayout(origin_layout)
        
        # Selector de región de destino
        dest_layout = QHBoxLayout()
        dest_label = QLabel("Destino:")
        self.dest_combo = QComboBox()
        dest_layout.addWidget(dest_label)
        dest_layout.addWidget(self.dest_combo)
        control_layout.addLayout(dest_layout)
        
        # Botón de cálculo de ruta
        self.route_button = QPushButton("Calcular Ruta")
        self.route_button.setStyleSheet("font-weight: bold; padding: 8px;")
        control_layout.addWidget(self.route_button)
        
        control_layout.addSpacing(20)
        
        # Tabla de resultados
        results_label = QLabel("Detalles de la Ruta:")
        results_label.setStyleSheet("font-weight: bold;")
        control_layout.addWidget(results_label)
        
        self.result_table = QTableWidget(0, 3)
        self.result_table.setHorizontalHeaderLabels(["Origen", "Destino", "Distancia"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        control_layout.addWidget(self.result_table)
        
        # Label para la distancia total
        self.total_distance_label = QLabel("Distancia Total: 0 km")
        self.total_distance_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        control_layout.addWidget(self.total_distance_label)
        
        # Panel derecho (mapa)
        map_panel = QWidget()
        map_layout = QVBoxLayout(map_panel)
        
        # Canvas del mapa
        self.canvas = self.map_visualizer.get_canvas()
        map_layout.addWidget(self.canvas)
        
        # Barra de navegación de matplotlib
        self.toolbar = NavigationToolbar(self.canvas, self)
        map_layout.addWidget(self.toolbar)
        
        # Añadir paneles al splitter
        splitter.addWidget(control_panel)
        splitter.addWidget(map_panel)
        splitter.setSizes([300, 900])
        
        # Llenar los combobox con las regiones
        self.populate_region_combos()
        
        # Conectar eventos
        self.route_button.clicked.connect(self.calculate_route)
        
        # Dibujar el mapa inicial
        self.map_visualizer.draw_base_map()
    
    def populate_region_combos(self):
        """
        Llena los combobox con la lista de regiones
        """
        regions = self.data_loader.get_region_names()
        
        self.origin_combo.clear()
        self.dest_combo.clear()
        
        for region in regions:
            self.origin_combo.addItem(region)
            self.dest_combo.addItem(region)
        
        # Seleccionar por defecto Lima y Cusco
        lima_index = self.origin_combo.findText("Lima")
        if lima_index >= 0:
            self.origin_combo.setCurrentIndex(lima_index)
            
        cusco_index = self.dest_combo.findText("Cusco")
        if cusco_index >= 0:
            self.dest_combo.setCurrentIndex(cusco_index)
    
    def calculate_route(self):
        """
        Calcula y muestra la ruta más corta entre las regiones seleccionadas
        """
        origin = self.origin_combo.currentText()
        destination = self.dest_combo.currentText()
        
        # Verificar si el origen y el destino son iguales
        if origin == destination:
            utils.show_error_message(self, "Error", "Por favor, seleccione dos regiones diferentes.")
            return
        
        # Calcular y visualizar la ruta
        path, total_distance, distances = self.map_visualizer.visualize_route(origin, destination)
        
        # Verificar si se encontró una ruta
        if not path:
            utils.show_error_message(self, "Error", "No existe una ruta entre las regiones seleccionadas.")
            self.clear_results()
            return
        
        # Actualizar la tabla de resultados
        self.update_result_table(distances)
        
        # Actualizar la etiqueta de distancia total
        self.total_distance_label.setText(f"Distancia Total: {utils.format_distance(total_distance)}")
    
    def update_result_table(self, distances):
        """
        Actualiza la tabla de resultados con los tramos de la ruta
        
        Args:
            distances: Lista de tuplas (origen, destino, distancia)
        """
        # Limpiar tabla
        self.result_table.setRowCount(0)
        
        # Llenar tabla con los tramos
        for origin, destination, distance in distances:
            row_position = self.result_table.rowCount()
            self.result_table.insertRow(row_position)
            
            self.result_table.setItem(row_position, 0, QTableWidgetItem(origin))
            self.result_table.setItem(row_position, 1, QTableWidgetItem(destination))
            self.result_table.setItem(row_position, 2, QTableWidgetItem(utils.format_distance(distance)))
    
    def clear_results(self):
        """
        Limpia los resultados de la tabla y la distancia total
        """
        self.result_table.setRowCount(0)
        self.total_distance_label.setText("Distancia Total: 0 km")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
