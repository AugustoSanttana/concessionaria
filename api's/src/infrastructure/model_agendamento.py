from src.config.data_base import db
from datetime import datetime

class Agendamento(db.Model):
    __tablename__ = "agendamentos"


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    cabeleireiro_id = db.Column(db.Integer, db.ForeignKey("cabeleireiros.id"), nullable=False)
    servico = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='pendente')

    cliente = db.relationship("Usuario", backref="agendamentos")
    cabeleireiro = db.relationship(
        "Cabeleireiro",
        backref=db.backref("agendamentos_feitos", cascade="all, delete-orphan")
    )

