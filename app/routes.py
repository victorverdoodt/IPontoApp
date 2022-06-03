from flask import Flask, flash, request, redirect, url_for, render_template, jsonify, send_from_directory, make_response
import json
from app import app
from .Helpers import elasticemail
from .views import empresa, helper, funcionario, funcionario_ponto, cargo
from .forms.cadastro_empresa import EmpresaCadastro
from .forms.login_empresa import EmpresaLogin
from .forms.login_funcionario import FuncionarioLogin
from .forms.cadastro_funcionario import FuncionarioCadastro
from .forms.editar_funcionario import FuncionarioEdiar
from .forms.cadastro_cargo import CargoCadastro
import datetime
from app.api_logic import upload_face, facial_recognition, create_collection
import flask_excel as excel
import numpy as np

excel.init_excel(app)


@app.route('/')
def hello():
    logado = helper.token_validate(request)
    if not logado:
        return render_template('home_page.html', logado=logado, title="IPonto - Bem-vindo!")
    else:
        return redirect('/empresa')


@app.route('/detalhes')
@helper.token_required
def hellof(current_user):
    if current_user[1] == 1:
        logado = helper.token_validate(request)
        ponto = funcionario_ponto.funcionario_ponto_by_id_funcionario(current_user[0].id_funcionario)
        return render_template('detalhes.html', logado=logado, title="Dashboard - funcionario!", users=ponto)
    else:
        redirect('/empresa')


@app.route('/cadastro')
def hello2():
    return render_template('empresa_cadastro.html', logado=helper.token_validate(request), title="Cadastrar empresa")


@app.route('/registrar', methods=['GET', 'POST'])
def registro_empresa():
    logado = helper.token_validate(request)
    if not logado:
        form = EmpresaCadastro()
        if request.method == 'POST':
            return empresa.post_empresa(form)
    else:
        return redirect("/")

    return render_template('registro_empresa.html', form=form, error=None, logado=logado, title="Cadastro empresa")


@app.route('/login', methods=['POST', 'GET'])
def authenticate():
    form = EmpresaLogin()
    if request.method == 'POST':
        return helper.auth(form, True)

    return render_template('login_empresa.html', form=form, error=None, logado=helper.token_validate(request),
                           title="Login Empresa")


@app.route('/loginfuncionario', methods=['POST', 'GET'])
def authenticatef():
    form = FuncionarioLogin()
    if request.method == 'POST':
        return helper.auth(form, False)

    return render_template('login_funcionario.html', form=form, error=None, logado=helper.token_validate(request),
                           title="Login funcionario")


@app.route('/logout', methods=['GET'])
def logout():
    resp = make_response(redirect('/'))
    resp.set_cookie('token', "")

    return resp


@app.route('/ponto', methods=['GET'])
@helper.token_required
def registra_ponto(current_user):
    return render_template('registro_ponto.html', logado=helper.token_validate(request), title="Registrar ponto")


@app.route('/ponto/<id>', methods=['GET'])
@helper.token_required
def cadastro_ponto(current_user, id):
    return render_template('cadastro_ponto.html', logado=helper.token_validate(request), id=id, title="Cadastrar foto")


@app.route('/ponto/<id>/relatorio', methods=['GET'])
@helper.token_required
def relatorio_ponto(current_user, id):
    if current_user[1] == 0:
        ret = funcionario_ponto.funcionario_ponto_relatorio(current_user[0].id_empresa, id)
        if ret:
            column_names = ['id_funcionario', 'nome', 'data_criacao']
            return excel.make_response_from_query_sets(ret, column_names, "xlsx", file_name="relatorio" + str(id))
        return redirect('/funcionarios')

    return redirect('/detalhes')


@app.route('/empresa', methods=['GET'])
@helper.token_required
def detalhe_empresa(current_user):
    if current_user[1] == 0:
        return render_template('detalhe_empresa.html', logado=helper.token_validate(request),
                               fCount=funcionario.count_funcionario_by_id_empresa(current_user[0].id_empresa),
                               cCount=cargo.count_cargo_by_id_empresa(current_user[0].id_empresa),
                               nome=current_user[0].nome, title="Dashboard - Empresa")

    return redirect('/detalhes')


@app.route('/funcionarios', methods=['GET'])
@helper.token_required
def detalhe_funcionario(current_user):
    if current_user[1] == 0:
        logado = helper.token_validate(request)
        users = funcionario.funcionarios_by_empresa(current_user[0].id_empresa)

        if cargo.count_cargo_by_id_empresa(current_user[0].id_empresa) <= 0:
            return render_template('funcionario_erro.html', logado=logado, title="Erro em cargos")

        return render_template('detalhe_funcionario.html', users=users, logado=logado, title="Funcionarios")

    return redirect('/detalhes')


@app.route('/funcionario', methods=['GET', 'POST'])
@helper.token_required
def registro_funcionario(current_user):
    if current_user[1] == 0:

        logado = helper.token_validate(request)
        form = FuncionarioCadastro()
        if cargo.count_cargo_by_id_empresa(current_user[0].id_empresa) <= 0:
            return render_template('funcionario_erro.html', logado=logado, title="Erro em cargos")

        countries_list = [(i.id_cargo, i.titulo) for i in cargo.cargo_by_id_empresa(current_user[0].id_empresa)]
        form.idCargo.choices = countries_list
        if request.method == 'POST':
            return funcionario.post_funcionario(form, current_user[0].id_empresa)

        return render_template('registro_funcionario.html', form=form, error=None, logado=logado,
                               title="Cadastro funcionario")

    return redirect('/detalhes')


@app.route('/funcionario/<id>/editar', methods=['GET', 'POST'])
@helper.token_required
def editar_funcionario(current_user, id):
    if current_user[1] == 0:
        logado = helper.token_validate(request)
        form = FuncionarioEdiar()
        if request.method == 'GET':
            countries_list = [(i.id_cargo, i.titulo) for i in cargo.cargo_by_id_empresa(current_user[0].id_empresa)]
            form.idCargo.choices = countries_list
            funci = funcionario.funcionario_by_id(id)
            if funci:
                form.senha.data = ""
                form.nome.data = funci.nome
                form.idCargo.data = funci.id_cargo
                form.cpf.data = funci.cpf
                form.email.data = funci.email

        if request.method == 'POST':
            funci = funcionario.funcionario_by_id(id)
            if funci:
                form.cpf.data = funci.cpf
            return funcionario.update_funcionario(form)

        return render_template('editar_funcionario.html', form=form, error=None, logado=logado, id=id,
                               title="Editar funcionario")

    return redirect('/detalhes')


@app.route('/cargos', methods=['GET'])
@helper.token_required
def detalhe_cargo(current_user):
    if current_user[1] == 0:
        logado = helper.token_validate(request)
        users = cargo.cargo_by_id_empresa(current_user[0].id_empresa)
        return render_template('detalhe_cargo.html', users=users, logado=logado, title="Cargos")

    return redirect('/detalhes')


@app.route('/cargo', methods=['GET', 'POST'])
@helper.token_required
def registro_cargo(current_user):
    if current_user[1] == 0:
        logado = helper.token_validate(request)
        form = CargoCadastro()
        if request.method == 'POST':
            return cargo.post_cargo(form, current_user[0].id_empresa)

        return render_template('registro_cargo.html', form=form, error=None, logado=logado, title="Registrar cargo")
    return redirect('/detalhes')


@app.route('/cargo/<id>/desabilitar', methods=['GET', 'POST'])
@helper.token_required
def desativar_cargo(current_user, id):
    if current_user[1] == 0:
        return cargo.desativar_cargo(id, current_user[0].id_empresa)

    return redirect('/detalhes')


@app.route('/create', methods=['GET', 'POST'])
@helper.token_required
def create(current_user):
    if current_user[1] == 0:
        if request.method == 'POST':
            name = request.form['name'].replace(" ", "")
            response = create_collection(name)
            return response
        else:
            return jsonify({'message': 'Something went wrong'})

    return redirect('/detalhes')


@app.route('/upload', methods=['GET', 'POST'])
@helper.token_required
def upload_file(current_user):
    if current_user[1] == 0:
        if request.method == 'POST':

            file = request.form['file'].split(',')[1]
            name = request.form['name'].replace(" ", "")
            func = funcionario.funcionario_by_id(int(name))
            if func and func.id_empresa == current_user[0].id_empresa:
                r = upload_face(name=name, image=file)
                data = json.loads(r.get_data().decode("utf-8"))
                if data['message'] == 'Face Uploaded!':
                    return render_template('registro_sucesso.html', logado=helper.token_validate(request),
                                           user=func.nome, title="Sucesso")
                else:
                    return render_template('registro_erro.html', logado=helper.token_validate(request), title="Erro")

            return render_template('registro_erro.html', logado=helper.token_validate(request), title="Erro")
        else:
            return render_template('registro_erro.html', logado=helper.token_validate(request), title="Erro")
    return redirect('/detalhes')


@app.route('/compare', methods=['GET', 'POST'])
@helper.token_required
def compare_image(current_user):
    if current_user[1] == 0:
        if request.method == 'POST':

            file = request.form['file'].split(',')[1]

            response = facial_recognition(image=file)
            data = json.loads(response.get_data().decode("utf-8"))
            if data['message'] == 'Face Found!':
                if int(data['confidence']) < 90:
                    return render_template('ponto_erro.html', logado=helper.token_validate(request), title="Erro")
                else:
                    func = funcionario.funcionario_by_id(int(data['id']))
                    if func and func.id_empresa == current_user[0].id_empresa:
                        funcionario_ponto.create_funcionario_ponto(func.id_funcionario, current_user[0].id_empresa)
                        # send simple email to one recipient
                        r = elasticemail.send(
                            func.email,
                            "Registro de ponto",
                            func.nome + ", Seu ponto foi registrado as " + str(datetime.datetime.now())
                        )
                        return render_template('ponto_sucesso.html',
                                               user=func.nome,
                                               data=datetime.datetime.now(),
                                               logado=helper.token_validate(request), title="Sucesso")
            else:
                return render_template('ponto_erro.html', logado=helper.token_validate(request), title="Erro")
        else:
            return render_template('ponto_erro.html', logado=helper.token_validate(request), title="Erro")

    return redirect('/detalhes')
