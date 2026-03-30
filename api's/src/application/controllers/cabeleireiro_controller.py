from flask import request, jsonify
from src.infrastructure.model_cabeleireiro import Cabeleireiro
from src.infrastructure.model_agendamento import Agendamento
from src.infrastructure.model_sevico import Servico
from src.config.data_base import db
from src.config.auth import gerar_token, verificar_token
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError

class CabeleireiroController:

    @staticmethod
    @verificar_token
    def cadastrar_cabeleireiro():
        try:
            if not getattr(request, "is_admin", False):
                return jsonify({"erro": "Acesso negado. Apenas administradores podem cadastrar cabeleireiros."}), 403

            data = request.get_json() or {}
            nome = data.get("nome")
            email = data.get("email")
            senha = data.get("senha")

            if not nome or not email or not senha:
                return jsonify({"erro": "Campos obrigatórios ausentes"}), 400

            if Cabeleireiro.query.filter_by(email=email).first():
                return jsonify({"erro": "Email já cadastrado"}), 400

            senha_hash = generate_password_hash(senha, method="pbkdf2:sha256:260000")
            cabeleireiro = Cabeleireiro(nome=nome, email=email, senha=senha_hash, is_admin=False)

            db.session.add(cabeleireiro)
            db.session.commit()

            return jsonify({
                "mensagem": "Cabeleireiro cadastrado com sucesso!",
                "cabeleireiro": {
                    "id": cabeleireiro.id,
                    "nome": cabeleireiro.nome,
                    "email": cabeleireiro.email
                }
            }), 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"erro": "Erro ao salvar no banco", "detalhes": str(e)}), 500
        except Exception as e:
            return jsonify({"erro": "Erro interno", "detalhes": str(e)}), 500

    @staticmethod
    @verificar_token
    def cadastrar_servico():
        try:
            # Permitir admin ou o próprio cabeleireiro (dependendo da sua regra)
            if not getattr(request, "is_admin", False) and not getattr(request, "user_id", None):
                return jsonify({"erro": "Acesso negado. Apenas administradores ou cabeleireiros autenticados podem cadastrar serviços."}), 403

            data = request.get_json() or {}
            nome = data.get("nome")
            preco = data.get("preco")
            cabeleireiro_id = data.get("cabeleireiro_id") or getattr(request, "user_id", None)

            if not nome or preco is None or not cabeleireiro_id:
                return jsonify({"erro": "Campos obrigatórios ausentes"}), 400

            # Verifica se cabeleireiro existe
            cabe = Cabeleireiro.query.get(cabeleireiro_id)
            if not cabe:
                return jsonify({"erro": "Cabeleireiro não encontrado"}), 404

            servico = Servico(nome=nome, preco=preco, cabeleireiro_id=cabeleireiro_id)
            db.session.add(servico)
            db.session.commit()

            return jsonify({
                "mensagem": "Serviço cadastrado com sucesso!",
                "servico": {
                    "id": servico.id,
                    "nome": servico.nome,
                    "preco": servico.preco,
                    "cabeleireiro_id": servico.cabeleireiro_id
                }
            }), 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"erro": "Erro ao salvar serviço no banco", "detalhes": str(e)}), 500
        except Exception as e:
            return jsonify({"erro": "Erro interno", "detalhes": str(e)}), 500

    @staticmethod
    def login():
        try:
            data = request.get_json() or {}
            email = data.get("email")
            senha = data.get("senha")

            if not email or not senha:
                return jsonify({"erro": "Email e senha são obrigatórios"}), 400

            cabeleireiro = Cabeleireiro.query.filter_by(email=email).first()
            if not cabeleireiro:
                return jsonify({"erro": "Credenciais inválidas"}), 401

            if not check_password_hash(cabeleireiro.senha, senha):
                return jsonify({"erro": "Credenciais inválidas"}), 401

            token = gerar_token(cabeleireiro.id)
            return jsonify({
                "token": token,
                "cabeleireiro": {
                    "id": cabeleireiro.id,
                    "nome": cabeleireiro.nome,
                    "email": cabeleireiro.email,
                    "is_admin": bool(cabeleireiro.is_admin)
                }
            }), 200

        except Exception as e:
            return jsonify({"erro": "Erro interno", "detalhes": str(e)}), 500

    @staticmethod
    @verificar_token
    def listar_cabeleireiros():
        try:
            cabeleireiros = Cabeleireiro.query.filter_by(is_admin=False).all()
            resultado = []
            for c in cabeleireiros:
                resultado.append({
                    "id": c.id,
                    "nome": c.nome,
                    "email": c.email,
                    "servicos": [s.to_dict() for s in getattr(c, "servicos", [])]
                })
            return jsonify(resultado), 200
        except Exception as e:
            return jsonify({"erro": "Erro ao listar cabeleireiros", "detalhes": str(e)}), 500

    @staticmethod
    @verificar_token
    def perfil_cabeleireiro():
        try:
            cabeleireiro_id = getattr(request, "user_id", None)
            if not cabeleireiro_id:
                return jsonify({"erro": "Token inválido ou ausente"}), 401

            cabeleireiro = Cabeleireiro.query.get(cabeleireiro_id)
            if not cabeleireiro:
                return jsonify({"erro": "Cabeleireiro não encontrado"}), 404

            
            avaliacoes = cabeleireiro.avaliacoes.all()
            if avaliacoes:
                nota_media = sum(a.nota for a in avaliacoes) / len(avaliacoes)
                nota_media = round(nota_media, 1)  
            else:
                nota_media = "N/A"  
            

            servicos = [s.to_dict() for s in getattr(cabeleireiro, "servicos", [])]

            agendamentos = Agendamento.query.filter_by(cabeleireiro_id=cabeleireiro.id).all()
            agendamentos_data = []
            for ag in agendamentos:
                agendamentos_data.append({
                    "id": ag.id,
                    "cliente_id": ag.cliente_id,
                    "cliente_nome": getattr(ag, "cliente").nome if getattr(ag, "cliente", None) else None,
                    "servico": ag.servico,
                    "data": ag.data.strftime("%Y-%m-%d") if ag.data else None,
                    "hora": ag.hora.strftime("%H:%M") if ag.hora else None,
                    "status": ag.status
                })

            perfil = {
                "id": cabeleireiro.id,
                "nome": cabeleireiro.nome,
                "email": cabeleireiro.email,
                "servicos": servicos,
                "agendamentos": agendamentos_data,
                "nota_media": nota_media 
            }

            return jsonify(perfil), 200

        except Exception as e:
            return jsonify({"erro": "Erro ao carregar perfil do cabeleireiro", "detalhes": str(e)}), 500

    @staticmethod
    @verificar_token
    def concluir_agendamento(agendamento_id):
        try:
            agendamento = Agendamento.query.get(agendamento_id)
            if not agendamento:
                return jsonify({"erro": "Agendamento não encontrado"}), 404

        # Obter o ID do usuário logado
            cabeleireiro_id = getattr(request, "user_id", None)

        # Verificar permissões
            if getattr(request, "is_admin", False):
                allowed = True
            elif agendamento.cabeleireiro_id == cabeleireiro_id:
                allowed = True
            else:
                allowed = False

            if not allowed:
                return jsonify({"erro": "Acesso negado. Apenas o cabeleireiro responsável ou admin podem concluir."}), 403

            if agendamento.status != "pendente":
                return jsonify({"erro": "Agendamento já foi concluído ou cancelado"}), 400

            agendamento.status = "concluido"
            db.session.commit()

            return jsonify({"mensagem": "Agendamento concluído com sucesso!"}), 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"erro": "Erro ao atualizar agendamento", "detalhes": str(e)}), 500
        except Exception as e:
            return jsonify({"erro": "Erro interno", "detalhes": str(e)}), 500

    @staticmethod
    @verificar_token
    def cadastrar_cabeleireiro_pelo_admin():
        try:
            if not getattr(request, "is_admin", False):
                return jsonify({"erro": "Acesso negado. Apenas o admin pode cadastrar cabeleireiros."}), 403

            data = request.get_json() or {}
            nome = data.get("nome")
            email = data.get("email")
            senha = data.get("senha")

            if not nome or not email or not senha:
                return jsonify({"erro": "Campos obrigatórios ausentes"}), 400

            if Cabeleireiro.query.filter_by(email=email).first():
                return jsonify({"erro": "Email já cadastrado"}), 400

            senha_hash = generate_password_hash(senha, method="pbkdf2:sha256:260000")
            cabeleireiro = Cabeleireiro(nome=nome, email=email, senha=senha_hash, is_admin=False)

            db.session.add(cabeleireiro)
            db.session.commit()

            return jsonify({
                "mensagem": "Cabeleireiro cadastrado com sucesso pelo admin!",
                "cabeleireiro": {
                    "id": cabeleireiro.id,
                    "nome": cabeleireiro.nome,
                    "email": cabeleireiro.email
                }
            }), 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"erro": "Erro ao salvar no banco", "detalhes": str(e)}), 500
        except Exception as e:
            return jsonify({"erro": "Erro interno", "detalhes": str(e)}), 500