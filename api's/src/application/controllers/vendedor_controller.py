from flask import request, jsonify
from src.infrastructure.model_vendedor import Vendedor
from src.config.data_base import db
from src.config.auth import gerar_token, verificar_token
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError

class VendedorController:

    @staticmethod
    @verificar_token
    def cadastrar_vendedor():
        try:
            if not getattr(request, "is_admin", False):
                return jsonify({"erro": "Acesso negado. Apenas administradores podem cadastrar vendedores."}), 403

            data = request.get_json() or {}
            nome = data.get("nome")
            email = data.get("email")
            senha = data.get("senha")
            cpf = data.get("cpf")
            telefone = data.get("telefone")
            endereco = data.get("endereco")
            cep = data.get("cep")
            data_nascimento = data.get("data_nascimento")
            codigo_vendedor = data.get("codigo_vendedor")
            comissao_percentual = data.get("comissao_percentual")
            meta_mensal = data.get("meta_mensal")
            gerente_id = data.get("gerente_id")

            if not all([nome, email, senha, cpf, telefone, endereco, cep, data_nascimento, codigo_vendedor, comissao_percentual]):
                return jsonify({"erro": "Campos obrigatórios ausentes"}), 400

            if Vendedor.query.filter_by(email=email).first():
                return jsonify({"erro": "Email já cadastrado"}), 400

            if Vendedor.query.filter_by(cpf=cpf).first():
                return jsonify({"erro": "CPF já cadastrado"}), 400

            senha_hash = generate_password_hash(senha, method="pbkdf2:sha256:260000")
            vendedor = Vendedor(
                nome=nome, email=email, senha=senha_hash,
                cpf=cpf, telefone=telefone, endereco=endereco,
                cep=cep, data_nascimento=data_nascimento,
                codigo_vendedor=codigo_vendedor,
                comissao_percentual=float(comissao_percentual),
                meta_mensal=float(meta_mensal) if meta_mensal else None,
                gerente_id=int(gerente_id) if gerente_id else None,
                is_admin=False
            )

            db.session.add(vendedor)
            db.session.commit()

            return jsonify({
                "mensagem": "Vendedor cadastrado com sucesso!",
                "vendedor": vendedor.to_dict()
            }), 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"erro": "Erro ao salvar no banco", "detalhes": str(e)}), 500
        except Exception as e:
            return jsonify({"erro": "Erro interno", "detalhes": str(e)}), 500

    @staticmethod
    def login():
        try:
            data = request.get_json() or {}
            email = data.get("email")
            senha = data.get("senha")

            if not email or not senha:
                return jsonify({"erro": "Email e senha são obrigatórios"}), 400

            vendedor = Vendedor.query.filter_by(email=email).first()
            if not vendedor:
                return jsonify({"erro": "Credenciais inválidas"}), 401

            if not check_password_hash(vendedor.senha, senha):
                return jsonify({"erro": "Credenciais inválidas"}), 401

            token = gerar_token(vendedor.id)
            return jsonify({
                "token": token,
                "vendedor": {
                    "id": vendedor.id,
                    "nome": vendedor.nome,
                    "email": vendedor.email,
                    "is_admin": bool(vendedor.is_admin)
                }
            }), 200

        except Exception as e:
            return jsonify({"erro": "Erro interno", "detalhes": str(e)}), 500

    @staticmethod
    @verificar_token
    def listar_vendedores():
        try:
            vendedores = Vendedor.query.filter_by(is_admin=False).all()
            return jsonify([v.to_dict() for v in vendedores]), 200
        except Exception as e:
            return jsonify({"erro": "Erro ao listar vendedores", "detalhes": str(e)}), 500

    @staticmethod
    @verificar_token
    def perfil_vendedor():
        try:
            vendedor_id = getattr(request, "user_id", None)
            if not vendedor_id:
                return jsonify({"erro": "Token inválido ou ausente"}), 401

            vendedor = Vendedor.query.get(vendedor_id)
            if not vendedor:
                return jsonify({"erro": "Vendedor não encontrado"}), 404

            return jsonify(vendedor.to_dict()), 200

        except Exception as e:
            return jsonify({"erro": "Erro ao carregar perfil do vendedor", "detalhes": str(e)}), 500
