class VeiculoCompraDomain:
    def __init__(self, modelo, marca, ano, preco, quilometragem, cor, combustivel, categoria, parcelas=None, descricao=None, imagem_url=None):
        self.modelo = modelo
        self.marca = marca
        self.ano = ano
        self.preco = preco
        self.quilometragem = quilometragem
        self.cor = cor
        self.combustivel = combustivel
        self.categoria = categoria
        self.parcelas = parcelas
        self.descricao = descricao
        self.imagem_url = imagem_url

    def to_dict(self):
        return{
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
    

class VeiculoAluguelDomain:
    def __init__(self, modelo, marca, ano, preco_diaria, quilometragem, cor, combustivel, categoria, tempo_minimo, descricao=None, imagem_url=None):
        self.modelo = modelo
        self.marca = marca
        self.ano = ano
        self.preco_diaria = preco_diaria
        self.quilometragem = quilometragem
        self.cor = cor
        self.combustivel = combustivel  # flex, gasolina, diesel, eletrico, hibrido
        self.categoria = categoria  # sedan, hatch, suv, pickup, etc
        self.tempo_minimo = tempo_minimo  # tempo minimo de aluguel em dias
        self.descricao = descricao
        self.imagem_url = imagem_url

    def to_dict(self):
        return{
            "modelo": self.modelo,
            "marca": self.marca,
            "ano": self.ano,
            "preco_diaria": self.preco_diaria,
            "quilometragem": self.quilometragem,
            "cor": self.cor,
            "combustivel": self.combustivel,
            "categoria": self.categoria,
            "tempo_minimo": self.tempo_minimo,
            "descricao": self.descricao,
            "imagem_url": self.imagem_url
        }