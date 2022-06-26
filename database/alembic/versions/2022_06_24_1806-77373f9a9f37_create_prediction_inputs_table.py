"""create prediction_inputs table

Revision ID: 77373f9a9f37
Revises: 
Create Date: 2022-06-24 18:06:20.142381

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid


# revision identifiers, used by Alembic.
revision = '77373f9a9f37'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'prediction_inputs',
        sa.Column('uuid', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('years_code', sa.Integer, nullable=False),
        sa.Column('years_code_pro', sa.Integer, nullable=False),
        sa.Column('age', sa.Integer, nullable=False),
        sa.Column('age_first_code', sa.Integer, nullable=False),
        sa.Column('country', sa.String, nullable=False),
        sa.Column('ed_level', sa.String, nullable=False),
        sa.Column('dev_type', sa.ARRAY(sa.String), nullable=False),
        sa.Column('languages', sa.ARRAY(sa.String), nullable=False),
        sa.Column('salary_actual', sa.Integer, nullable=False),
    )

def downgrade() -> None:
    op.drop_table('prediction_inputs')