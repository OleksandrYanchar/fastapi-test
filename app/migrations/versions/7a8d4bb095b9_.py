"""empty message

Revision ID: 7a8d4bb095b9
Revises: 
Create Date: 2024-06-29 10:24:40.834334

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '7a8d4bb095b9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index('author_name_index', 'authors', ['name'], unique=False)
    op.create_table('categories',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_index('category_title_index', 'categories', ['title'], unique=False)
    op.create_table('tags',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_index('tag_title_index', 'tags', ['title'], unique=False)
    op.create_table('posts',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('author_id', sa.UUID(), nullable=False),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('body', sa.String(length=1024), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_index('post_title_index', 'posts', ['title'], unique=False)
    op.create_table('posts_categories_tags',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('postid', sa.UUID(), nullable=False),
    sa.Column('categoryid', sa.UUID(), nullable=True),
    sa.Column('tagid', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['categoryid'], ['categories.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['postid'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tagid'], ['tags.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index('posts_categories_tags_index', 'posts_categories_tags', ['postid', 'categoryid', 'tagid'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('posts_categories_tags_index', table_name='posts_categories_tags')
    op.drop_table('posts_categories_tags')
    op.drop_index('post_title_index', table_name='posts')
    op.drop_table('posts')
    op.drop_index('tag_title_index', table_name='tags')
    op.drop_table('tags')
    op.drop_index('category_title_index', table_name='categories')
    op.drop_table('categories')
    op.drop_index('author_name_index', table_name='authors')
    op.drop_table('authors')
    # ### end Alembic commands ###
