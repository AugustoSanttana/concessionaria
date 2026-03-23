from werkzeug.security import generate_password_hash, check_password_hash
from src.domain.user import UserDomain
from src.infrastructure.model_usuario import Usuario
from src.config.data_base import db

class UserService:
    @staticmethod
    def create_user(nome, email, senha, cpf, endereco):
        senha_hash = generate_password_hash(senha)
        new_user = UserDomain(nome, email, senha_hash, cpf, endereco)
        user = Usuario(
            nome=new_user.nome,
            email=new_user.email,
            senha=new_user.senha,
            cpf=new_user.cpf,
            endereco=new_user.endereco
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user(idUser):
        return Usuario.query.get(idUser)

    @staticmethod
    def login(email, senha):
        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            return None
        if not check_password_hash(usuario.senha, senha):
            return None
        return usuario
