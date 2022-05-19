from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    IntegerField,
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

#nome, cpf, senha, id_cargo, id_empresa
class FuncionarioCadastro(FlaskForm):
    nome = StringField(
        'Nome',
        [
            DataRequired()
        ]
    )
    cpf = StringField(
        'CPF',
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
    idCargo = IntegerField(
        'Cargo',
        [
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
