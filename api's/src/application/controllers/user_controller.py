from flask import request, jsonify, make_response
from src.application.service.user_service import UserService
from flask import request, jsonify
from src.infrastructure.model_usuario import Usuario
from src.config.data_base import db
from werkzeug.security import check_password_hash
from src.config.auth import gerar_token
from src.config.auth import verificar_token
from src.infrastructure.model_agendamento import Agendamento




class UserController:
    @staticmethod
    def register_user():
        data = request.get_json()
        nome = data.get('nome')
        email = data.get('email')
        senha = data.get('senha')
        cpf = data.get('cpf')
        endereco = data.get('endereco')

        if not nome or not email or not senha or not cpf or not endereco:
            return make_response(jsonify({"erro": "Campos obrigatórios ausentes"}), 400)
        
        user = UserService.create_user(nome, email, senha, cpf, endereco)
        return make_response(jsonify({
            "mensagem": "User salvo com sucesso",
            "usuarios": user.to_dict()
        }), 200)
    
    @staticmethod
    def get_user(idUser):
        user = UserService.get_user(idUser)
        if not user:
            return make_response(jsonify({"erro": "Usuário não encontrado"}), 404)
        return make_response(jsonify({
            "usuario": user.to_dict()
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
            return jsonify({"erro": "Usuário não encontrado"}), 404

        agendamentos = Agendamento.query.filter_by(cliente_id=usuario.id).all()

        agendamentos_data = [
            {
                "id": ag.id,
                "profissional": ag.cabeleireiro_agendamento.nome if ag.cabeleireiro_agendamento else None,
                "servico": ag.servico,
                "data": ag.data.strftime("%d/%m/%Y"),
                "hora": ag.hora.strftime("%H:%M"),
                "status": ag.status
            }
            for ag in agendamentos
        ]

        usuario_data = {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "cpf": usuario.cpf,
            "endereco": usuario.endereco,
            "agendamentos": agendamentos_data
        }

        return jsonify(usuario_data), 200