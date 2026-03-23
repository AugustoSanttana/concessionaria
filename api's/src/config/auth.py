import jwt
import datetime
from flask import request, jsonify
from src.infrastructure.model_cabeleireiro import Cabeleireiro

SECRET_KEY = "sua_chave_super_secreta"  

def gerar_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=365)  
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verificar_token(func):
    def wrapper(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]  

        if not token:
            return jsonify({"erro": "Token não fornecido"}), 401

        try:
            dados = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = dados["user_id"]
            request.user_id = user_id

            cabeleireiro = Cabeleireiro.query.get(user_id)
            if cabeleireiro:
                request.is_admin = cabeleireiro.is_admin
        except jwt.ExpiredSignatureError:
            return jsonify({"erro": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"erro": "Token inválido"}), 401

        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
