from werkzeug.security import generate_password_hash
from app import db
from datetime import date, datetime, timedelta
from flask import request, jsonify

from ..models.funcionario import Funcionario
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
    today = date.today()
    first = today.replace(day=1)

    #last_month_last_day = first - timedelta(days=1)
    #last_month_first_day = last_month_last_day.replace(day=1)

    result = Funcionario_ponto.query.with_entities(Funcionario_ponto.id_funcionario, Funcionario.nome, func.strftime("%Y-%m-%d %H:%M", Funcionario_ponto.data_criacao).label("data_criacao")).filter(
        Funcionario_ponto.id_empresa == id_empresa and Funcionario_ponto.id_funcionario == id_funcionario and today >= Funcionario_ponto.data_criacao >= first) \
        .join(Funcionario, Funcionario.id_funcionario == Funcionario_ponto.id_funcionario, isouter=True) \
        .order_by(Funcionario_ponto.data_criacao).all()

    return result
