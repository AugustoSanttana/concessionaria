from flask import Flask, request, send_from_directory
from flask import Flask, request, send_from_directory, jsonify
from src.config.data_base import db, init_db
from src.routes import cliente_routes, vendedor_routes, veiculos_routes
from flask_cors import CORS
from flask_migrate import Migrate
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

    init_db(app)

    @app.before_request
    def handle_options():
        if request.method == "OPTIONS":
            return '', 200

    migrate = Migrate(app, db)

    app.register_blueprint(cliente_routes, url_prefix="/cliente")
    app.register_blueprint(vendedor_routes, url_prefix="/vendedor")
    app.register_blueprint(veiculos_routes, url_prefix="/veiculo")

    @app.route('/')
    def index():
        return jsonify({"status": "API Concessionária Online", "versao": "1.0.0"}), 200

    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory("uploads", filename)

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)