import sqlite3
from flask_login import UserMixin

banco = 'banco.db'

def conexao():
    conn = sqlite3.connect(banco)
    conn.row_factory = sqlite3.Row
    return conn


class Users(UserMixin):
    def __init__(self, id, nome, email, senha):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha

    @classmethod
    def get(cls, user_id):
        conn = conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tb_usuarios WHERE usu_id = ?', (user_id,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            return cls(
                user_data['usu_id'],
                user_data['usu_nome'],
                user_data['usu_email'],
                user_data['usu_senha']
            )
        return None
    
    @classmethod
    def get_by_email(cls, email):
        conn = conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tb_usuarios WHERE usu_email = ?', (email,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            return cls(
                user_data['usu_id'],
                user_data['usu_nome'],
                user_data['usu_email'],
                user_data['usu_senha']
            )
        return None

