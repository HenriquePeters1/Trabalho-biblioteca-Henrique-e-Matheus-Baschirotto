#Arquivo banco este serve para executar os códigos SQL
import sqlite3
BANCO = "biblioteca.db"
def conectar():
    return sqlite3.connect(BANCO)
def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
        """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS autores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS editoras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor_id INTEGER NOT NULL,
            editora_id INTEGER NOT NULL,
            ano_publicacao INTEGER,
            edicao INTEGER,
            disponivel INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (autor_id) REFERENCES autores(id),
            FOREIGN KEY (editora_id) REFERENCES editoras(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emprestimos_livros (
            emprestimo_id INTEGER NOT NULL,
            livro_id INTEGER NOT NULL,
            data_devolucao TEXT,
            PRIMARY KEY (emprestimo_id, livro_id),
            FOREIGN KEY (emprestimo_id)
                REFERENCES emprestimos(id),
            FOREIGN KEY (livro_id)
                REFERENCES livros(id)
        )
    """)
    conexao.commit()
    conexao.close()