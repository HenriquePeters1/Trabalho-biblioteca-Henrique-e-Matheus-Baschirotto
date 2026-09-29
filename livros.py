#Arquivo livros este arquivo tem as funções cadastrar, listar e mostrar o menu de livrso
from banco import conectar
def cadastrar():
    titulo = input("Título do livro: ").strip()
    if not titulo:
        print("O título não pode ficar vazio.")
        return
    print("\n========== AUTORES ==========")
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome
        FROM autores
        ORDER BY id
    """)
    autores = cursor.fetchall()
    if not autores:
        print("Cadastre um autor antes de cadastrar um livro.")
        conexao.close()
        return
    for autor in autores:
        print(
            f"ID: {autor[0]} | "
            f"Nome: {autor[1]}"
        )
    autor_id = int(input("\nID do autor: "))
    cursor.execute(
        "SELECT id FROM autores WHERE id = ?",
        (autor_id,)
    )
    if cursor.fetchone() is None:
        print("Autor não encontrado.")
        conexao.close()
        return
    print("\n========== EDITORAS ==========")
    cursor.execute("""
        SELECT id, nome
        FROM editoras
        ORDER BY id
    """)
    editoras = cursor.fetchall()
    if not editoras:
        print("Cadastre uma editora antes de cadastrar um livro.")
        conexao.close()
        return
    for editora in editoras:
        print(
            f"ID: {editora[0]} | "
            f"Nome: {editora[1]}"
        )
    editora_id = int(input("\nID da editora: "))
    cursor.execute(
        "SELECT id FROM editoras WHERE id = ?",
        (editora_id,)
    )
    if cursor.fetchone() is None:
        print("Editora não encontrada.")
        conexao.close()
        return
    ano = int(input("Ano de publicação: "))
    edicao = int(input("Edição: "))
    cursor.execute("""
        INSERT INTO livros (
            titulo,
            autor_id,
            editora_id,
            ano_publicacao,
            edicao,
            disponivel
        )
        VALUES (?, ?, ?, ?, ?, 1)
    """, (
        titulo,
        autor_id,
        editora_id,
        ano,
        edicao
    ))
    conexao.commit()
    conexao.close()
    print("Livro cadastrado com sucesso!")
def listar():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT
            livros.id,
            livros.titulo,
            autores.nome,
            editoras.nome,
            livros.ano_publicacao,
            livros.edicao,
            livros.disponivel
        FROM livros
        INNER JOIN autores
            ON livros.autor_id = autores.id
        INNER JOIN editoras
            ON livros.editora_id = editoras.id
        ORDER BY livros.id
    """)
    livros = cursor.fetchall()
    conexao.close()
    print("\n========== LIVROS ==========")
    if not livros:
        print("Nenhum livro cadastrado.")
        return
    for livro in livros:
        if livro[6] == 1:
            status = "Disponível"
        else:
            status = "Emprestado"
        print(f"""
ID: {livro[0]}
Título: {livro[1]}
Autor: {livro[2]}
Editora: {livro[3]}
Ano de publicação: {livro[4]}
Edição: {livro[5]}
Status: {status}
------------------------------
""")
def menu():
    while True:
        print("========== MENU LIVROS ==========\n1 - Cadastrar livro\n2 - Listar livros\n0 - Voltar\n")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            listar()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")