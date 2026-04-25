import requests
from etl import ETL
import sqlite3
from datetime import datetime

class DownloadDatasets:
    DATASETS = {
        'vendas': 'https://raw.githubusercontent.com/datasets/advertising-expenditure/master/data/advertising.csv',
        'covid': 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv',
    }
    
    @staticmethod
    def baixar(nome, destino=None):
        url = DownloadDatasets.DATASETS.get(nome)
        if not url:
            print(f"Dataset '{nome}' indisponivel!")
            return None
        
        destino = destino or f'{nome}.csv'
        print(f"Baixando {nome}...")
        
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                with open(destino, 'wb') as f:
                    f.write(resp.content)
                print(f"Salvo: {destino}")
                return destino
        except Exception as e:
            print(f"Erro: {e}")
        return None

class Pipeline:
    def __init__(self):
        self.dados = 'dados_originais.csv'
        self.banco = 'dados.db'
    
    def executar(self):
        print("=" * 50)
        print("PIPELINE COMPLETO")
        print("=" * 50)
        print(f"Inicio: {datetime.now()}")
        
        # Baixar
        print("[1/4] Baixando dataset...")
        DownloadDatasets.baixar('vendas', self.dados)
        
        # ETL
        print("[2/4] Executando ETL...")
        etl = ETL(self.dados, self.banco, 'vendas')
        etl.executar()
        etl.fechar()
        
        # Queries
        print("[3/4] Gerando resultados...")
        conn = sqlite3.connect(self.banco)
        cursor = conn.cursor()
        
        with open('resultados.txt', 'w', encoding='utf-8') as f:
            f.write(f"Resultados - {datetime.now()}\n")
            f.write("=" * 40 + "\n\n")
            
            queries = [
                ("Total registros", "SELECT COUNT(*) FROM vendas"),
                ("Soma total", "SELECT COALESCE(SUM(Total), 0) FROM vendas"),
                ("Media valor", "SELECT AVG(Valor) FROM vendas"),
                ("Minimo", "SELECT MIN(Valor) FROM vendas"),
                ("Maximo", "SELECT MAX(Valor) FROM vendas"),
            ]
            
            for desc, sql in queries:
                cursor.execute(sql)
                f.write(f"{desc}: {cursor.fetchone()[0]}\n")
        
        conn.close()
        
        # Resumo
        print("[4/4] Resumo:")
        with open('resultados.txt', 'r', encoding='utf-8') as f:
            print(f.read())
        
        print(f"Fim: {datetime.now()}")
        return True

if __name__ == "__main__":
    Pipeline().executar()