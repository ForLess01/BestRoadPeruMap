@echo off
REM Script para ejecutar la aplicación Ruteador Perú usando Anaconda

echo Activando entorno de Anaconda...
call conda activate base

echo Ejecutando Ruteador Perú...
python main.py

pause
