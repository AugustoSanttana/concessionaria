import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import request, jsonify
from src.config.auth import verificar_token
from src.infrastructure.model_usuario import Usuario


class PropostaController:

    @staticmethod
    @verificar_token
    def solicitar_proposta():
        data = request.get_json()

        nome_veiculo  = data.get("nome_veiculo", "")
        preco_veiculo = data.get("preco_veiculo", "")
        info_veiculo  = data.get("info_veiculo", "")
        descricao     = data.get("descricao", "")

        # Busca o usuário autenticado pelo token
        usuario = Usuario.query.get(request.user_id)
        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404

        destinatario = usuario.email
        nome_cliente = usuario.nome

        # ──────────────────────────────────────────────────
        # Configuração do e-mail — altere as variáveis de
        # ambiente ou os valores abaixo conforme sua conta.
        # ──────────────────────────────────────────────────
        EMAIL_REMETENTE = "customssaopaulo0@gmail.com"
        EMAIL_SENHA     = "hzqfgozkrmpugetf"
        SMTP_HOST       = "smtp.gmail.com"
        SMTP_PORT       = 587
        # Monta o corpo do e-mail em HTML
        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background:#f4f4f4; padding:20px;">
            <div style="max-width:600px; margin:auto; background:#fff; border-radius:10px;
                        padding:30px; border:1px solid #ddd;">
              <h2 style="color:#7c3aed;">São Paulo Customs</h2>
              <p>Olá, <strong>{nome_cliente}</strong>! 👋</p>
              <p>Recebemos sua solicitação de proposta. Veja os detalhes abaixo:</p>
              <hr style="border:none; border-top:1px solid #eee; margin:20px 0;">
              <table style="width:100%; border-collapse:collapse;">
                <tr>
                  <td style="padding:8px; font-weight:bold; color:#555;">Veículo:</td>
                  <td style="padding:8px;">{nome_veiculo}</td>
                </tr>
                <tr style="background:#f9f9f9;">
                  <td style="padding:8px; font-weight:bold; color:#555;">Informações:</td>
                  <td style="padding:8px;">{info_veiculo}</td>
                </tr>
                <tr>
                  <td style="padding:8px; font-weight:bold; color:#555;">Preço:</td>
                  <td style="padding:8px; color:#7c3aed; font-weight:bold;">{preco_veiculo}</td>
                </tr>
                <tr style="background:#f9f9f9;">
                  <td style="padding:8px; font-weight:bold; color:#555; vertical-align:top;">Descrição:</td>
                  <td style="padding:8px;">{descricao}</td>
                </tr>
              </table>
              <hr style="border:none; border-top:1px solid #eee; margin:20px 0;">
              <p style="color:#555;">Em breve um de nossos consultores entrará em contato com você pelo telefone
                <strong>{usuario.telefone}</strong> para finalizar sua proposta.</p>
              <p style="color:#888; font-size:12px;">
                São Paulo Customs · Rua dos Automóveis, 123 · São Paulo, SP
              </p>
            </div>
          </body>
        </html>
        """

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Proposta: {nome_veiculo} — São Paulo Customs"
        msg["From"]    = EMAIL_REMETENTE
        msg["To"]      = destinatario
        msg.attach(MIMEText(html, "html"))
        
        try:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.ehlo()
                server.starttls()
                server.login(EMAIL_REMETENTE, EMAIL_SENHA)
                server.sendmail(EMAIL_REMETENTE, destinatario, msg.as_string())
        except Exception as e:
            print(f"ERRO DETALHADO: {type(e).__name__}: {e}")  # ← adiciona essa linha
            return jsonify({"erro": f"Falha ao enviar e-mail: {str(e)}"}), 500

        return jsonify({
            "mensagem": f"Proposta enviada com sucesso para {destinatario}!"
        }), 200
