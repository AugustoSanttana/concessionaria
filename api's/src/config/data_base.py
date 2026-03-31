import os
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

def init_db(app):
    database_url = os.getenv('DATABASE_URL', "mysql+pymysql://root:oKSoXaZsQrsDPIrqsLioSBoBSckSYtVB@caboose.proxy.rlwy.net:41758/railway")
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)