import datetime

from app import db, ma


class Cargo(db.Model):
    id_cargo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(40), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    id_empresa = db.Column(db.Integer, db.ForeignKey('empresa.id_empresa'), nullable=False)
    hora_entrada = db.Column(db.Time)
    hora_almoco = db.Column(db.Time)
    hora_saida = db.Column(db.Time)
    data_criacao = db.Column(db.DateTime, default=datetime.datetime.now())
    empresas = db.relationship('Empresa', back_populates='cargos')

    def __init__(self, titulo, descricao, id_empresa, hora_entrada, hora_almoco, hora_saida):
        self.titulo = titulo
        self.descricao = descricao
        self.id_empresa = id_empresa
        self.hora_entrada = hora_entrada
        self.hora_almoco = hora_almoco
        self.hora_saida = hora_saida


class CargoSchema(ma.Schema):
    class Meta:
        fields = ('id_cargo', 'titulo', 'descricao', 'id_empresa', 'hora_entrada', 'hora_almoco', 'hora_saida', 'data_criacao')


cargo_schema = CargoSchema()
cargos_schema = CargoSchema(many=True)
