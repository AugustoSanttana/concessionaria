from src.application.controllers.user_controller import UserController
from src.application.controllers.veiculo_controller import VeiculoController
from src.application.controllers.vendedor_controller import VendedorController
from flask import jsonify, make_response, send_from_directory
from flask import Blueprint
from flask import request


cliente_routes = Blueprint("cliente_routes", __name__)
vendedor_routes = Blueprint("vendedor_routes", __name__)
veiculos_routes = Blueprint("veiculos_routes", __name__)

#-------------------------------------#
# CLIENTE (usuário)
#-------------------------------------#

@cliente_routes.route("/<int:idUser>", methods=["GET"])
def get_cliente(idUser):
    return UserController.get_user(idUser)

@cliente_routes.route("/cadastrar", methods=["POST"])
def cadastrar_cliente():
    return UserController.register_user()

@cliente_routes.route("/login", methods=["POST"])
def login_cliente():
    return UserController.login()

@cliente_routes.route("/perfil", methods=["GET"])
def perfil_cliente():
    return UserController.perfil_usuario()

#-------------------------------------#
# VENDEDOR
#-------------------------------------#

@vendedor_routes.route("/cadastrar", methods=["POST"])
def cadastrar_vendedor():
    return VendedorController.cadastrar_vendedor()

@vendedor_routes.route("/login", methods=["POST"])
def login_vendedor():
    return VendedorController.login()

@vendedor_routes.route("/perfil", methods=["GET"])
def perfil_vendedor():
    return VendedorController.perfil_vendedor()

@vendedor_routes.route("/listar", methods=["GET"])
def listar_vendedores():
    return VendedorController.listar_vendedores()

#-------------------------------------#
# VEÍCULOS - COMPRA
#-------------------------------------#

@veiculos_routes.route("/compra/listar", methods=["GET"])
def listar_veiculos_compra():
    return VeiculoController.listar_veiculos_compra()

@veiculos_routes.route("/compra/cadastrar", methods=["POST"])
def cadastrar_veiculo_compra():
    return VeiculoController.cadastrar_veiculo_compra()

@veiculos_routes.route("/compra/<int:id>", methods=["GET"])
def get_veiculo_compra(id):
    return VeiculoController.get_veiculo_compra(id)

@veiculos_routes.route("/compra/<int:id>", methods=["PUT"])
def atualizar_veiculo_compra(id):
    return VeiculoController.atualizar_veiculo_compra(id)

@veiculos_routes.route("/compra/<int:id>", methods=["DELETE"])
def deletar_veiculo_compra(id):
    return VeiculoController.deletar_veiculo_compra(id)

#-------------------------------------#
# VEÍCULOS - ALUGUEL
#-------------------------------------#

@veiculos_routes.route("/aluguel/listar", methods=["GET"])
def listar_veiculos_aluguel():
    return VeiculoController.listar_veiculos_aluguel()

@veiculos_routes.route("/aluguel/cadastrar", methods=["POST"])
def cadastrar_veiculo_aluguel():
    return VeiculoController.cadastrar_veiculo_aluguel()

@veiculos_routes.route("/aluguel/<int:id>", methods=["GET"])
def get_veiculo_aluguel(id):
    return VeiculoController.get_veiculo_aluguel(id)

@veiculos_routes.route("/aluguel/<int:id>", methods=["PUT"])
def atualizar_veiculo_aluguel(id):
    return VeiculoController.atualizar_veiculo_aluguel(id)

@veiculos_routes.route("/aluguel/<int:id>", methods=["DELETE"])
def deletar_veiculo_aluguel(id):
    return VeiculoController.deletar_veiculo_aluguel(id)