from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo

# Instanciamos o banco de dados
db = SQLAlchemy()

def hora_brasilia():
    return datetime.now(ZoneInfo("America/Sao_Paulo"))

class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False, default=0.0)
    quantidade_atual = db.Column(db.Integer, nullable=False, default=0)
    movimentacoes = db.relationship('Movimentacao', backref='produto', lazy=True)

    def __repr__(self):
        return f'<Produto {self.nome}>'

class Movimentacao(db.Model):
    __tablename__ = 'movimentacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    
    # 'E' para Entrada, 'S' para Saída
    tipo = db.Column(db.String(1), nullable=False) 
    quantidade = db.Column(db.Integer, nullable=False)
    
    cliente = db.Column(db.String(100), nullable=True)
    data_hora = db.Column(db.DateTime, nullable=False, default=hora_brasilia)

    def __repr__(self):
        return f'<Movimentacao {self.tipo} - {self.quantidade} un.>'