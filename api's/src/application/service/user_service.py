from werkzeug.security import generate_password_hash, check_password_hash
from src.domain.user import ClienteDomain
from src.infrastructure.model_usuario import Usuario
from src.config.data_base import db

class UserService:
    @staticmethod
    def create_user(nome, email, senha, cpf, telefone, endereco, cep, data_nascimento,
                    renda_mensal=None, cnh=None, categoria_cnh=None, profissao=None):
        senha_hash = generate_password_hash(senha)
        new_user = ClienteDomain(
            nome=nome, email=email, senha=senha_hash, cpf=cpf,
            telefone=telefone, endereco=endereco, cep=cep,
            data_nascimento=data_nascimento, renda_mensal=renda_mensal,
            cnh=cnh, categoria_cnh=categoria_cnh, profissao=profissao
        )
        user = Usuario(
            nome=new_user.nome,
            email=new_user.email,
            senha=new_user.senha,
            cpf=new_user.cpf,
            telefone=new_user.telefone,
            endereco=new_user.endereco,
            cep=new_user.cep,
            data_nascimento=new_user.data_nascimento,
            renda_mensal=new_user.renda_mensal,
            cnh=new_user.cnh,
            categoria_cnh=new_user.categoria_cnh,
            profissao=new_user.profissao
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
