import sqlite3
from conexao import ConexaoDB

class QueriesAnaliticas:
    def __init__(self, nome_banco='dados.db'):
        self.db = ConexaoDB(nome_banco)
        self.db.conectar()
    
    def total_registros(self):
        query = "SELECT Count(*) FROM vendas"
        resultado = self.db.executar_query(query)
        return resultado[0][0] if resultado else 0
    
    def soma_total(self):
        query = "SELECT Sum(Total) FROM vendas"
        resultado = self.db.executar_query(query)
        return resultado[0][0] if resultado[0][0] else 0
    
    def media(self):
        query = "SELECT AVG(Valor) FROM vendas"
        resultado = self.db.executar_query(query)
        return resultado[0][0] if resultado[0][0] else 0
    
    def min_max(self):
        query = "SELECT MIN(Valor), MAX(Valor) FROM vendas"
        resultado = self.db.executar_query(query)
        return resultado[0] if resultado else (0, 0)
    
    def agrupamento_categoria(self):
        query = "SELECT Categoria, Count(*), Sum(Total) FROM vendas GROUP BY Categoria"
        return self.db.executar_query(query)
    
    def top_produtos(self, limite=5):
        query = f"SELECT Produto, Sum(Quantidade), Sum(Total) FROM vendas GROUP BY Produto ORDER BY Sum(Total) DESC LIMIT {limite}"
        return self.db.executar_query(query)
    
    def distribuir_categoria(self):
        query = "SELECT Categoria, Count(*) * 100.0 / (SELECT Count(*) FROM vendas) FROM vendas GROUP BY Categoria"
        return self.db.executar_query(query)
    
    def executar_todas(self):
        print("=" * 50)
        print("RELATORIO ANALITICO")
        print("=" * 50)
        
        print(f"\n1. Total Registros: {self.total_registros()}")
        print(f"2. Soma Total: R$ {self.soma_total():.2f}")
        print(f"3. Media: R$ {self.media():.2f}")
        
        minimo, maximo = self.min_max()
        print(f"4. Menor: R$ {minimo:.2f}")
        print(f"5. Maior: R$ {maximo:.2f}")
        
        print("\n6. Por Categoria:")
        for row in self.agrupamento_categoria():
            print(f"   {row[0]}: {row[1]} vendas, R$ {row[2]:.2f}")
        
        print("\n7. Top 5 Produtos:")
        for row in self.top_produtos(5):
            print(f"   {row[0]}: {row[1]} unid, R$ {row[2]:.2f}")
        
        self.db.desconectar()

if __name__ == "__main__":
    q = QueriesAnaliticas('dados.db')
    q.executar_todas()