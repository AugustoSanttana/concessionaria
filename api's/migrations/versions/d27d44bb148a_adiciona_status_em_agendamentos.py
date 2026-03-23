"""Adiciona status em agendamentos e remove tabela user antiga

Revision ID: d27d44bb148a
Revises: 
Create Date: 2025-10-08 15:21:03.211817
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd27d44bb148a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Remove tabela antiga 'user' se ainda existir
    conn = op.get_bind()
    insp = sa.inspect(conn)
    if 'user' in insp.get_table_names():
        op.drop_table('user')

    # Adiciona a coluna 'status' na tabela 'agendamentos', caso ainda não exista
    with op.batch_alter_table('agendamentos', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('status', sa.String(length=20), nullable=False, server_default='pendente')
        )


def downgrade():
    # Remove a coluna status (caso precise reverter)
    with op.batch_alter_table('agendamentos', schema=None) as batch_op:
        batch_op.drop_column('status')
