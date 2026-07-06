from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Produto, Movimentacao

app = Flask(__name__)

# Configurações básicas
app.config['SECRET_KEY'] = 'chave_secreta_para_mensagens_flash'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Conecta o banco de dados criado no models.py com este app Flask
db.init_app(app)

# Cria as tabelas dentro do contexto da aplicação
with app.app_context():
    db.create_all()
    
    # Dica: Adiciona um produto de teste se a tabela estiver vazia
    if not Produto.query.first():
        produto_teste = Produto(nome="Cabo USB-C", preco=25.90, quantidade_atual=0)
        db.session.add(produto_teste)
        db.session.commit()

# Rota principal
@app.route('/')
def index():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)

# Rota para cadastrar um novo produto
@app.route('/novo_produto', methods=['GET', 'POST'])
def novo_produto():
    if request.method == 'POST':
        nome = request.form.get('nome')
        preco_str = request.form.get('preco').replace(',', '.')
        
        try:
            preco = float(preco_str)
            novo = Produto(nome=nome, preco=preco, quantidade_atual=0)
            db.session.add(novo)
            db.session.commit()
            flash(f'Produto "{nome}" cadastrado com sucesso!', 'success')
            return redirect(url_for('index'))
            
        except ValueError:
            flash('Erro: O preço digitado é inválido.', 'error')
            return redirect(url_for('novo_produto'))
    return render_template('novo_produto.html')

if __name__ == '__main__':
    app.run(debug=True)