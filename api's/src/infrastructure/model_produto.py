from src.config.data_base import db

class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    imagem_url = db.Column(db.String(255), nullable=True)
    parcelas = db.Column(db.Integer, nullable=False)
    
        

    def to_dict(self):
        return {
            "id": self.id,
            "modelo": self.modelo,
            "preco": self.preco,
            "quantidade": self.quantidade,
            "imagem_url": self.imagem_url,
            "parcelas": self.parcelas
        }