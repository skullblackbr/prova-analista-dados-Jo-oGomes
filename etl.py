import pandas as pd
import sqlite3
from datetime import datetime

class ETL:
    def __init__(self, arquivo_origem, nome_banco='dados.db', nome_tabela='vendas'):
        self.arquivo_origem = arquivo_origem
        self.nome_banco = nome_banco
        self.nome_tabela = nome_tabela
        self.df = None
        self.conn = None
    
    def extraer(self):
        print(f"[EXTRACT] Lendo: {self.arquivo_origem}")
        extensao = self.arquivo_origem.split('.')[-1].lower()
        
        if extensao == 'csv':
            try:
                self.df = pd.read_csv(self.arquivo_origem, encoding='utf-8')
            except:
                self.df = pd.read_csv(self.arquivo_origem, encoding='latin1')
        elif extensao == 'json':
            self.df = pd.read_json(self.arquivo_origem)
        elif extensao == 'xlsx':
            self.df = pd.read_excel(self.arquivo_origem)
        
        print(f"   Registros: {len(self.df)}")
        print(f"   Colunas: {list(self.df.columns)}")
        return self.df
    
    def transformar(self):
        print("[TRANSFORM] Limpando dados...")
        original = len(self.df)
        
        self.df = self.df.drop_duplicates()
        duplicatas = original - len(self.df)
        print(f"   Duplicatas removidas: {duplicatas}")
        
        nulos_antes = self.df.isnull().sum().sum()
        self.df = self.df.fillna(0)
        print(f"   Nulos tratados: {nulos_antes}")
        
        self.df.columns = self.df.columns.str.strip().str.replace(' ', '_')
        
        for col in self.df.columns:
            if 'data' in col.lower() or 'date' in col.lower():
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
        
        if 'Valor' in self.df.columns and 'Quantidade' in self.df.columns:
            self.df['Total'] = self.df['Valor'] * self.df['Quantidade']
            print("   Coluna 'Total' criada")
        
        for col in self.df.select_dtypes(include=['float64']).columns:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)
        
        print(f"   Registros finais: {len(self.df)}")
        return self.df
    
    def cargar(self):
        print(f"[LOAD] Salvando em {self.nome_banco}...")
        self.conn = sqlite3.connect(self.nome_banco)
        self.df.to_sql(self.nome_tabela, self.conn, if_exists='replace', index=False)
        
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {self.nome_tabela}")
        total = cursor.fetchone()[0]
        print(f"   Tabela '{self.nome_tabela}' com {total} registros")
        return self.conn
    
    def executar(self):
        print("=" * 50)
        print("INICIO - ETL")
        print("=" * 50)
        print(f"Hora: {datetime.now()}")
        
        self.extraer()
        self.transformar()
        self.cargar()
        
        print("=" * 50)
        print("SUCESSO - ETL Concluido!")
        print("=" * 50)
        return self.df
    
    def fechar(self):
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    import sys
    arquivo = sys.argv[1] if len(sys.argv) > 1 else 'dados_originais.csv'
    banco = sys.argv[2] if len(sys.argv) > 2 else 'dados.db'
    
    etl = ETL(arquivo, banco)
    etl.executar()
    etl.fechar()