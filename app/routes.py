from flask import Flask, flash, request, redirect, url_for, render_template, jsonify, send_from_directory
import base64
import os
import boto3
from werkzeug.utils import secure_filename
import json
from app import app

from app.api_logic import upload_face, facial_recognition, create_collection


@app.route('/')
def hello():
    return render_template('login_form.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        file = request.form['file'].split(',')[1]
        name = request.form['name'].replace(" ", "")

        response = upload_face(name=name, image=file)

        return response
    else:
        return jsonify({'message': 'Something went wrong'})


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':

        name = request.form['name'].replace(" ", "")

        response = create_collection(name)

        return response
    else:
        return jsonify({'message': 'Something went wrong'})


@app.route('/compare', methods=['GET', 'POST'])
def compare_image():
    if request.method == 'POST':

        file = request.form['file'].split(',')[1]

        response = facial_recognition(image=file)
        data = json.loads(response.get_data().decode("utf-8"))
        print(data)
        if int(data['confidence']) < 60:
            return render_template('login_form.html');
        else:
            return render_template('admin_panel.html', user=data['id'])
    else:
        return render_template('login_form.html');


