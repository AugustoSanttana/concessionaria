from src.config.data_base import db

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(600), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    cep = db.Column(db.String(10), nullable=False)
    data_nascimento = db.Column(db.String(10), nullable=False)
    renda_mensal = db.Column(db.Float, nullable=True)
    cnh = db.Column(db.String(20), unique=True, nullable=True)
    categoria_cnh = db.Column(db.String(5), nullable=True)
    profissao = db.Column(db.String(100), nullable=True)

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
            "renda_mensal": self.renda_mensal,
            "cnh": self.cnh,
            "categoria_cnh": self.categoria_cnh,
            "profissao": self.profissao
        }