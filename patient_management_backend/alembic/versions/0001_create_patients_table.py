from alembic import op
import sqlalchemy as sa
import enum

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

class GenderEnum(sa.Enum):
    def __init__(self):
        super().__init__('male', 'female', 'other', name='genderenum')

def upgrade():
    op.create_table(
        'patients',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True, index=True),
        sa.Column('phone', sa.String(length=15), nullable=False),
        sa.Column('gender', GenderEnum(), nullable=False),
        sa.Column('dob', sa.Date, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

def downgrade():
    op.drop_table('patients')
    GenderEnum().drop(op.get_bind(), checkfirst=False) 