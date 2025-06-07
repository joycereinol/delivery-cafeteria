
from flask import Flask, render_template, request, redirect, url_for
from models import db, Produto, Pedido

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafeteria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form['nome']
    preco = float(request.form['preco'])
    novo_produto = Produto(nome=nome, preco=preco)
    db.session.add(novo_produto)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    produto = Produto.query.get(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/pedidos')
def pedidos():
    pedidos = Pedido.query.all()
    return render_template('pedidos.html', pedidos=pedidos)

@app.route('/fazer_pedido', methods=['POST'])
def fazer_pedido():
    produto_id = request.form['produto_id']
    novo_pedido = Pedido(produto_id=produto_id)
    db.session.add(novo_pedido)
    db.session.commit()
    return redirect(url_for('pedidos'))

if __name__ == '__main__':
    app.run(debug=True)
