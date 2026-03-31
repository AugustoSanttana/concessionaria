import jwt
from datetime import datetime, timedelta, timezone
from flask import request, jsonify, g
from functools import wraps
from src.infrastructure.model_vendedor import Vendedor

SECRET_KEY = "sua_chave_super_secreta"  

def gerar_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=365)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verificar_token(func):
    @wraps(func)
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
            g.user_id = user_id

            # Usando Session.get() para compatibilidade com SQLAlchemy 2.0
            from src.config.data_base import db
            vendedor = db.session.get(Vendedor, user_id)
            
            if vendedor:
                request.is_admin = vendedor.is_admin
                g.is_admin = vendedor.is_admin
        except jwt.ExpiredSignatureError:
            return jsonify({"erro": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"erro": "Token inválido"}), 401

        return func(*args, **kwargs)
    return wrapper
