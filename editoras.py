#Arquivo editors este arquivo tem as funções de cadastrar, listar e mostrar o menu de editoras
from banco import conectar
def cadastrar():
    nome = input("Nome da editora: ").strip()
    if not nome:
        print("O nome não pode ficar vazio.")
        return
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO editoras (nome) VALUES (?)",
        (nome,)
    )
    conexao.commit()
    conexao.close()
    print("Editora cadastrada com sucesso!")
def listar():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome
        FROM editoras
        ORDER BY id
    """)
    editoras = cursor.fetchall()
    conexao.close()
    print("\n========== EDITORAS ==========")
    if not editoras:
        print("Nenhuma editora cadastrada.")
        return
    for editora in editoras:
        print(
            f"ID: {editora[0]} | "
            f"Nome: {editora[1]}"
        )
def menu():
    while True:
        print("========== MENU EDITORAS ==========\n1 - Cadastrar editora\n2 - Listar editoras\n0 - Voltar")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            listar()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")