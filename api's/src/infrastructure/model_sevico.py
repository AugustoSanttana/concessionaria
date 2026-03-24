from src.config.data_base import db

class Servico(db.Model):
    __tablename__ = "servicos"

    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Integer, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    imagem_url = db.Column(db.String(255), nullable=True)  
    tempo = db.Column(db.String(50), nullable=False)
    quilometragem = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "modelo": self.modelo,
            "preco": self.preco,
            "quantidade": self.quantidade,
            "imagem_url": self.imagem_url,
            "tempo": self.tempo,
            "quilometragem": self.quilometragem
        }
