import os
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

def init_db(app):
    database_url = os.getenv('DATABASE_URL', "mysql+pymysql://root:fuYzRRvPELwXmqLEKbzZUoEBXyOtcVXE@tramway.proxy.rlwy.net:33501/railway")
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)