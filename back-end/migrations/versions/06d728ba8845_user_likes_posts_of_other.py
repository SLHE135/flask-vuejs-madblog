"""user likes posts of other

Revision ID: 06d728ba8845
Revises: a3681c69cd41
Create Date: 2022-04-08 19:27:56.770381

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '06d728ba8845'
down_revision = 'a3681c69cd41'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts_likes',
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('post_id', sa.Integer(), nullable=True),
                    sa.Column('timestamp', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name=op.f('fk_posts_likes_post_id_posts')),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_posts_likes_user_id_users'))
                    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_posts_likes_read_time', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('last_posts_likes_read_time')

    op.drop_table('posts_likes')
    # ### end Alembic commands ###