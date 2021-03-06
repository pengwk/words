"""empty message

Revision ID: 90478e1df358
Revises: b56c2604fec1
Create Date: 2017-05-10 23:12:48.247000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '90478e1df358'
down_revision = 'b56c2604fec1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'user_ibfk_1', 'user', type_='foreignkey')
    op.drop_column('user', 'watched_videos_id')
    op.add_column('video', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'video', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'video', type_='foreignkey')
    op.drop_column('video', 'user_id')
    op.add_column('user', sa.Column('watched_videos_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key(u'user_ibfk_1', 'user', 'video', ['watched_videos_id'], ['id'])
    # ### end Alembic commands ###
