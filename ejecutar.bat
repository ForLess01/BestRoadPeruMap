@echo off
REM Script para ejecutar la aplicación Ruteador Perú en Windows

echo Ejecutando Ruteador Peru...
python main.py

IF %ERRORLEVEL% NEQ 0 (
    echo Error al ejecutar la aplicacion principal.
    echo Intentando ejecutar la version alternativa...
    python main_pyside2.py
    
    IF %ERRORLEVEL% NEQ 0 (
        echo Error al ejecutar la version alternativa.
        echo Instalando dependencias necesarias...
        pip install -r requirements.txt
        echo Intentando ejecutar nuevamente...
        python main.py
        
        IF %ERRORLEVEL% NEQ 0 (
            echo ====================================
            echo No se pudo ejecutar la aplicacion!
            echo Intente instalar PyQt5 manualmente:
            echo conda install -c anaconda pyqt
            echo ====================================
        )
    )
)

pause
