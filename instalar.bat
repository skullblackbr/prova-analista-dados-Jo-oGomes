@echo off
chcp 65001 >nul
title Instalador - Prova Analista de Dados

echo ========================================
echo  Instalador de Ambiente
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Instale o Python 3.8+:
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python:
python --version
echo.

echo [1/3] Atualizando pip...
python -m pip install --upgrade pip >nul 2>&1
echo.

echo [2/3] Instalando dependencias...
pip install pandas sqlalchemy openpyxl requests
echo.

echo [3/3] Verificando...
python -c "import pandas; import sqlalchemy; import openpyxl; import requests; print('[OK] Tudo instalado!')"
echo.

echo ========================================
echo  Instalacao concluida!
echo ========================================
echo.
pause