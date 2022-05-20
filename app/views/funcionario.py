from werkzeug.security import generate_password_hash
from app import db
from flask import request, jsonify, render_template, redirect
from ..models.funcionario import Funcionario, funcionario_schema, funcionarios_schema
from sqlalchemy import func
from validate_docbr import CPF

cpf = CPF()

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


def funcionarios_by_empresa(idEmpresa):
    try:
        return Funcionario.query.filter(Funcionario.id_empresa == idEmpresa)
    except:
        return None


def create_funcionario(nome, cpf, senha, email, id_cargo, id_empresa):
    funcionario = Funcionario(nome, cpf, senha, email, id_cargo, id_empresa)
    if funcionario:
        try:
            db.session.add(funcionario)
            db.session.commit()
            return True
        except:
            return False
    return False


def count_funcionario_by_id_empresa(id_empresa):
    try:
        return Funcionario.query.filter(Funcionario.id_empresa == id_empresa).with_entities(func.count()).scalar()
    except:
        return 0


def post_funcionario(form, idEmpresa):
    if not cpf.validate(form.cpf.data):
        return render_template('registro_funcionario.html', form=form, error="CPF invalido")

    funcionario = create_funcionario(form.nome.data, form.cpf.data, form.senha.data, form.email.data, form.idCargo.data, idEmpresa)
    if funcionario:
        return redirect('/funcionarios')
    else:
        return render_template('registro_funcionario.html', form=form, error="Funcionario já existe")

    return render_template('registro_funcionario.html', form=form, error="Algo deu errado")



