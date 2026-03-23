from src.config.data_base import db

class Servico(db.Model):
    __tablename__ = "servicos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Integer, nullable=False)
    cabeleireiro_id = db.Column(db.Integer, db.ForeignKey("cabeleireiros.id"), nullable=False)


    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "cabeleireiro_id": self.cabeleireiro_id
        }
