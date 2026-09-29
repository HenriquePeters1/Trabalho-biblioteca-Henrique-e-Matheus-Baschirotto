#Arquivo usuarios este vai ter as funções de cadastrar, listar e mostrar o menu de usuarioas
from banco import conectar
def cadastrar():
    nome = input("Nome do usuário: ").strip()
    if not nome:
        print("O nome não pode ficar vazio.")
        return
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome) VALUES (?)",
        (nome,)
    )
    conexao.commit()
    conexao.close()
    print("Usuário cadastrado com sucesso!")
def listar():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome
        FROM usuarios
        ORDER BY id
    """)
    usuarios = cursor.fetchall()
    conexao.close()
    print("\n========== USUÁRIOS ==========")
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    for usuario in usuarios:
        print(
            f"ID: {usuario[0]} | "
            f"Nome: {usuario[1]}"
        )
def menu():
    while True:
        print("========== MENU USUÁRIOS ==========\n1 - Cadastrar usuário\n2 - Listar usuários\n0 - Voltar\n")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            listar()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")