from flask import request, jsonify, make_response
from src.application.service.user_service import UserService
from src.infrastructure.model_usuario import Usuario
from src.config.data_base import db
from werkzeug.security import check_password_hash
from src.config.auth import gerar_token
from src.config.auth import verificar_token


class UserController:
    @staticmethod
    def register_user():
        data = request.get_json()
        nome = data.get('nome')
        email = data.get('email')
        senha = data.get('senha')
        cpf = data.get('cpf')
        telefone = data.get('telefone')
        endereco = data.get('endereco')
        cep = data.get('cep')
        data_nascimento = data.get('data_nascimento')
        renda_mensal = data.get('renda_mensal')
        cnh = data.get('cnh')
        categoria_cnh = data.get('categoria_cnh')
        profissao = data.get('profissao')

        if not nome or not email or not senha or not cpf or not telefone or not endereco or not cep or not data_nascimento:
            return make_response(jsonify({"erro": "Campos obrigatórios ausentes"}), 400)
        
        user = UserService.create_user(
            nome=nome, email=email, senha=senha, cpf=cpf,
            telefone=telefone, endereco=endereco, cep=cep,
            data_nascimento=data_nascimento, renda_mensal=renda_mensal,
            cnh=cnh, categoria_cnh=categoria_cnh, profissao=profissao
        )
        return make_response(jsonify({
            "mensagem": "Cliente cadastrado com sucesso",
            "cliente": user.to_dict()
        }), 201)
    
    @staticmethod
    def get_user(idUser):
        user = UserService.get_user(idUser)
        if not user:
            return make_response(jsonify({"erro": "Cliente não encontrado"}), 404)
        return make_response(jsonify({
            "cliente": user.to_dict()
        }), 200)
    
    @staticmethod
    def login():
        data = request.get_json()
        email = data.get("email")
        senha = data.get("senha")

        usuario = UserService.login(email, senha)
        if not usuario:
            return jsonify({"erro": "Credenciais inválidas"}), 401

        token = gerar_token(usuario.id)
        return jsonify({
            "token": token,
            "id": usuario.id,
            "nome": usuario.nome
        })
    
    @staticmethod
    @verificar_token
    def perfil_usuario():
        usuario = Usuario.query.get(request.user_id)

        if not usuario:
            return jsonify({"erro": "Cliente não encontrado"}), 404

        return jsonify(usuario.to_dict()), 200