import sqlite3
import os

# Caminho dinâmico para o diretório do projeto
current_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual

# Caminho para o banco de dados e o arquivo SQL na mesma pasta
banco_sql_path = os.path.join(current_dir,  'banco.sql')  # Caminho para o arquivo SQL
banco_db_path = os.path.join(current_dir,  'banco.db')  # Caminho para o arquivo do banco de dados

# Verifica se o arquivo SQL existe
if not os.path.exists(banco_sql_path):
    print(f"Erro: Arquivo {banco_sql_path} não encontrado.")
    exit(1)

# Conexão com o banco de dados
try:
    # Cria o banco de dados na pasta 'database'
    conn = sqlite3.connect(banco_db_path)
    
    # Executa o script SQL para criar as tabelas
    with open(banco_sql_path, 'r') as banco:
        conn.executescript(banco.read())
    
    conn.commit()
    print("Banco de dados inicializado com sucesso.")
    
except sqlite3.Error as e:
    print(f"Erro no SQLite: {e}")

finally:
    conn.close()

# Conexão para garantir que a tabela seja criada, se necessário
conn = sqlite3.connect(banco_db_path)  # Usando o banco de dados correto

# Criação manual da tabela, caso o script SQL não a tenha criado
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tb_usuarios (
    usu_id INTEGER PRIMARY KEY AUTOINCREMENT,
    usu_email TEXT NOT NULL UNIQUE,
    usu_senha TEXT NOT NULL
);
""")

print("Tabela criada com sucesso.")
conn.commit()
conn.close()