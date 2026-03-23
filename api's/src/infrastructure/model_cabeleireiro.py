from src.config.data_base import db
import enum

class StatusAgendamento(enum.Enum):
    PENDENTE = "pendente"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"

class Cabeleireiro(db.Model):
    __tablename__ = "cabeleireiros"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(600), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


    servicos = db.relationship(
        "Servico",
        backref="cabeleireiro",
        cascade="all, delete-orphan"
    )

    agendamentos = db.relationship(
        "Agendamento",
        backref="cabeleireiro_agendamento",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "servicos": [s.to_dict() for s in self.servicos],
        }