import funcoes

def exibir_menu():
    while True:
        print("\n--- SISTEMA BIBLIOTECA MODULAR ---")
        print("1. Cadastrar")
        print("2. Listar")
        print("3. Pesquisar")
        print("4. Alterar")
        print("0. Sair")
        
        opcao = input("\nEscolha: ")

        if opcao == "1":
            funcoes.cadastrar()
        elif opcao == "2":
            funcoes.listar()
        elif opcao == "3":
            funcoes.pesquisar()
        elif opcao == "4":
            funcoes.alterar_livro()
        elif opcao == "0":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    exibir_menu()