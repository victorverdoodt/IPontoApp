from werkzeug.security import generate_password_hash
from app import db
from flask import request, jsonify
from ..models.funcionario import Funcionario, funcionario_schema, funcionarios_schema


def funcionario_by_id(id):
    try:
        return Funcionario.query.filter(Funcionario.id_funcionario == id).one()
    except:
        return None


def funcionario_by_cpf(cpf):
    try:
        return Funcionario.query.filter(Funcionario.cpf == cpf).one()
    except:
        return None


def create_funcionario(nome, cpf, senha, id_cargo, id_empresa):
    funcionario = Funcionario(nome, cpf, senha, id_cargo, id_empresa)

    try:
        db.session.add(funcionario)
        db.session.commit()
        return True
    except:
        return False
