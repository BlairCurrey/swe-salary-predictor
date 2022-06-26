"""empty message

Revision ID: c579ac91f3eb
Revises: 77373f9a9f37
Create Date: 2022-06-25 22:40:21.349014

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid


# revision identifiers, used by Alembic.
revision = 'c579ac91f3eb'
down_revision = '77373f9a9f37'
branch_labels = None
depends_on = None


def upgrade() -> None:
    encodings_store_table = op.create_table('encodings_store',
        sa.Column('uuid', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('bucket', sa.String, nullable=False),
        sa.Column('path', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, default=sa.func.now())
    )
    op.bulk_insert(encodings_store_table,
        [
            {'bucket': 'swe-salary-predictor-store', 'path': 'encodings.pickle'}
        ]
    )

    models_store_table = op.create_table('models_store',
        sa.Column('uuid', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('bucket', sa.String, nullable=False),
        sa.Column('path', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, default=sa.func.now())
    )
    op.bulk_insert(models_store_table,
        [
            {'bucket': 'swe-salary-predictor-store', 'path': 'model_1656041268'}
        ]
    )

def downgrade() -> None:
    op.drop_table('encodings_store')
    op.drop_table('models_store')