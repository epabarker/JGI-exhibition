"""smells table

Revision ID: 1953a34a04f1
Revises: ae8688a6a6cf
Create Date: 2022-06-06 18:05:36.611810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1953a34a04f1'
down_revision = 'ae8688a6a6cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('smell',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('smell', sa.String(length=64), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_smell_rating'), 'smell', ['rating'], unique=False)
    op.create_index(op.f('ix_smell_smell'), 'smell', ['smell'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_smell_smell'), table_name='smell')
    op.drop_index(op.f('ix_smell_rating'), table_name='smell')
    op.drop_table('smell')
    # ### end Alembic commands ###
