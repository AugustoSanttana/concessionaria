# reset_db.py
from app import create_app   # importa sua factory de app
from src.config.data_base import db
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    print("🔄 Resetando banco de dados...")
    db.drop_all()   # apaga todas as tabelas
    db.create_all() # recria com os modelos atuais

    # mostrar as tabelas existentes depois da recriação
    inspector = inspect(db.engine)
    print("✅ Tabelas atuais no banco:", inspector.get_table_names())

print("✨ Reset do banco finalizado.")
