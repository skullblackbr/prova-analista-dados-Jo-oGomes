import sqlite3

class ConexaoDB:
    def __init__(self, nome_banco='dados.db'):
        self.nome_banco = nome_banco
        self.conexao = None
    
    def conectar(self):
        try:
            self.conexao = sqlite3.connect(self.nome_banco)
            return self.conexao
        except Exception as e:
            print(f"Erro: {e}")
            return None
    
    def desconectar(self):
        if self.conexao:
            self.conexao.close()
    
    def executar_query(self, query):
        cursor = self.conexao.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    
    def listar_tabelas(self):
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        cursor = self.conexao.cursor()
        cursor.execute(query)
        return [t[0] for t in cursor.fetchall()]

if __name__ == "__main__":
    db = ConexaoDB('dados.db')
    db.conectar()
    if db.conexao:
        tabelas = db.listar_tabelas()
        print(f"Tabelas: {tabelas}")
        db.desconectar()