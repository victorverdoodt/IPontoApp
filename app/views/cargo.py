from werkzeug.security import generate_password_hash
from app import db
from flask import request, jsonify, redirect, render_template
from ..models.cargo import Cargo, cargo_schema, cargos_schema


def cargo_by_id(id):
    try:
        return Cargo.query.filter(Cargo.id_cargo == id).one()
    except:
        return None


def cargo_by_id_empresa(id_empresa):
    try:
        return Cargo.query.filter(Cargo.id_empresa == id_empresa)
    except:
        return None


def create_cargo(titulo, descricao, id_empresa, hora_entrada, hora_almoco, hora_saida):
    cargo = Cargo(titulo, descricao, id_empresa, hora_entrada, hora_almoco, hora_saida)

    try:
        db.session.add(cargo)
        db.session.commit()
        return True
    except:
        return False


def post_cargo(form, idEmpresa):
    funcionario = create_cargo(form.titulo.data, form.descricao.data, idEmpresa, form.hora_entrada.data, form.hora_almoco.data, form.hora_saida.data)
    if funcionario:
        return redirect('/empresa')
    else:
        return render_template('registro_cargo.html', form=form, error="user already exists")

    return render_template('registro_cargo.html', form=form, error="Algo deu errado")
