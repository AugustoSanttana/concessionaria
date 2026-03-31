from src.config.data_base import db

class VeiculoCompra(db.Model):
    __tablename__ = "veiculos_compra"

    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quilometragem = db.Column(db.String(50), nullable=False)
    cor = db.Column(db.String(50), nullable=False)
    combustivel = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    parcelas = db.Column(db.Integer, nullable=True)
    descricao = db.Column(db.Text, nullable=True)
    imagem_url = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "modelo": self.modelo,
            "marca": self.marca,
            "ano": self.ano,
            "preco": self.preco,
            "quilometragem": self.quilometragem,
            "cor": self.cor,
            "combustivel": self.combustivel,
            "categoria": self.categoria,
            "parcelas": self.parcelas,
            "descricao": self.descricao,
            "imagem_url": self.imagem_url
        }