@echo off
TITLE PDF OCR Vision V2 - Alto Contraste
echo ===================================================
echo   Iniciando sistema de Visión Artificial para PDF
echo ===================================================

:: Comprobar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python no esta instalado en este equipo.
    echo Abriendo la pagina oficial para descargarlo...
    start https://www.python.org/downloads/
    pause
    exit
)

:: Ejecutar el script principal
python windows_vision_v2.py
pause
