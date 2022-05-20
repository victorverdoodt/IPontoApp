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
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = empresa_by_cnpj(cnpj=data['username'])
            if not current_user:
                return redirect("/login")
        except:
            return redirect("/login")
        return f(current_user, *args, **kwargs)

    return decorated


def token_validate(request):
    token = request.cookies.get('token')

    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        current_user = empresa_by_cnpj(cnpj=data['username'])
        if current_user:
            return True
    except:
        return None

    return None


def auth(form):
    user = empresa_by_cnpj(form.cnpj.data)
    if not user:
        return render_template('login_empresa.html', form=form, error="user not found")

    if user and check_password_hash(user.senha, form.senha.data):
        token = jwt.encode({'username': user.cnpj, 'exp': datetime.datetime.now() + datetime.timedelta(hours=12)},
                           app.config['SECRET_KEY'])
        resp = make_response(redirect('/empresa'))
        resp.set_cookie('token', token)
        return resp

    return render_template('login_empresa.html', form=form, error="'could not verify")
