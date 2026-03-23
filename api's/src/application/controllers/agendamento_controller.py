from flask import jsonify, request
from src.infrastructure.model_agendamento import Agendamento
from src.infrastructure.model_cabeleireiro import Cabeleireiro
from src.config.data_base import db
from datetime import datetime, date
from src.config.auth import verificar_token  

class AgendamentoController:

    @staticmethod
    @verificar_token
    def criar_agendamento():
        data = request.get_json()
        cliente_id = request.user_id
        cabeleireiro_id = data.get("profissional_id")  # ID do cabeleireiro
        servico = data.get("servico")
        data_agenda = data.get("data")
        hora_agenda = data.get("hora")

        if not cabeleireiro_id or not servico or not data_agenda or not hora_agenda:
            return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

        # Verificar se o cabeleireiro existe
        cabeleireiro = Cabeleireiro.query.get(cabeleireiro_id)
        if not cabeleireiro:
            return jsonify({"erro": "Cabeleireiro não encontrado"}), 404

        # Verificar se o horário já está ocupado para esse cabeleireiro
        conflito = Agendamento.query.filter_by(
            cabeleireiro_id=cabeleireiro_id,
            data=datetime.strptime(data_agenda, "%Y-%m-%d").date(),
            hora=datetime.strptime(hora_agenda, "%H:%M").time()
        ).first()

        if conflito:
            return jsonify({"erro": "Esse horário já está ocupado!"}), 400

        agendamento = Agendamento(
            cliente_id=cliente_id,
            cabeleireiro_id=cabeleireiro_id,
            servico=servico,
            data=datetime.strptime(data_agenda, "%Y-%m-%d").date(),
            hora=datetime.strptime(hora_agenda, "%H:%M").time(),
            status="pendente"
        )

        db.session.add(agendamento)
        db.session.commit()

        return jsonify({"mensagem": "Agendamento criado com sucesso!"}), 201


    @staticmethod
    @verificar_token
    def listar_agendamentos():
        user_id = request.user_id
        is_admin = getattr(request, "is_admin", False)

        if is_admin:
            agendamentos = Agendamento.query.all()
        else:
            # Usuários comuns veem apenas seus agendamentos
            agendamentos = Agendamento.query.filter_by(cliente_id=user_id).all()

        # Cancelar agendamentos pendentes passados
        for ag in agendamentos:
            if ag.data < date.today() and ag.status == "pendente":
                ag.status = "cancelado"

        db.session.commit()

        resultado = []
        for a in agendamentos:
            resultado.append({
                "id": a.id,
                "cliente_id": a.cliente_id,
                "cliente_nome": a.cliente.nome if a.cliente else None,
                "profissional_id": a.cabeleireiro_id,
                "profissional_nome": a.cabeleireiro_agendamento.nome if hasattr(a, "cabeleireiro_agendamento") and a.cabeleireiro_agendamento else None,
                "servico": a.servico,
                "data": a.data.strftime("%Y-%m-%d"),
                "hora": a.hora.strftime("%H:%M"),
                "status": a.status
            })

        return jsonify(resultado), 200


    @staticmethod
    @verificar_token
    def cancelar_agendamento(agendamento_id):
        agendamento = Agendamento.query.filter_by(
            id=agendamento_id, cliente_id=request.user_id
        ).first()

        if not agendamento:
            return jsonify({"erro": "Agendamento não encontrado"}), 404

        if agendamento.status != "pendente":
            return jsonify({"erro": "Não é possível cancelar este agendamento"}), 400

        agendamento.status = "cancelado"
        db.session.commit()

        return jsonify({"mensagem": "Agendamento cancelado com sucesso!"}), 200


    @staticmethod
    @verificar_token
    def concluir_agendamento(id):
        if not getattr(request, "is_admin", False):
            return jsonify({"erro": "Acesso negado. Apenas administradores podem concluir agendamentos."}), 403

        agendamento = Agendamento.query.get(id)
        if not agendamento:
            return jsonify({"erro": "Agendamento não encontrado"}), 404

        if agendamento.status != "pendente":
            return jsonify({"erro": "Agendamento já foi concluído ou cancelado"}), 400

        agendamento.status = "concluido"
        db.session.commit()
        return jsonify({"mensagem": "Agendamento concluído com sucesso!"}), 200
