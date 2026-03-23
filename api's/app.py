from flask import Flask, request, send_from_directory
from src.config.data_base import db, init_db
from src.routes import user_routes, agendamento_routes, cabeleireiro_routes, produtos_routes, avaliacao_routes
from flask_cors import CORS
from flask_migrate import Migrate
import pymysql
import os

def create_app():
    app = Flask(__name__)
    CORS(app, resources={
        r"/*": {
            "origins": ["http://127.0.0.1:5500"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mpfg2005@localhost/barbearia_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db_name = 'barbearia_db'
    conn = pymysql.connect(host='localhost', user='root', password='mpfg2005')
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    conn.commit()
    cursor.close()
    conn.close()

    init_db(app)

    @app.before_request
    def handle_options():
        if request.method == "OPTIONS":
            return '', 200

    migrate = Migrate(app, db)

    app.register_blueprint(user_routes, url_prefix="/user_routes")
    app.register_blueprint(agendamento_routes, url_prefix="/agendamento")
    app.register_blueprint(cabeleireiro_routes, url_prefix="/cabeleireiro")
    app.register_blueprint(produtos_routes, url_prefix="/produto")
    app.register_blueprint(avaliacao_routes, url_prefix="/avaliacao")

    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory("uploads", filename)

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)