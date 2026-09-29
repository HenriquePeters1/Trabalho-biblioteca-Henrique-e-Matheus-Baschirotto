#Trabalho feito por Henrique Peters e Matheus Baschirotto
#Nós separamos de modo que o Matheus vai fazer a parte do SQL porque ele entendeu melhor e eu (Henrique) vou fazer mais ou menos 70% do python
#Arquivo main este arquivo vai criar o menu e importar o código dos outros aquivos
import banco
import usuarios
import autores
import editoras
import livros
import emprestimos
def menu_principal():
    while True:
        print("\n========================================\n        SISTEMA DE BIBLIOTECA\n========================================\n1 - Usuários\n2 - Autores\n3 - Editoras\n4 - Livros\n5 - Empréstimos\n0 - Sair\n========================================")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            usuarios.menu()
        elif opcao == "2":
            autores.menu()
        elif opcao == "3":
            editoras.menu()
        elif opcao == "4":
            livros.menu()
        elif opcao == "5":
            emprestimos.menu()
        elif opcao == "0":
            print("Programa encerrado.")
            break
        else:
            print("Opção inválida.")
if __name__ == "__main__":
    banco.criar_tabelas()
    menu_principal()