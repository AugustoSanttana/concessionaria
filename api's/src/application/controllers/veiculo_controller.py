from flask import request, jsonify, make_response, send_from_directory
from werkzeug.utils import secure_filename
import os
from src.config.data_base import db
from src.application.service.veiculo_service import VeiculoService

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class VeiculoController:
    @staticmethod
    def cadastrar_produto():
        try: 
            nome = request.form.get("nome")
            preco = request.form.get("preco")
            quantidade = request.form.get("quantidade")
            imagem = request.files.get("imagem")

            if not nome or not preco or not quantidade:
                return make_response(jsonify({"erro": "Campos obrigatórios ausentes"}), 400)

            imagem_url = None
            if imagem:
                filename = secure_filename(imagem.filename)
                save_path = os.path.join(UPLOAD_FOLDER, filename)
                imagem.save(save_path)
                imagem_url = f"/uploads/{filename}"

            produto = ProdutoService.create_produto(
                nome=nome,
                preco=float(preco),
                quantidade=int(quantidade),
                imagem_url=imagem_url
            )

            return make_response(jsonify({
                "mensagem": "Produto criado com sucesso",
                "produto": produto.to_dict()
            }), 201)

        except Exception as e:
            print("Erro ao cadastrar produto:", e)
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def listar_produtos():
        try:
            produtos = ProdutoService.get_all_produtos()
            return make_response(jsonify([p.to_dict() for p in produtos]), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def get_produto(produto_id):
        try:
            produto = ProdutoService.get_produto_by_id(produto_id)
            if not produto:
                return make_response(jsonify({"erro": "Produto não encontrado"}), 404)
            return make_response(jsonify(produto.to_dict()), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def atualizar_produto(produto_id):
        try:
            data = request.form
            imagem = request.files.get("imagem")

            update_data = {
                "nome": data.get("nome"),
                "preco": float(data.get("preco")) if data.get("preco") is not None else None,
                "quantidade": int(data.get("quantidade")) if data.get("quantidade") is not None else None,
            }

            if imagem:
                filename = secure_filename(imagem.filename)
                save_path = os.path.join(UPLOAD_FOLDER, filename)
                imagem.save(save_path)
                update_data["imagem_url"] = f"/uploads/{filename}"

            produto = ProdutoService.update_produto(produto_id, **update_data)
            if not produto:
                return make_response(jsonify({"erro": "Produto não encontrado"}), 404)
            return make_response(jsonify(produto.to_dict()), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def deletar_produto(produto_id):
        try:
            if not ProdutoService.delete_produto(produto_id):
                return make_response(jsonify({"erro": "Produto não encontrado"}), 404)
            return make_response(jsonify({"mensagem": "Produto deletado com sucesso"}), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)