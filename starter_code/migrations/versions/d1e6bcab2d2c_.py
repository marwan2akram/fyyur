"""empty message

Revision ID: d1e6bcab2d2c
Revises: 7ed480a57cd5
Create Date: 2020-08-27 10:28:41.202156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1e6bcab2d2c'
down_revision = '7ed480a57cd5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artists', 'seeking_description')
    # ### end Alembic commands ###
