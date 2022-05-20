from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    IntegerField,
    PasswordField,
    DateField,
    SelectField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    URL
)

from ..models.cargo import Cargo, cargo_schema, cargos_schema


# nome, cpf, senha, id_cargo, id_empresa
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

    idCargo = SelectField(
        'Cargo',
        [
            DataRequired()
        ],
        choices=[],
        coerce=int
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
