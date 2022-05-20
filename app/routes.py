from flask import Flask, flash, request, redirect, url_for, render_template, jsonify, send_from_directory, make_response
import json
from app import app
from .views import empresa, helper, funcionario, funcionario_ponto, cargo
from .forms.cadastro_empresa import EmpresaCadastro
from .forms.login_empresa import EmpresaLogin
from .forms.cadastro_funcionario import FuncionarioCadastro
from .forms.cadastro_cargo import CargoCadastro

from app.api_logic import upload_face, facial_recognition, create_collection


@app.route('/')
def hello():
    return render_template('home_page.html', logado=helper.token_validate(request))


@app.route('/cadastro')
def hello2():
    return render_template('empresa_cadastro.html', logado=helper.token_validate(request))


@app.route('/registrar', methods=['GET', 'POST'])
def registro_empresa():
    logado = helper.token_validate(request)
    if not logado:
        form = EmpresaCadastro()
        if request.method == 'POST':
            return empresa.post_empresa(form)
    else:
        return redirect("/")

    return render_template('registro_empresa.html', form=form, error=None, logado=logado)


@app.route('/login', methods=['POST', 'GET'])
def authenticate():
    form = EmpresaLogin()
    if request.method == 'POST':
        return helper.auth(form)

    return render_template('login_empresa.html', form=form, error=None, logado=helper.token_validate(request))


@app.route('/logout', methods=['GET'])
def logout():
    resp = make_response(redirect('/'))
    resp.set_cookie('token', "")

    return resp


@app.route('/ponto', methods=['GET'])
@helper.token_required
def registra_ponto(current_user):
    return render_template('registro_ponto.html', logado=helper.token_validate(request))

@app.route('/ponto/<id>', methods=['GET'])
@helper.token_required
def cadastro_ponto(current_user, id):
    return render_template('cadastro_ponto.html', logado=helper.token_validate(request), id=id)


@app.route('/empresa', methods=['GET'])
@helper.token_required
def detalhe_empresa(current_user):
    return render_template('detalhe_empresa.html', logado=helper.token_validate(request), fCount=funcionario.count_funcionario_by_id_empresa(current_user.id_empresa), cCount=cargo.count_cargo_by_id_empresa(current_user.id_empresa))


@app.route('/funcionarios', methods=['GET'])
@helper.token_required
def detalhe_funcionario(current_user):
    logado = helper.token_validate(request)
    users = funcionario.funcionarios_by_empresa(current_user.id_empresa)
    return render_template('detalhe_funcionario.html', users=users, logado=logado)


@app.route('/funcionario', methods=['GET', 'POST'])
@helper.token_required
def registro_funcionario(current_user):
    logado = helper.token_validate(request)
    form = FuncionarioCadastro()
    countries_list = [(i.id_cargo, i.titulo) for i in cargo.cargo_by_id_empresa(current_user.id_empresa)]
    form.idCargo.choices = countries_list
    if request.method == 'POST':
        return funcionario.post_funcionario(form, current_user.id_empresa)

    return render_template('registro_funcionario.html', form=form, error=None, logado=logado)


@app.route('/cargos', methods=['GET'])
@helper.token_required
def detalhe_cargo(current_user):
    logado = helper.token_validate(request)
    users = cargo.cargo_by_id_empresa(current_user.id_empresa)
    return render_template('detalhe_cargo.html', users=users, logado=logado)


@app.route('/cargo', methods=['GET', 'POST'])
@helper.token_required
def registro_cargo(current_user):
    logado = helper.token_validate(request)
    form = CargoCadastro()
    if request.method == 'POST':
        return cargo.post_cargo(form, current_user.id_empresa)

    return render_template('registro_cargo.html', form=form, error=None, logado=logado)


@app.route('/create', methods=['GET', 'POST'])
@helper.token_required
def create():
    if request.method == 'POST':
        name = request.form['name'].replace(" ", "")
        response = create_collection(name)
        return response
    else:
        return jsonify({'message': 'Something went wrong'})


@app.route('/upload', methods=['GET', 'POST'])
@helper.token_required
def upload_file(current_user):
    if request.method == 'POST':

        file = request.form['file'].split(',')[1]
        name = request.form['name'].replace(" ", "")
        func = funcionario.funcionario_by_id(int(name))
        if func and func.id_empresa == current_user.id_empresa:
            response = upload_face(name=name, image=file)
            return response

        return jsonify({'message': 'Something went wrong'})
    else:
        return jsonify({'message': 'Something went wrong'})


@app.route('/compare', methods=['GET', 'POST'])
@helper.token_required
def compare_image(current_user):
    if request.method == 'POST':

        file = request.form['file'].split(',')[1]

        response = facial_recognition(image=file)
        data = json.loads(response.get_data().decode("utf-8"))
        print(data)

        if int(data['confidence']) < 90:
            return render_template('ponto_erro.html', logado=helper.token_validate(request))
        else:
            func = funcionario.funcionario_by_id(int(data['id']))
            if func and func.id_empresa == current_user.id_empresa:
                cria = funcionario_ponto.create_funcionario_ponto(func.id_funcionario)
                if cria:
                    return render_template('ponto_sucesso.html', user=funcionario.funcionario_by_id(int(func.nome)).nome, logado=helper.token_validate(request))
                else:
                    return render_template('ponto_erro.html', logado=helper.token_validate(request))
    else:
        return render_template('ponto_erro.html', logado=helper.token_validate(request))
