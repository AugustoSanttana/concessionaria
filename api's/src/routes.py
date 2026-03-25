from src.application.controllers.user_controller import UserController
from src.application.controllers.agendamento_controller import AgendamentoController
from src.application.controllers.cabeleireiro_controller import CabeleireiroController
from src.application.controllers.veiculo_controller import VeiculoController
from src.application.controllers.avaliacao_controller import AvaliacaoController
from flask import jsonify, make_response, send_from_directory
from flask import Blueprint
from flask import request





user_routes = Blueprint("user_routes", __name__)
agendamento_routes = Blueprint("agendamento_routes", __name__)
cabeleireiro_routes = Blueprint("cabeleireiro_routes", __name__)
veiculos_routes = Blueprint("veiculos_routes", __name__)
avaliacao_routes = Blueprint("avaliacao_routes", __name__)

#-------------------------------------#


@user_routes.route("/<int:idUser>", methods=["GET"])
def get_user(idUser):
    return UserController.get_user(idUser)
    
@user_routes.route("/cadastrar", methods=["POST"])
def register_user():
    return UserController.register_user()

@user_routes.route("/login", methods=["POST"])
def login():
    return UserController.login()

@user_routes.route("/perfil", methods=["GET"])
def perfil_usuario():
    return UserController.perfil_usuario()

#-------------------------------------#


@agendamento_routes.route("/listar", methods=["GET"])
def listar_agendamentos():
    return AgendamentoController.listar_agendamentos()

@agendamento_routes.route("/criar", methods=["POST"])
def criar_agendamento():
    return AgendamentoController.criar_agendamento()

@agendamento_routes.route("/<int:id>/concluir", methods=["PUT"])
def concluir_agendamento(id):
    return AgendamentoController.concluir_agendamento(id)

@agendamento_routes.route("/cancelar/<int:agendamento_id>", methods=["PUT"])
def cancelar_agendamento(agendamento_id):
    return AgendamentoController.cancelar_agendamento(agendamento_id)

#-------------------------------------

@cabeleireiro_routes.route("/cadastrar", methods=["POST"])
def cadastrar_cabeleireiro():
    return CabeleireiroController.cadastrar_cabeleireiro()

@cabeleireiro_routes.route("/listar", methods=["GET"])
def listar_cabeleireiros():
    return CabeleireiroController.listar_cabeleireiros()

@cabeleireiro_routes.route("/servico/cadastrar", methods=["POST"])
def cadastrar_servico():
    return CabeleireiroController.cadastrar_servico()

@cabeleireiro_routes.route("/login", methods=["POST"])
def login_cabeleireiro():
    return CabeleireiroController.login()

@cabeleireiro_routes.route("/perfil", methods=["GET"])
def perfil_cabeleireiro():
    return CabeleireiroController.perfil_cabeleireiro()

@cabeleireiro_routes.route("/agendamentos/<int:agendamento_id>/concluir", methods=["PUT"])
def concluir_agendamento_cabeleireiro(agendamento_id):
    return CabeleireiroController.concluir_agendamento(agendamento_id)



#-------------------------------------


@veiculos_routes.route("/listar", methods=["GET"])
def listar_produtos():
    return VeiculoController.listar_veiculos()

@veiculos_routes.route("/cadastrar", methods=["POST"])
def cadastrar_produto():
    return VeiculoController.cadastrar_veiculo()

@veiculos_routes.route("/<int:id>", methods=["GET"])
def get_produto(id):
    return VeiculoController.get_veiculo(id)

@veiculos_routes.route("/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    return VeiculoController.atualizar_veiculo(id)

@veiculos_routes.route("/<int:id>", methods=["DELETE"])
def deletar_produto(id):
    return VeiculoController.deletar_veiculo(id)

#-------------------------------------

@avaliacao_routes.route("/", methods=["POST"])
def criar_avaliacao():
    return AvaliacaoController.criar_avaliacao()

@avaliacao_routes.route("/listar", methods=["GET"])
def listar_avaliacoes():
    return AvaliacaoController.listar_avaliacoes()