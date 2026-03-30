from flask import request, jsonify
from src.config.data_base import db
from src.config.auth import verificar_token
from src.infrastructure.model_avaliacao import Avaliacao


class AvaliacaoController:

    @staticmethod
    @verificar_token
    def criar_avaliacao():
        user_id = request.user_id
        dados = request.get_json()
        
        nota = dados.get('nota')
        comentario = dados.get('comentario')

        if not nota:
            return jsonify({"erro": "Nota é obrigatória"}), 400

        if not 1 <= int(nota) <= 5:
            return jsonify({"erro": "A nota deve ser entre 1 e 5"}), 400

        nova_avaliacao = Avaliacao(
            nota=nota,
            comentario=comentario,
            usuario_id=user_id
        )

        db.session.add(nova_avaliacao)
        db.session.commit()

        return jsonify({"mensagem": "Avaliação enviada com sucesso!"}), 201

    @staticmethod
    def listar_avaliacoes():
        avaliacoes = Avaliacao.query.order_by(Avaliacao.data_criacao.desc()).all()

        lista = []
        for a in avaliacoes:
            lista.append({
                "usuario": a.usuario.nome,
                "nota": a.nota,
                "comentario": a.comentario
            })

        return jsonify(lista), 200