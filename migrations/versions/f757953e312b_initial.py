"""Initial

Revision ID: f757953e312b
Revises: 
Create Date: 2021-06-30 23:36:35.428910

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2 as ga


# revision identifiers, used by Alembic.
revision = 'f757953e312b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'gis_polygon',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('class_id', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('name', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
        sa.Column('props', sa.JSON(), autoincrement=False, nullable=True),
        sa.Column('geom', ga.types.Geometry(geometry_type="POLYGON", srid=4326), nullable=False),
        sa.Column('_created', sa.TIMESTAMP(), nullable=False),
        sa.Column('_updated', sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('gis_polygon')
