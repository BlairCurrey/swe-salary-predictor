"""create prediction_inputs table

Revision ID: f414a9333503
Revises: 
Create Date: 2022-06-12 14:01:55.985969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f414a9333503'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'prediction_inputs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('years_coding', sa.Integer, nullable=False),
        sa.Column('years_coding_pro', sa.Integer, nullable=False),
    )

def downgrade():
    op.drop_table('prediction_inputs')
