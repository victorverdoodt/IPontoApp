from flask import Flask, flash, request, redirect, url_for, render_template, jsonify, send_from_directory
import base64
import os
import boto3
from werkzeug.utils import secure_filename
import json
from app import app
from .views import empresa, helper, funcionario, funcionario_ponto

from app.api_logic import upload_face, facial_recognition, create_collection


@app.route('/')
def hello():
    return render_template('login_form.html')


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
            return render_template('login_form.html');
        else:
            func = funcionario.funcionario_by_id(int(data['id']))
            if func and func.id_empresa == current_user.id_empresa:
                funcionario_ponto.create_funcionario_ponto(func.id_funcionario)
                return render_template('admin_panel.html', user=func.nome)
    else:
        return render_template('login_form.html');


@app.route('/authenticate', methods=['POST'])
def authenticate():
    return helper.auth()


@app.route('/empresa', methods=['POST'])
def post_empresa():
    return empresa.post_empresa()


