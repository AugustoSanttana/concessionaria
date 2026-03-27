from src.config.data_base import db


class Vendedor(db.Model):
    __tablename__ = "vendedores"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(600), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    cep = db.Column(db.String(10), nullable=False)
    data_nascimento = db.Column(db.String(10), nullable=False)
    codigo_vendedor = db.Column(db.String(50), unique=True, nullable=False)
    comissao_percentual = db.Column(db.Float, nullable=False)
    meta_mensal = db.Column(db.Float, nullable=True)
    gerente_id = db.Column(db.Integer, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "cpf": self.cpf,
            "telefone": self.telefone,
            "endereco": self.endereco,
            "cep": self.cep,
            "data_nascimento": self.data_nascimento,
            "codigo_vendedor": self.codigo_vendedor,
            "comissao_percentual": self.comissao_percentual,
            "meta_mensal": self.meta_mensal,
            "gerente_id": self.gerente_id
        }