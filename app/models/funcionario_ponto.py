import datetime

from app import db, ma


class Funcionario_ponto(db.Model):
    id_funcionario_ponto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_funcionario = db.Column(db.Integer, db.ForeignKey('funcionario.id_funcionario'), nullable=False)
    id_empresa = db.Column(db.Integer, db.ForeignKey('empresa.id_empresa'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.datetime.now())
    funcionarios = db.relationship('Funcionario', back_populates='funcionario_ponto', lazy=True)
    empresas = db.relationship('Empresa', back_populates='funcionario_pontos', lazy=True)

    def __init__(self, id_funcionario, id_empresa):
        self.id_funcionario = id_funcionario
        self.id_empresa = id_empresa


class Funcionario_pontoSchema(ma.Schema):
    class Meta:
        fields = ('id_funcionario_ponto', 'id_funcionario', 'id_empresa', 'data_criacao')


funcionario_ponto_schema = Funcionario_pontoSchema()
funcionario_pontos_schema = Funcionario_pontoSchema(many=True)
