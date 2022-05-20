import datetime
from app import db, ma


class Empresa(db.Model):
    id_empresa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(200), unique=False, nullable=False)
    cnpj = db.Column(db.String(15), unique=True, nullable=False)
    senha = db.Column(db.String(20), unique=False, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.datetime.now())
    cargos = db.relationship('Cargo', backref='empresa', lazy=True)
    funcionarios = db.relationship('Funcionario', backref='empresa', lazy=True)
    funcionario_pontos = db.relationship('Funcionario_ponto', backref='empresa', lazy=True)

    def __init__(self, email, senha, cnpj, nome):
        self.cnpj = cnpj
        self.senha = senha
        self.nome = nome
        self.email = email


class EmpresaSchema(ma.Schema):
    class Meta:
        fields = ('id_empresa', 'nome', 'email', 'cnpj', 'senha', 'id_status', 'data_criacao')


empresa_schema = EmpresaSchema()
empresas_schema = EmpresaSchema(many=True)
