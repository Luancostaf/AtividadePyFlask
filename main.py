from flask import Flask, jsonify, request, render_template, redirect, url_for
import dados

biblioteca = dados.carregar_do_arquivo()

app = Flask(__name__)

# Rota da página inicial (listagem + formulário de deletar)
@app.route('/')
def pagina_inicial():
    return render_template('index.html', livros=biblioteca)

# Rota para exibir e processar o formulário de cadastro
@app.route('/livro/novo', methods=['GET', 'POST'])
def novo_livro_web():
    if request.method == 'POST':
        isbn = request.form.get('isbn').strip()
        
        for livro in biblioteca:
            if livro['isbn'] == isbn:
                return "⚠️ ERRO: Já existe um livro cadastrado com este ISBN!", 400

        novo = {
            "isbn": isbn,
            "titulo": request.form.get('titulo').strip(),
            "autor": request.form.get('autor').strip(),
            "genero": request.form.get('genero').strip(),
            "ano_publicacao": int(request.form.get('ano_publicacao')),
            "editora": request.form.get('editora').strip(),
            "paginas": int(request.form.get('paginas')),
            "status": "disponivel", 
            "localizacao": request.form.get('localizacao').strip()
        }
        
        biblioteca.append(novo)
        dados.salvar_no_arquivo(biblioteca)
        return redirect(url_for('pagina_inicial'))
        
    return render_template('cadastro.html')

# Rota para exibir e processar o formulário de atualização
@app.route('/livro/editar/<isbn>', methods=['GET', 'POST'])
def editar_livro_web(isbn):
    livro_encontrado = None
    for livro in biblioteca:
        if livro['isbn'] == isbn:
            livro_encontrado = livro
            break
            
    if not livro_encontrado:
        return "❌ Livro não encontrado", 404

    if request.method == 'POST':
        livro_encontrado['titulo'] = request.form.get('titulo').strip()
        livro_encontrado['autor'] = request.form.get('autor').strip()
        livro_encontrado['genero'] = request.form.get('genero').strip()
        livro_encontrado['ano_publicacao'] = int(request.form.get('ano_publicacao'))
        livro_encontrado['editora'] = request.form.get('editora').strip()
        livro_encontrado['paginas'] = int(request.form.get('paginas'))
        livro_encontrado['localizacao'] = request.form.get('localizacao').strip()
        livro_encontrado['status'] = request.form.get('status')
        
        dados.salvar_no_arquivo(biblioteca)
        return redirect(url_for('pagina_inicial'))

    return render_template('editar.html', livro=livro_encontrado)

# Rota para processar a remoção (deletar)
@app.route('/livro/deletar/<isbn>', methods=['POST'])
def deletar_livro_web(isbn):
    for livro in biblioteca:
        if livro['isbn'] == isbn:
            biblioteca.remove(livro)
            dados.salvar_no_arquivo(biblioteca)
            break
    return redirect(url_for('pagina_inicial'))

@app.route('/atualizar', methods=['GET', 'POST'])
def atualizar_livro_web():
    # Pegando o ISBN passado na URL (Ex: /atualizar?isbn=12345)
    isbn_busca = request.args.get('isbn')
    
    # Localizar o livro correspondente na biblioteca
    livro_encontrado = None
    for livro in biblioteca:
        if livro['isbn'] == isbn_busca:
            livro_encontrado = livro
            break

    if not livro_encontrado:
        return "❌ Livro não encontrado no acervo.", 404

    # Se o usuário preencheu o formulário e clicou em "Salvar"
    if request.method == 'POST':
        livro_encontrado['titulo'] = request.form.get('titulo').strip()
        livro_encontrado['autor'] = request.form.get('autor').strip()
        livro_encontrado['genero'] = request.form.get('genero').strip()
        livro_encontrado['ano_publicacao'] = int(request.form.get('ano_publicacao'))
        livro_encontrado['editora'] = request.form.get('editora').strip()
        livro_encontrado['paginas'] = int(request.form.get('paginas'))
        livro_encontrado['localizacao'] = request.form.get('localizacao').strip()
        livro_encontrado['status'] = request.form.get('status')
        
        # Salva as alterações de volta no arquivo JSON
        dados.salvar_no_arquivo(biblioteca)
        
        # Redireciona de volta para a tabela da página inicial
        return redirect(url_for('pagina_inicial'))

    # Se for um acesso via GET, apenas exibe o formulário com os dados atuais do livro
    return render_template('atualizar.html', livro=livro_encontrado)

# --- (Mantidos os seus endpoints originais da API abaixo para não quebrar o código anterior) ---
@app.route('/biblioteca', methods=['GET', 'POST'])
@app.route('/biblioteca/<isbn>', methods=['GET', 'PUT', 'DELETE'])
def gerenciar_biblioteca(isbn=None):
    # ... Seu código antigo de API em JSON permanece aqui se desejar ...
    if request.method == 'GET':
        if isbn is None: return jsonify(biblioteca)
        for l in biblioteca:
            if l['isbn'] == isbn: return jsonify(l)
        return jsonify("Livro não encontrado"), 404
    # ... (restante do método gerenciar_biblioteca)

if __name__ == '__main__':
    app.run(debug=True)