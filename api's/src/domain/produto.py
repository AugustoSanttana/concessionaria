class ProdutoDomain:
    def __init__(self, nome, preco, quantidade, imagem_url=None):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.imagem_url = imagem_url

    def to_dict(self):
        return{
            "nome": self.nome,
            "preco": self.preco,
            "quantidade": self.quantidade,
            "imagem_url": self.imagem_url
        }