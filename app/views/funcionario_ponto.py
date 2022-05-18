from werkzeug.security import generate_password_hash
from app import db
from flask import request, jsonify
from ..models.funcionario_ponto import Funcionario_ponto, funcionario_ponto_schema, funcionario_pontos_schema


def funcionario_ponto_by_id(id):
    try:
        return Funcionario_ponto.query.filter(Funcionario_ponto.id_funcionario_ponto == id).one()
    except:
        return None


def funcionario_ponto_by_id_funcionario(id_funcionario):
    try:
        return Funcionario_ponto.query.filter(Funcionario_ponto.id_funcionario == id_funcionario)
    except:
        return None


def create_funcionario_ponto(id_funcionario):
    funcionario_ponto = Funcionario_ponto(id_funcionario=id_funcionario)

    try:
        db.session.add(funcionario_ponto)
        db.session.commit()
        return True
    except:
        return False
