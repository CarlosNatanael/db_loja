from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Produto, Movimentacao

app = Flask(__name__)

app.config['SECRET_KEY'] = 'chave_secreta_para_mensagens_flash'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

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

# Registra a movimentação de entrada e saida
@app.route('/movimentar/<int:id_produto>/<tipo>', methods=['GET', 'POST'])
def movimentar(id_produto, tipo):
    produto = Produto.query.get_or_404(id_produto)
    
    if request.method == 'POST':
        quantidade = int(request.form.get('quantidade'))
        
        if tipo == 'S' and quantidade > produto.quantidade_atual:
            flash(f'Erro: Estoque insuficiente. Você só tem {produto.quantidade_atual} un.', 'error')
            return redirect(url_for('movimentar', id_produto=produto.id, tipo=tipo))

        nova_movimentacao = Movimentacao(produto_id=produto.id, tipo=tipo, quantidade=quantidade)
        db.session.add(nova_movimentacao)

        if tipo == 'E':
            produto.quantidade_atual += quantidade
            flash(f'Entrada de {quantidade} un. registrada com sucesso!', 'success')
        elif tipo == 'S':
            produto.quantidade_atual -= quantidade
            flash(f'Saída de {quantidade} un. registrada com sucesso!', 'success')
            
        db.session.commit()
        return redirect(url_for('index'))
        
    return render_template('movimentar.html', produto=produto, tipo=tipo)

# Registra entrada e saida
@app.route('/historico')
def historico():
    movimentacoes = Movimentacao.query.order_by(Movimentacao.data_hora.desc()).all()
    return render_template('historico.html', movimentacoes=movimentacoes)

if __name__ == '__main__':
    app.run(debug=True)