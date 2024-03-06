"""initial migration

Revision ID: 9d92c0ee1bcb
Revises: 
Create Date: 2024-03-06 19:05:26.374823

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '9d92c0ee1bcb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# id = Column(UUID(as_uuid=True), primary_key=True)
#     name = Column(String, nullable=False)
#     image_url = Column(String, nullable=False)
#     city = Column(String, nullable=False)
#     description = Column(String, nullable=False)

def upgrade() -> None:
    op.create_table('hotels',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('image_url', sa.String(), nullable=False),
                    sa.Column('city', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('hotels')
