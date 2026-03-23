"""Tornar cabeleireiro_id obrigatório

Revision ID: d552373b4419
Revises: 7d0516fb3981
Create Date: 2025-10-31 18:04:42.141961

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd552373b4419'
down_revision = '7d0516fb3981'
branch_labels = None
depends_on = None


def upgrade():
    # Primeiro atualizar registros existentes
    op.execute("UPDATE agendamentos SET cabeleireiro_id = 1 WHERE cabeleireiro_id IS NULL")

    # Tornar a coluna NOT NULL
    with op.batch_alter_table('agendamentos') as batch_op:
        batch_op.alter_column('cabeleireiro_id',
                              existing_type=sa.Integer(),
                              nullable=False)


def downgrade():
    with op.batch_alter_table('servicos', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('servicos_ibfk_1'), 'cabeleireiros', ['cabeleireiro_id'], ['id'])

    with op.batch_alter_table('agendamentos', schema=None) as batch_op:
        batch_op.alter_column('cabeleireiro_id',
               existing_type=mysql.INTEGER(),
               nullable=True)

    op.create_table('cabelereiros',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('nome', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('email', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('senha', mysql.VARCHAR(length=600), nullable=False),
    sa.Column('is_admin', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
