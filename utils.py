from PyQt5.QtWidgets import QMessageBox

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