import dados

biblioteca = dados.carregar_do_arquivo()

import dados

def cadastrar():
    print("\n" + "="*15 + " NOVO CADASTRO DE OBRA " + "="*15)
    
    # Identificador único (importante para a função de alterar/excluir depois)
    isbn = input("ISBN (Ex: 978...): ").strip()
    
    # Validação simples: verificar se o ISBN já existe na memória
    for livro in funcoes.biblioteca: # ou apenas 'biblioteca' se estiver no mesmo escopo
        if livro['isbn'] == isbn:
            print("\n⚠️  ERRO: Já existe um livro cadastrado com este ISBN!")
            return

    titulo = input("Título: ").strip()
    autor = input("Autor: ").strip()
    genero = input("Gênero: ").strip()
    editora = input("Editora: ").strip()
    localizacao = input("Localização (Ex: Estante A1, Prateleira 2): ").strip()

    try:
        ano = int(input("Ano de Publicação: "))
        paginas = int(input("Quantidade de Páginas: "))
    except ValueError:
        print("\n❌ ERRO: Ano e Páginas devem ser números inteiros. Cadastro cancelado.")
        return

    novo_livro = {
        "isbn": isbn,
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "ano_publicacao": ano,
        "editora": editora,
        "paginas": paginas,
        "status": "disponivel", 
        "localizacao": localizacao
    }

    funcoes.biblioteca.append(novo_livro)
    dados.salvar_no_arquivo(funcoes.biblioteca)
    
    print(f"\n✔ '{titulo}' cadastrado e salvo com sucesso!")

def listar():
    if not biblioteca:
        print("\nAcervo vazio.")
        return
    
    print("\n" + "="*40)
    for l in biblioteca:
        print(f"[{l['isbn']}] {l['titulo']} - {l['autor']} ({l['status']})")
    print("="*40)

def pesquisar():
    termo = input("\n🔍 Digite o Título ou ISBN para busca: ").strip().lower()
    
    # Busca por parte do título ou ISBN exato
    resultados = [l for l in biblioteca if termo in l['titulo'].lower() or termo == l['isbn']]
    
    if resultados:
        print(f"\n✅ Foram encontrados {len(resultados)} resultado(s):")
        for r in resultados:
            print("-" * 40)
            print(f"📌 TÍTULO:      {r.get('titulo', 'N/A').upper()}")
            print(f"🆔 ISBN:        {r.get('isbn', 'N/A')}")
            print(f"✍️  AUTOR:       {r.get('autor', 'N/A')}")
            print(f"🎭 GÊNERO:      {r.get('genero', 'N/A')}")
            print(f"📅 ANO:         {r.get('ano_publicacao', 'N/A')}")
            print(f"🏢 EDITORA:     {r.get('editora', 'N/A')}")
            print(f"📄 PÁGINAS:     {r.get('paginas', 'N/A')}")
            print(f"📍 LOCALIZAÇÃO: {r.get('localizacao', 'N/A')}")
            print(f"🚦 STATUS:      {r.get('status', 'N/A').upper()}")
        print("-" * 40)
    else:
        print("\n❌ Nenhum livro encontrado com esse termo.")

def alterar_livro():
    print("\n--- ALTERAR CADASTRO DE LIVRO ---")
    isbn_busca = input("Digite o ISBN exato do livro que deseja alterar: ").strip()
    
    livro_encontrado = None
    for livro in biblioteca:
        if livro['isbn'] == isbn_busca:
            livro_encontrado = livro
            break
    
    if not livro_encontrado:
        print("❌ Livro não encontrado com este ISBN.")
        return

    print(f"\nLivro Atual: {livro_encontrado['titulo']} - {livro_encontrado['autor']}")
    print("O que deseja alterar?")
    print("1. Título")
    print("2. Autor")
    print("3. Género")
    print("4. Ano de Publicação")
    print("5. Editora")
    print("6. Páginas")
    print("7. Localização")
    print("8. Status (disponivel/emprestado)")
    print("0. Cancelar")

    opcao = input("\nEscolha uma opção (0-8): ")

    if opcao == "0":
        return
    
    campos = {
        "1": "titulo",
        "2": "autor",
        "3": "genero",
        "4": "ano_publicacao",
        "5": "editora",
        "6": "paginas",
        "7": "localizacao",
        "8": "status"
    }

    if opcao in campos:
        chave = campos[opcao]
        novo_valor = input(f"Novo valor para {chave}: ").strip()
        
        if opcao in ["4", "6"]:
            try:
                novo_valor = int(novo_valor)
            except ValueError:
                print("❌ Erro: Este campo deve ser um número inteiro. Operação cancelada.")
                return

        livro_encontrado[chave] = novo_valor
        
        import dados
        dados.salvar_no_arquivo(biblioteca)
        
        print(f"\n✅ {chave.capitalize()} atualizado com sucesso!")
    else:
        print("❌ Opção inválida.")