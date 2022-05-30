from werkzeug.security import generate_password_hash
from app import db
from flask import request, jsonify, render_template, redirect
from ..models.funcionario import Funcionario, funcionario_schema, funcionarios_schema
from sqlalchemy import func
from validate_docbr import CPF

cpf = CPF()


def funcionario_by_id(id):
    try:
        return Funcionario.query.filter(Funcionario.id_funcionario == id).filter(Funcionario.id_status == 1).one()
    except:
        return None


def funcionario_by_cpf(cpf):
    try:
        return Funcionario.query.filter(Funcionario.cpf == cpf).filter(Funcionario.id_status == 1).one()
    except:
        return None


def funcionarios_by_empresa(idEmpresa):
    try:
        return Funcionario.query.filter(Funcionario.id_empresa == idEmpresa).filter(Funcionario.id_status == 1).all()
    except:
        return None


def create_funcionario(nome, cpf, senha, email, id_cargo, id_empresa):
    funcionario = Funcionario(nome, cpf, senha, email, id_cargo, id_empresa, 1)
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
        return Funcionario.query.filter(
            Funcionario.id_empresa == id_empresa and Funcionario.id_status == 1).with_entities(func.count()).scalar()
    except:
        return 0


def post_funcionario(form, idEmpresa):
    if not cpf.validate(form.cpf.data):
        return render_template('registro_funcionario.html', form=form, error="CPF invalido")

    pass_hash = generate_password_hash(form.senha.data)
    funcionario = create_funcionario(form.nome.data, form.cpf.data, pass_hash, form.email.data, form.idCargo.data,
                                     idEmpresa)
    if funcionario:
        return redirect('/funcionarios')
    else:
        return render_template('registro_funcionario.html', form=form, error="Funcionario já existe")

    return render_template('registro_funcionario.html', form=form, error="Algo deu errado")


def update_funcionario(form):
    if not cpf.validate(form.cpf.data):
        return render_template('editar_funcionario.html', form=form, error="CPF invalido")

    funcionario = funcionario_by_cpf(form.cpf.data)
    if funcionario:

        if len(form.senha.data) > 3:
            pass_hash = generate_password_hash(form.senha.data)
            if pass_hash != funcionario.senha:
                funcionario.senha = pass_hash

        if len(form.nome.data) > 3 and funcionario.nome != form.nome.data:
            funcionario.nome = form.nome.data
        if form.idCargo.data != funcionario.id_cargo:
            funcionario.id_cargo = form.idCargo.data
        if len(form.email.data) > 3 and form.email.data != funcionario.email:
            funcionario.email = form.email

        if form.desabilitado.data:
            funcionario.id_status = 0

        db.session.commit()

        return redirect('/funcionarios')

    return render_template('registro_funcionario.html', form=form, error="Algo deu errado")
