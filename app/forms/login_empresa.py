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


class EmpresaLogin(FlaskForm):
    cnpj = StringField(
        'Cnpj',
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

    submit = SubmitField('Entrar')
