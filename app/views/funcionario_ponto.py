from werkzeug.security import generate_password_hash
from app import db
from flask import request, jsonify
from ..models.funcionario_ponto import Funcionario_ponto, funcionario_ponto_schema, funcionario_pontos_schema
from sqlalchemy import func, extract
from itertools import groupby


def grouper(item):
    return item.data_criacao.year, item.data_criacao.month, item.data_criacao.day


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


def funcionario_ponto_by_id_empresa(id_empresa):
    try:
        return Funcionario_ponto.query.filter(Funcionario_ponto.id_empresa == id_empresa)
    except:
        return None


def create_funcionario_ponto(id_funcionario, id_empresa):
    funcionario_ponto = Funcionario_ponto(id_funcionario=id_funcionario, id_empresa=id_empresa)

    try:
        db.session.add(funcionario_ponto)
        db.session.commit()
        return True
    except:
        return False


def funcionario_ponto_relatorio(id_empresa, id_funcionario):
    result = Funcionario_ponto.query.with_entities(Funcionario_ponto.data_criacao, func.count(Funcionario_ponto.data_criacao)) \
                  .filter(Funcionario_ponto.id_empresa == id_empresa and Funcionario_ponto.id_funcionario == id_funcionario) \
                  .group_by(extract('day', Funcionario_ponto.data_criacao)).all()

    return result
