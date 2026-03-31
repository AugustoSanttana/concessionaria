from src.domain.veiculo import VeiculoCompraDomain, VeiculoAluguelDomain
from src.infrastructure.model_veiculo import VeiculoCompra
from src.infrastructure.model_sevico import VeiculoAluguel
from src.config.data_base import db

class VeiculoService:

    # ==================== COMPRA ====================

    @staticmethod
    def create_veiculo_compra(modelo, marca, ano, preco, quilometragem, cor, combustivel, categoria, parcelas=None, descricao=None, imagem_url=None):
        domain = VeiculoCompraDomain(
            modelo=modelo, marca=marca, ano=ano, preco=preco,
            quilometragem=quilometragem, cor=cor, combustivel=combustivel,
            categoria=categoria, parcelas=parcelas, descricao=descricao, imagem_url=imagem_url
        )
        veiculo = VeiculoCompra(
            modelo=domain.modelo, marca=domain.marca, ano=domain.ano,
            preco=domain.preco, quilometragem=domain.quilometragem,
            cor=domain.cor, combustivel=domain.combustivel,
            categoria=domain.categoria, parcelas=domain.parcelas,
            descricao=domain.descricao, imagem_url=domain.imagem_url
        )
        db.session.add(veiculo)
        db.session.commit()
        db.session.refresh(veiculo)
        return veiculo

    @staticmethod
    def get_all_veiculos_compra():
        return VeiculoCompra.query.all()

    @staticmethod
    def get_veiculo_compra_by_id(veiculo_id):
        return VeiculoCompra.query.get(veiculo_id)

    @staticmethod
    def update_veiculo_compra(veiculo_id, **kwargs):
        veiculo = VeiculoCompra.query.get(veiculo_id)
        if not veiculo:
            return None
        for key, value in kwargs.items():
            if value is not None and hasattr(veiculo, key):
                setattr(veiculo, key, value)
        db.session.commit()
        return veiculo

    @staticmethod
    def delete_veiculo_compra(veiculo_id):
        veiculo = VeiculoCompra.query.get(veiculo_id)
        if not veiculo:
            return False
        db.session.delete(veiculo)
        db.session.commit()
        return True

    # ==================== ALUGUEL ====================

    @staticmethod
    def create_veiculo_aluguel(modelo, marca, ano, preco_diaria, quilometragem, cor, combustivel, categoria, tempo_minimo, descricao=None, imagem_url=None):
        domain = VeiculoAluguelDomain(
            modelo=modelo, marca=marca, ano=ano, preco_diaria=preco_diaria,
            quilometragem=quilometragem, cor=cor, combustivel=combustivel,
            categoria=categoria, tempo_minimo=tempo_minimo, descricao=descricao, imagem_url=imagem_url
        )
        veiculo = VeiculoAluguel(
            modelo=domain.modelo, marca=domain.marca, ano=domain.ano,
            preco_diaria=domain.preco_diaria, quilometragem=domain.quilometragem,
            cor=domain.cor, combustivel=domain.combustivel,
            categoria=domain.categoria, tempo_minimo=domain.tempo_minimo,
            descricao=domain.descricao, imagem_url=domain.imagem_url
        )
        db.session.add(veiculo)
        db.session.commit()
        db.session.refresh(veiculo)
        return veiculo

    @staticmethod
    def get_all_veiculos_aluguel():
        return VeiculoAluguel.query.all()

    @staticmethod
    def get_veiculo_aluguel_by_id(veiculo_id):
        return VeiculoAluguel.query.get(veiculo_id)

    @staticmethod
    def update_veiculo_aluguel(veiculo_id, **kwargs):
        veiculo = VeiculoAluguel.query.get(veiculo_id)
        if not veiculo:
            return None
        for key, value in kwargs.items():
            if value is not None and hasattr(veiculo, key):
                setattr(veiculo, key, value)
        db.session.commit()
        return veiculo

    @staticmethod
    def delete_veiculo_aluguel(veiculo_id):
        veiculo = VeiculoAluguel.query.get(veiculo_id)
        if not veiculo:
            return False
        db.session.delete(veiculo)
        db.session.commit()
        return True
