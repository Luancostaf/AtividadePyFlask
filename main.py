from flask import Flask, jsonify, request, render_template
import dados

biblioteca = dados.carregar_do_arquivo()

app = Flask(__name__)

# --- Nova rota adicionada para a página inicial ---
@app.route('/')
def pagina_inicial():
    return render_template('index.html', livros=biblioteca)

# Unificamos os endpoints e declaramos todos os métodos aceitos
@app.route('/biblioteca', methods=['GET', 'POST'])
@app.route('/biblioteca/<isbn>', methods=['GET', 'PUT', 'DELETE'])
def gerenciar_biblioteca(isbn=None):
    
    if request.method == 'GET':
        if isbn is None:
            return jsonify(biblioteca)
        
        for livro in biblioteca:
            if livro['isbn'] == isbn:
                return jsonify(livro)
        return jsonify("Livro não encontrado"), 404

    elif request.method == 'POST':
        novo_livro = request.get_json()
        biblioteca.append(novo_livro)
        dados.salvar_no_arquivo(biblioteca)
        return jsonify("Livro criado com sucesso"), 201

    elif request.method == 'PUT':
        novo_livro = request.get_json()
        for livro in biblioteca:
            if livro['isbn'] == isbn:
                livro.update(novo_livro) 
                dados.salvar_no_arquivo(biblioteca)
                return jsonify("Livro alterado com sucesso"), 200
        return jsonify("Livro não encontrado para atualização"), 404

    elif request.method == 'DELETE':
        for livro in biblioteca:
            if livro['isbn'] == isbn:
                biblioteca.remove(livro)
                dados.salvar_no_arquivo(biblioteca)
                return jsonify("Livro deletado com sucesso"), 200
        return jsonify("Livro não encontrado para remoção"), 404

if __name__ == '__main__':
    app.run(debug=True)
