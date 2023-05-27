print("Db.py Carregado")
import sqlite3

# Função para criar as tabelas no banco de dados, caso ainda não existam
def criar_tabelas():
    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    # Tabela de itens
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL
        )
    """)

    # Tabela de usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL,
            admin INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

