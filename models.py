from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False, default=0.0)
    quantidade_atual = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<Produto {self.nome}>'

class Movimentacao(db.Model):
    id = db.Column(db.Integer)