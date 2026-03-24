class ProdutoCompraDomain:
    def __init__(self, modelo, preco, quantidade, parcelas, imagem_url=None):
        self.modelo = modelo
        self.preco = preco
        self.quantidade = quantidade
        self.parcelas = parcelas    
        self.imagem_url = imagem_url

    def to_dict(self):
        return{
            "modelo": self.modelo,
            "preco": self.preco,
            "quantidade": self.quantidade,
            "imagem_url": self.imagem_url,
            "parcelas": self.parcelas
        }
    

class ProdutoAluguelDomain:
    def __init__(self, modelo, preco, quantidade, parcelas, tempo, imagem_url=None, quilometragem=None):
        self.modelo = modelo
        self.preco = preco
        self.quantidade = quantidade
        self.parcelas = parcelas    
        self.tempo = tempo  
        self.quilometragem = quilometragem
        self.imagem_url = imagem_url

    def to_dict(self):
        return{
            "modelo": self.modelo,
            "preco": self.preco,
            "quantidade": self.quantidade,
            "imagem_url": self.imagem_url,
            "parcelas": self.parcelas,
            "tempo": self.tempo,
            "quilometragem": self.quilometragem
        }