from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    PasswordField,
    DateField,
    SelectField
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    URL
)


class EmpresaCadastro(FlaskForm):
    nome = StringField(
        'Nome',
        [
            DataRequired()
        ]
    )
    cnpj = StringField(
        'CNPJ',
        [
            DataRequired()
        ]
    )
    email = StringField(
        'Email',
        [
            Email(message='Not a valid email address.'),
            DataRequired()
        ]
    )
    senha = PasswordField(
        'Senha',
        [
            DataRequired(message="Please enter a senha."),
        ]
    )
    confirmSenha = PasswordField(
        'Repetir a Senha',
        [
            EqualTo('senha', message='Passwords must match.')
        ]
    )

    submit = SubmitField('Registrar')
