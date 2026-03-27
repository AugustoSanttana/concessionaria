from flask import request, jsonify, make_response, send_from_directory
from werkzeug.utils import secure_filename
import os
from src.config.data_base import db
from src.application.service.veiculo_service import VeiculoService

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class VeiculoController:

    # ==================== COMPRA ====================

    @staticmethod
    def cadastrar_veiculo_compra():
        try:
            data = request.form
            imagem = request.files.get("imagem")

            modelo = data.get("modelo")
            marca = data.get("marca")
            ano = data.get("ano")
            preco = data.get("preco")
            quilometragem = data.get("quilometragem")
            cor = data.get("cor")
            combustivel = data.get("combustivel")
            categoria = data.get("categoria")
            parcelas = data.get("parcelas")
            descricao = data.get("descricao")

            if not all([modelo, marca, ano, preco, quilometragem, cor, combustivel, categoria, parcelas]):
                return make_response(jsonify({"erro": "Campos obrigatórios ausentes"}), 400)

            imagem_url = None
            if imagem:
                filename = secure_filename(imagem.filename)
                save_path = os.path.join(UPLOAD_FOLDER, filename)
                imagem.save(save_path)
                imagem_url = f"/uploads/{filename}"

            veiculo = VeiculoService.create_veiculo_compra(
                modelo=modelo, marca=marca, ano=int(ano),
                preco=float(preco), quilometragem=quilometragem,
                cor=cor, combustivel=combustivel, categoria=categoria,
                parcelas=int(parcelas), descricao=descricao, imagem_url=imagem_url
            )

            return make_response(jsonify({
                "mensagem": "Veículo cadastrado com sucesso",
                "veiculo": veiculo.to_dict()
            }), 201)

        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def listar_veiculos_compra():
        try:
            veiculos = VeiculoService.get_all_veiculos_compra()
            return make_response(jsonify([v.to_dict() for v in veiculos]), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def get_veiculo_compra(veiculo_id):
        try:
            veiculo = VeiculoService.get_veiculo_compra_by_id(veiculo_id)
            if not veiculo:
                return make_response(jsonify({"erro": "Veículo não encontrado"}), 404)
            return make_response(jsonify(veiculo.to_dict()), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def atualizar_veiculo_compra(veiculo_id):
        try:
            data = request.form
            imagem = request.files.get("imagem")

            update_data = {
                "modelo": data.get("modelo"),
                "marca": data.get("marca"),
                "ano": int(data.get("ano")) if data.get("ano") else None,
                "preco": float(data.get("preco")) if data.get("preco") else None,
                "quilometragem": data.get("quilometragem"),
                "cor": data.get("cor"),
                "combustivel": data.get("combustivel"),
                "categoria": data.get("categoria"),
                "parcelas": int(data.get("parcelas")) if data.get("parcelas") else None,
                "descricao": data.get("descricao"),
            }

            if imagem:
                filename = secure_filename(imagem.filename)
                save_path = os.path.join(UPLOAD_FOLDER, filename)
                imagem.save(save_path)
                update_data["imagem_url"] = f"/uploads/{filename}"

            veiculo = VeiculoService.update_veiculo_compra(veiculo_id, **update_data)
            if not veiculo:
                return make_response(jsonify({"erro": "Veículo não encontrado"}), 404)
            return make_response(jsonify(veiculo.to_dict()), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def deletar_veiculo_compra(veiculo_id):
        try:
            if not VeiculoService.delete_veiculo_compra(veiculo_id):
                return make_response(jsonify({"erro": "Veículo não encontrado"}), 404)
            return make_response(jsonify({"mensagem": "Veículo deletado com sucesso"}), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    # ==================== ALUGUEL ====================

    @staticmethod
    def cadastrar_veiculo_aluguel():
        try:
            data = request.form
            imagem = request.files.get("imagem")

            modelo = data.get("modelo")
            marca = data.get("marca")
            ano = data.get("ano")
            preco_diaria = data.get("preco_diaria")
            quilometragem = data.get("quilometragem")
            cor = data.get("cor")
            combustivel = data.get("combustivel")
            categoria = data.get("categoria")
            tempo_minimo = data.get("tempo_minimo")
            descricao = data.get("descricao")

            if not all([modelo, marca, ano, preco_diaria, quilometragem, cor, combustivel, categoria, tempo_minimo]):
                return make_response(jsonify({"erro": "Campos obrigatórios ausentes"}), 400)

            imagem_url = None
            if imagem:
                filename = secure_filename(imagem.filename)
                save_path = os.path.join(UPLOAD_FOLDER, filename)
                imagem.save(save_path)
                imagem_url = f"/uploads/{filename}"

            veiculo = VeiculoService.create_veiculo_aluguel(
                modelo=modelo, marca=marca, ano=int(ano),
                preco_diaria=float(preco_diaria), quilometragem=quilometragem,
                cor=cor, combustivel=combustivel, categoria=categoria,
                tempo_minimo=int(tempo_minimo), descricao=descricao, imagem_url=imagem_url
            )

            return make_response(jsonify({
                "mensagem": "Veículo de aluguel cadastrado com sucesso",
                "veiculo": veiculo.to_dict()
            }), 201)

        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def listar_veiculos_aluguel():
        try:
            veiculos = VeiculoService.get_all_veiculos_aluguel()
            return make_response(jsonify([v.to_dict() for v in veiculos]), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def get_veiculo_aluguel(veiculo_id):
        try:
            veiculo = VeiculoService.get_veiculo_aluguel_by_id(veiculo_id)
            if not veiculo:
                return make_response(jsonify({"erro": "Veículo não encontrado"}), 404)
            return make_response(jsonify(veiculo.to_dict()), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def atualizar_veiculo_aluguel(veiculo_id):
        try:
            data = request.form
            imagem = request.files.get("imagem")

            update_data = {
                "modelo": data.get("modelo"),
                "marca": data.get("marca"),
                "ano": int(data.get("ano")) if data.get("ano") else None,
                "preco_diaria": float(data.get("preco_diaria")) if data.get("preco_diaria") else None,
                "quilometragem": data.get("quilometragem"),
                "cor": data.get("cor"),
                "combustivel": data.get("combustivel"),
                "categoria": data.get("categoria"),
                "tempo_minimo": int(data.get("tempo_minimo")) if data.get("tempo_minimo") else None,
                "descricao": data.get("descricao"),
            }

            if imagem:
                filename = secure_filename(imagem.filename)
                save_path = os.path.join(UPLOAD_FOLDER, filename)
                imagem.save(save_path)
                update_data["imagem_url"] = f"/uploads/{filename}"

            veiculo = VeiculoService.update_veiculo_aluguel(veiculo_id, **update_data)
            if not veiculo:
                return make_response(jsonify({"erro": "Veículo não encontrado"}), 404)
            return make_response(jsonify(veiculo.to_dict()), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def deletar_veiculo_aluguel(veiculo_id):
        try:
            if not VeiculoService.delete_veiculo_aluguel(veiculo_id):
                return make_response(jsonify({"erro": "Veículo não encontrado"}), 404)
            return make_response(jsonify({"mensagem": "Veículo deletado com sucesso"}), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)