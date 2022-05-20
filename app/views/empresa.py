from werkzeug.security import generate_password_hash
from app import db
from flask import request, jsonify, url_for, flash, redirect, render_template
from ..models.empresa import Empresa, empresa_schema, empresas_schema
from ..forms.cadastro_empresa import EmpresaCadastro
from validate_docbr import CNPJ

cnpj = CNPJ()


def get_empresas():
    name = request.args.get('name')
    if name:
        empresa = Empresa.query.filter(Empresa.name.like(f'%{name}%')).all()
    else:
        empresa = Empresa.query.all()
    if empresa:
        result = empresas_schema.dump(empresa)
        return jsonify({'message': 'successfully fetched', 'data': result.data})

    return jsonify({'message': 'nothing found', 'data': {}})


def get_empresa(id):
    empresa = Empresa.query.get(id)
    if empresa:
        result = empresa_schema.dump(empresa)
        return jsonify({'message': 'successfully fetched', 'data': result.data}), 201

    return jsonify({'message': "user don't exist", 'data': {}}), 404


def post_empresa(form):
    empresa = empresa_by_cnpj(form.cnpj.data)
    if empresa:
        return render_template('registro_empresa.html', form=form, error="CNPJ já cadastrado")

    if not cnpj.validate(form.cnpj.data):
        return render_template('registro_empresa.html', form=form, error="CNPJ invalido")

    pass_hash = generate_password_hash(form.senha.data)
    empresa = Empresa(form.email.data, pass_hash, form.cnpj.data, form.nome.data)

    try:
        db.session.add(empresa)
        db.session.commit()
        return redirect('/login')
    except:
        return render_template('registro_empresa.html', form=form, error="Algo deu errado")

    return render_template('registro_empresa.html', form=form, error=None)


def update_empresa(id):
    nome = request.json['nome']
    email = request.json['email']
    cnpj = request.json['cnpj']
    senha = request.json['senha']
    empresa = Empresa.query.get(id)

    if not empresa:
        return jsonify({'message': "user don't exist", 'data': {}}), 404

    pass_hash = generate_password_hash(senha)

    if empresa:
        try:
            empresa.username = nome
            empresa.password = pass_hash
            empresa.cnpj = cnpj
            empresa.email = email
            db.session.commit()
            result = empresa_schema.dump(empresa)
            return jsonify({'message': 'successfully updated', 'data': result.data}), 201
        except:
            return jsonify({'message': 'unable to update', 'data': {}}), 500


def delete_empresa(id):
    empresa = Empresa.query.get(id)
    if not empresa:
        return jsonify({'message': "user don't exist", 'data': {}}), 404

    if empresa:
        try:
            db.session.delete(empresa)
            db.session.commit()
            result = empresa_schema.dump(empresa)
            return jsonify({'message': 'successfully deleted', 'data': result.data}), 200
        except:
            return jsonify({'message': 'unable to delete', 'data': {}}), 500


def empresa_by_cnpj(cnpj):
    try:
        return Empresa.query.filter(Empresa.cnpj == cnpj).one()
    except:
        return None
