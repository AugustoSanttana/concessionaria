"""add cabeleireiro_id to agendamentos

Revision ID: 7d0516fb3981
Revises: d27d44bb148a
Create Date: 2025-10-31 16:52:18.585223
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = '7d0516fb3981'
down_revision = 'd27d44bb148a'
branch_labels = None
depends_on = None


def _has_column(table_name, column_name):
    """Verifica se a coluna já existe na tabela."""
    bind = op.get_bind()
    insp = inspect(bind)
    columns = [col['name'] for col in insp.get_columns(table_name)]
    return column_name in columns


def upgrade():
    conn = op.get_bind()

    # Só adiciona a coluna se não existir
    if not _has_column('agendamentos', 'cabeleireiro_id'):
        with op.batch_alter_table('agendamentos', schema=None) as batch_op:
            batch_op.add_column(sa.Column('cabeleireiro_id', sa.Integer(), nullable=True))
            batch_op.create_foreign_key(
                'fk_agendamento_cabeleireiro',
                'cabeleireiros',
                ['cabeleireiro_id'],
                ['id'],
                ondelete='SET NULL'
            )
            try:
                batch_op.drop_column('profissional')
            except Exception:
                pass
    else:
        print("⚠️ Coluna 'cabeleireiro_id' já existe na tabela agendamentos — ignorando criação.")

    # Verifica se existe a coluna em 'servicos'
    if not _has_column('servicos', 'cabeleireiro_id'):
        with op.batch_alter_table('servicos', schema=None) as batch_op:
            batch_op.add_column(sa.Column('cabeleireiro_id', sa.Integer(), nullable=True))
    else:
        print("⚠️ Coluna 'cabeleireiro_id' já existe na tabela servicos — ignorando criação.")


def downgrade():
    with op.batch_alter_table('agendamentos', schema=None) as batch_op:
        batch_op.drop_constraint('fk_agendamento_cabeleireiro', type_='foreignkey')
        batch_op.drop_column('cabeleireiro_id')
        batch_op.add_column(sa.Column('profissional', sa.String(100), nullable=True))

    with op.batch_alter_table('servicos', schema=None) as batch_op:
        try:
            batch_op.drop_column('cabeleireiro_id')
        except Exception:
            pass
