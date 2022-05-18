import datetime
from functools import wraps
from app import app
from flask import request, jsonify, render_template, make_response, redirect
from .empresa import empresa_by_cnpj
import jwt
from werkzeug.security import check_password_hash


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return redirect("/login")
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = empresa_by_cnpj(cnpj=data['username'])
        except:
            return redirect("/login")
        return f(current_user, *args, **kwargs)

    return decorated


def auth(form):
    user = empresa_by_cnpj(form.cnpj.data)
    if not user:
        return render_template('login_empresa.html', form=form, error="user not found")

    if user and check_password_hash(user.password, form.senha.data):
        token = jwt.encode({'username': user.username, 'exp': datetime.datetime.now() + datetime.timedelta(hours=12)},
                           app.config['SECRET_KEY'])
        resp = make_response(render_template('home_page.html'))
        resp.set_cookie('token', token)
        return resp

    return render_template('login_empresa.html', form=form, error="'could not verify")
