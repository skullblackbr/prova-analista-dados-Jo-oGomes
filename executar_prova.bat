@echo off
chcp 65001 >nul
title Prova Analista de Dados

echo ========================================
echo  Prova Pratica - Analista de Dados
echo  ETL + Power BI
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao instalado!
    echo Instale em: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python:
python --version
echo.

echo [1/4] Instalando dependencias...
pip install pandas sqlalchemy openpyxl requests >nul 2>&1
echo.

echo [2/4] Criando dataset exemplo...
python -c "
import pandas as pd
import random
data = {
    'ID': range(1, 101),
    'Produto': [random.choice(['A','B','C','D','E']) for _ in range(100)],
    'Categoria': [random.choice(['Eletronicos','Roupas','Alimentos','Moveis']) for _ in range(100)],
    'Valor': [round(random.uniform(10, 500), 2) for _ in range(100)],
    'Quantidade': [random.randint(1, 10) for _ in range(100)],
    'Data': [f'2024-0{random.randint(1,9)}-{random.randint(10,28)}' for _ in range(100)]
}
df = pd.DataFrame(data)
df.to_csv('dados_originais.csv', index=False)
print('OK')
"
echo.

echo [3/4] Executando ETL...
python etl.py dados_originais.csv dados.db
echo.

echo [4/4] Executando Queries...
python queries.py
echo.

echo ========================================
echo  Concluido!
echo ========================================
echo.
echo Arquivos criados:
dir *.csv *.db *.txt 2>nul
echo.
echo Proximo passo:
echo 1. Abrir Power BI Desktop
echo 2. Conectar em dados.db
echo 3. Criar dashboard
echo 4. Enviar para GitHub
echo.
pause