from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    IntegerField,
    PasswordField,
    DateField,
    DateTimeField,
    TimeField,
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
    hora_entrada = TimeField(
        'Hora Entrada',
        [
            DataRequired()
        ]
    )
    hora_almoco = TimeField(
        'Hora Almoço',
        [
            DataRequired()
        ]
    )
    hora_saida = TimeField(
        'Hora Saida',
        [
            DataRequired()
        ]
    )

    submit = SubmitField('Registrar')
