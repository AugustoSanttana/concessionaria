"""corrige_fk_servicos_agendamentos

Revision ID: corrige_cabeleireiro_servico
Revises: d552373b4419
Create Date: 2025-10-31 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'corrige_cabeleireiro_servico'
down_revision = 'd552373b4419'
branch_labels = None
depends_on = None

def upgrade():
    # --- Passo 1: Garantir que todos os servicos tenham cabeleireiro_id válido ---
    # Aqui definimos todos os servicos com cabeleireiro_id inválido para NULL ou removemos
    op.execute("""
        DELETE FROM servicos 
        WHERE cabeleireiro_id IS NULL 
           OR cabeleireiro_id NOT IN (SELECT id FROM cabeleireiros)
    """)

    # --- Passo 2: Criar FK corretamente ---
    # Se a constraint já existe, podemos pular o drop
    # op.drop_constraint('servicos_ibfk_1', 'servicos', type_='foreignkey')

    op.create_foreign_key(
        'servicos_ibfk_1',    # nome da FK
        'servicos',            # tabela que recebe a FK
        'cabeleireiros',       # tabela referenciada
        ['cabeleireiro_id'],   # coluna local
        ['id'],                # coluna referenciada
        ondelete='CASCADE'     # comportamento ao deletar o cabeleireiro
    )

def downgrade():
    op.drop_constraint('servicos_ibfk_1', 'servicos', type_='foreignkey')
