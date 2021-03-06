"""which recived comments are new

Revision ID: b13222762817
Revises: 256eb4f57cd2
Create Date: 2022-04-07 15:22:52.488303

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b13222762817'
down_revision = '256eb4f57cd2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_recived_comments_read_time', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('last_recived_comments_read_time')

    # ### end Alembic commands ###
