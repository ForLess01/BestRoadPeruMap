try:
    from PyQt5.QtWidgets import QMessageBox
    print("Utils: Usando PyQt5")
except ImportError:
    try:
        from PySide2.QtWidgets import QMessageBox
        print("Utils: Usando PySide2")
    except ImportError:
        print("No se pudo importar QMessageBox de PyQt5 ni PySide2")
        
        # Crear un sustituto básico para QMessageBox que muestra mensajes en consola
        class FakeMessageBox:
            Ok = 0
            
            @staticmethod
            def critical(parent, title, message, buttons):
                print(f"ERROR: {title} - {message}")
                return 0
                
            @staticmethod
            def information(parent, title, message, buttons):
                print(f"INFO: {title} - {message}")
                return 0
        
        QMessageBox = FakeMessageBox
        print("Utils: Usando implementación de consola para los mensajes")

def show_error_message(parent, title, message):
    """
    Muestra un mensaje de error
    
    Args:
        parent: Ventana padre
        title: Título del mensaje
        message: Contenido del mensaje
    """
    QMessageBox.critical(parent, title, message, QMessageBox.Ok)

def show_info_message(parent, title, message):
    """
    Muestra un mensaje informativo
    
    Args:
        parent: Ventana padre
        title: Título del mensaje
        message: Contenido del mensaje
    """
    QMessageBox.information(parent, title, message, QMessageBox.Ok)

def format_distance(distance):
    """
    Formatea una distancia en kilómetros
    
    Args:
        distance: Distancia en kilómetros
        
    Returns:
        Cadena formateada de la distancia
    """
    return f"{distance:.1f} km"
