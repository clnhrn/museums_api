"""New Migration

Revision ID: fe8581c8a50c
Revises: 5e7328488575
Create Date: 2023-02-04 11:47:40.577276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe8581c8a50c'
down_revision = '5e7328488575'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('artworks_artist_id_fkey', 'artworks', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('artworks_artist_id_fkey', 'artworks', 'artists', ['artist_id'], ['id'])
    # ### end Alembic commands ###
