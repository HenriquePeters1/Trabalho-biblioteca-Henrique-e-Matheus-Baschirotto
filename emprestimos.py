#Arquivos empréstimos este arquivo tem as funções de cadstrar, listar, devolver e mostrar o menu de empréstimos
from banco import conectar
from datetime import date
def cadastrar():
    print("\n========== NOVO EMPRÉSTIMO ==========")
    conexao = conectar()
    cursor = conexao.cursor()
    # Usuários
    cursor.execute("""
        SELECT id, nome
        FROM usuarios
        ORDER BY id
    """)
    usuarios = cursor.fetchall()
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        conexao.close()
        return
    print("\nUsuários:")
    for usuario in usuarios:
        print(
            f"ID: {usuario[0]} | "
            f"Nome: {usuario[1]}"
        )
    usuario_id = int(input("\nID do usuário: "))
    cursor.execute(
        "SELECT id FROM usuarios WHERE id = ?",
        (usuario_id,)
    )
    if cursor.fetchone() is None:
        print("Usuário não encontrado.")
        conexao.close()
        return
    cursor.execute("""
        SELECT id, titulo
        FROM livros
        WHERE disponivel = 1
        ORDER BY id
    """)
    livros = cursor.fetchall()
    if not livros:
        print("Nenhum livro disponível.")
        conexao.close()
        return
    print("\nLivros disponíveis:")
    for livro in livros:
        print(
            f"ID: {livro[0]} | "
            f"Título: {livro[1]}"
        )
    livros_escolhidos = []
    print("\nDigite 0 quando terminar.")
    while True:
        livro_id = int(
            input("ID do livro: ")
        )
        if livro_id == 0:
            break
        cursor.execute("""
            SELECT id, titulo
            FROM livros
            WHERE id = ?
            AND disponivel = 1
        """, (livro_id,))
        livro = cursor.fetchone()
        if livro is None:
            print("Livro não encontrado ou indisponível.")
        elif livro_id in livros_escolhidos:
            print("Livro já selecionado.")
        else:
            livros_escolhidos.append(livro_id)
            print(
                f"'{livro[1]}' adicionado."
            )
    if not livros_escolhidos:
        print("Nenhum livro selecionado.")
        conexao.close()
        return
    data = date.today().isoformat()
    cursor.execute("""
        INSERT INTO emprestimos (
            usuario_id,
            data
        )
        VALUES (?, ?)
    """, (usuario_id, data))
    emprestimo_id = cursor.lastrowid
    for livro_id in livros_escolhidos:
        cursor.execute("""
            INSERT INTO emprestimos_livros (
                emprestimo_id,
                livro_id,
                data_devolucao
            )
            VALUES (?, ?, NULL)
        """, (
            emprestimo_id,
            livro_id
        ))
        cursor.execute("""
            UPDATE livros
            SET disponivel = 0
            WHERE id = ?
        """, (livro_id,))
    conexao.commit()
    conexao.close()
    print(
        f"\nEmpréstimo #{emprestimo_id} "
        "cadastrado com sucesso!"
    )
def listar():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT
            emprestimos.id,
            usuarios.nome,
            emprestimos.data
        FROM emprestimos
        INNER JOIN usuarios
            ON emprestimos.usuario_id = usuarios.id

        ORDER BY emprestimos.id
    """)
    emprestimos = cursor.fetchall()
    print("\n========== EMPRÉSTIMOS ==========")
    if not emprestimos:
        print("Nenhum empréstimo cadastrado.")
        conexao.close()
        return
    for emprestimo in emprestimos:
        print(f"""
Empréstimo: {emprestimo[0]}
Usuário: {emprestimo[1]}
Data: {emprestimo[2]}
Livros:""")
        cursor.execute("""
            SELECT
                livros.id,
                livros.titulo,
                emprestimos_livros.data_devolucao
            FROM emprestimos_livros
            INNER JOIN livros
                ON emprestimos_livros.livro_id = livros.id
            WHERE emprestimos_livros.emprestimo_id = ?
        """, (emprestimo[0],))
        livros = cursor.fetchall()
        for livro in livros:
            if livro[2] is None:
                status = "Não devolvido"
            else:
                status = (
                    f"Devolvido em {livro[2]}"
                )
            print(
                f"  ID: {livro[0]} | "
                f"{livro[1]} | "
                f"{status}"
            )
        print("------------------------------")
    conexao.close()
def devolver():
    print("\n========== DEVOLUÇÃO ==========")
    emprestimo_id = int(
        input("ID do empréstimo: ")
    )
    livro_id = int(
        input("ID do livro: ")
    )
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT *
        FROM emprestimos_livros
        WHERE emprestimo_id = ?
        AND livro_id = ?
        AND data_devolucao IS NULL
    """, (
        emprestimo_id,
        livro_id
    ))
    registro = cursor.fetchone()
    if registro is None:
        print(
            "Empréstimo ou livro não encontrado, "
            "ou o livro já foi devolvido."
        )
        conexao.close()
        return
    data_devolucao = date.today().isoformat()
    cursor.execute("""
        UPDATE emprestimos_livros
        SET data_devolucao = ?
        WHERE emprestimo_id = ?
        AND livro_id = ?
    """, (
        data_devolucao,
        emprestimo_id,
        livro_id
    ))
    cursor.execute("""
        UPDATE livros
        SET disponivel = 1
        WHERE id = ?
    """, (livro_id,))
    conexao.commit()
    conexao.close()
    print("Livro devolvido com sucesso!")
def menu():
    while True:
        print("========== MENU EMPRÉSTIMOS ==========\n1 - Cadastrar empréstimo\n2 - Listar empréstimos\n3 - Devolver livro\n0 - Voltar\n")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            listar()
        elif opcao == "3":
            devolver()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")