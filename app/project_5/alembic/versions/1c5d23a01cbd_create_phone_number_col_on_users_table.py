"""create phone number col on users table

Revision ID: 1c5d23a01cbd
Revises: 
Create Date: 2025-08-05 22:30:19.973185

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c5d23a01cbd'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # it will run if "alembic upgrade <id>" is called 
    # the below line will add the nes column in the table
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True), schema='dbo')


# this function will run if we can "alembic downgrade -1" after the above upgrade
def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'phone_number')  # drop_column will delete the column along with the data
