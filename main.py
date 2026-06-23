from flask import Flask, jsonify, request, render_template, redirect, url_for
import dados

biblioteca = dados.carregar_do_arquivo()

app = Flask(__name__)

# --- ROTA DA PÁGINA INICIAL (LISTAGEM + FORMULÁRIO DE DELETAR) ---
@app.route('/')
def pagina_inicial():
    return render_template('index.html', livros=biblioteca)

# --- ROTA PARA EXIBIR E PROCESSAR O FORMULÁRIO DE CADASTRO ---
@app.route('/livro/novo', methods=['GET', 'POST'])
def novo_livro_web():
    if request.method == 'POST':
        # Coleta os dados vindos do formulário HTML
        isbn = request.form.get('isbn').strip()
        
        # Validação simples de duplicidade
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

# --- ROTA PARA EXIBIR E PROCESSAR O FORMULÁRIO DE ATUALIZAÇÃO ---
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

# --- ROTA PARA PROCESSAR A REMOÇÃO (DELETAR) ---
@app.route('/livro/deletar/<isbn>', methods=['POST'])
def deletar_livro_web(isbn):
    for livro in biblioteca:
        if livro['isbn'] == isbn:
            biblioteca.remove(livro)
            dados.salvar_no_arquivo(biblioteca)
            break
    return redirect(url_for('pagina_inicial'))


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