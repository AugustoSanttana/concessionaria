from src.domain.veiculo import VeiculoCompraDomain, VeiculoAluguelDomain
from src.infrastructure.model_veiculo import Veiculo
from src.config.data_base import db

class VeiculoService:    
    @staticmethod
    def create_produto(nome, preco, quantidade, imagem_url=None):
        produto_novo = ProdutoDomain(nome, preco, quantidade, imagem_url)
        produto = Produto(
            nome=produto_novo.nome,
            preco=produto_novo.preco,
            quantidade=produto_novo.quantidade,
            imagem_url=produto_novo.imagem_url
        )
        db.session.add(produto)
        db.session.commit()
        db.session.refresh(produto)

        return produto
   

    @staticmethod
    def get_all_produtos():
        return Produto.query.all()

    @staticmethod
    def get_produto_by_id(produto_id):
        return Produto.query.get(produto_id)

    @staticmethod
    def update_produto(produto_id, nome=None, preco=None, quantidade=None, imagem_url=None):
        produto = Produto.query.get(produto_id)
        if not produto:
            return None
        if nome:
            produto.nome = nome
        if preco:
            produto.preco = preco
        if quantidade:
            produto.quantidade = quantidade
        if imagem_url:
            produto.imagem_url = imagem_url
        db.session.commit()
        return produto

    @staticmethod
    def delete_produto(produto_id):
        produto = Produto.query.get(produto_id)
        if not produto:
            return False
        db.session.delete(produto)
        db.session.commit()
        return True
