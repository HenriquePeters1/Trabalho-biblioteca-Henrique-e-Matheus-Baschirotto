#Arquivo autores este arquivo vai ter as fnções de cadastrar, listar e mostrar o menu dos autores
from banco import conectar
def cadastrar():
    nome = input("Nome do autor: ").strip()
    if not nome:
        print("O nome não pode ficar vazio.")
        return
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO autores (nome) VALUES (?)",(nome,))
    conexao.commit()
    conexao.close()
    print("Autor cadastrado com sucesso!")
def listar():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome
        FROM autores
        ORDER BY id
    """)
    autores = cursor.fetchall()
    conexao.close()
    print("\n========== AUTORES ==========")
    if not autores:
        print("Nenhum autor cadastrado.")
        return
    for autor in autores:
        print(
            f"ID: {autor[0]} | "
            f"Nome: {autor[1]}")
def menu():
    while True:
        print("========== MENU AUTORES ==========\n1 - Cadastrar autor\n2 - Listar autores\n0 - Voltar\n")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            listar()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")