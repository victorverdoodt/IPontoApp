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


class CargoCadastro(FlaskForm):
    titulo = StringField(
        'Titulo',
        [
            DataRequired()
        ]
    )
    descricao = StringField(
        'Descricao',
        [
            DataRequired()
        ]
    )
    hora_entrada = DateField(
        'Hora Entrada',
        [
            DataRequired()
        ]
    )
    hora_almoco = DateField(
        'Hora almoco',
        [
            DataRequired()
        ]
    )
    hora_saida = DateField(
        'Hora saida',
        [
            DataRequired()
        ]
    )

    submit = SubmitField('Registrar')
