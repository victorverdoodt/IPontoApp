import datetime

from app import db, ma


class Funcionario(db.Model):
    id_funcionario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(40), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    senha = db.Column(db.String(20), nullable=False)
    id_cargo = db.Column(db.Integer, db.ForeignKey('cargo.id_cargo'), nullable=False)
    id_empresa = db.Column(db.Integer, db.ForeignKey('empresa.id_empresa'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.datetime.now())
    empresas = db.relationship('Empresa', back_populates='funcionarios')
    cargo = db.relationship('Cargo', backref='funcionarios', lazy='dynamic')
    funcionario_ponto = db.relationship('Funcionario_ponto', backref='funcionario', lazy=True)

    def __init__(self, nome, cpf, senha, email, id_cargo, id_empresa):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.senha = senha
        self.id_cargo = id_cargo
        self.id_empresa = id_empresa


class FuncionarioSchema(ma.Schema):
    class Meta:
        fields = ('id_funcionario', 'nome', 'cpf', 'email','senha', 'id_cargo', 'id_empresa', 'data_criacao')


funcionario_schema = FuncionarioSchema()
funcionarios_schema = FuncionarioSchema(many=True)
