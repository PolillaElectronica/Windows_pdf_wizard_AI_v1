@echo off
TITLE PDF OCR Vision V2 - Alto Contraste

:: ESTA ES LA LÍNEA MÁGICA: Obliga a Windows a ubicarse en esta misma carpeta
cd /d "%~dp0"

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
:: ¡IMPORTANTE! Si cambiaste el nombre del archivo de Python, cámbialo aquí también:
python windows_vision_v2.py

pause
