from werkzeug.security import generate_password_hash
from src.config.data_base import db, init_db
from infrastructure.model_cabeleireiro import Cabeleireiro
from flask import Flask

# Cria o app Flask e inicializa o DB
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mpfg2005@localhost/barbearia_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)

with app.app_context():
    # Checa se já existe um admin
    admin_existente = Cabeleireiro.query.filter_by(is_admin=True).first()
    
    if admin_existente:
        print(f"Admin já existe: {admin_existente.email}")
    else:
        # Cria um hash para a senha do admin
        senha_admin = "senha_super_secreta"  # Coloque a senha que quiser
        senha_hash = generate_password_hash(senha_admin)

        admin = Cabeleireiro(
            nome="Admin",
            email="admin@salon.com",
            senha=senha_hash,
            is_admin=True
        )

        db.session.add(admin)
        db.session.commit()
        print("Admin criado com sucesso!")
        print(f"Email: {admin.email}")
        print(f"Senha: {senha_admin}")
