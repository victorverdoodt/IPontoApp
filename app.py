from flask import Flask, flash, request, redirect, url_for, render_template, jsonify, send_from_directory
import base64
import os
import boto3
from werkzeug.utils import secure_filename

from face import upload_face, facial_recognition

UPLOAD_FOLDER = './static/img'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        file = request.form['file'].split(',')[1]
        name = request.form['name'].replace(" ", "")

        response = upload_face(name=name, image=file)

        if file and allowed_file(file_name):
            filename = secure_filename(file_name)
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "wb") as fh:
                fh.write(base64.b64decode(file))

        return response
    else:
        return jsonify({'message': 'Something went wrong'})

@app.route('/create', methods=['GET', 'POST'])
def create_collection():
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
        return response
    else:
        return jsonify({'message': 'Something went wrong'})


app.secret_key = '<SOMETHING_SUPER_SECRET>'

if __name__ == '__main__':
    app.run()
