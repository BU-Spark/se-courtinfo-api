"""init config

Revision ID: 49d0e058ad13
Revises: 
Create Date: 2020-09-21 21:38:22.805294-07:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '49d0e058ad13'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('is_county_authorized', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=True)
    op.create_table('criminal_complaints',
    sa.Column('cc_id', sa.Integer(), nullable=False),
    sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('docket', sa.String(), nullable=True),
    sa.Column('number_of_counts', sa.Integer(), nullable=True),
    sa.Column('defen_name', sa.String(), nullable=True),
    sa.Column('defen_adr', sa.String(), nullable=True),
    sa.Column('defen_DOB', sa.String(), nullable=True),
    sa.Column('court_name_adr', sa.String(), nullable=True),
    sa.Column('complaint_issued_date', sa.String(), nullable=True),
    sa.Column('offense_date', sa.String(), nullable=True),
    sa.Column('arrest_date', sa.String(), nullable=True),
    sa.Column('next_event_date', sa.String(), nullable=True),
    sa.Column('next_event_type', sa.String(), nullable=True),
    sa.Column('next_event_room_session', sa.String(), nullable=True),
    sa.Column('offense_city', sa.String(), nullable=True),
    sa.Column('offense_adr', sa.String(), nullable=True),
    sa.Column('offense_codes', sa.String(), nullable=True),
    sa.Column('police_dept', sa.String(), nullable=True),
    sa.Column('police_incident_num', sa.String(), nullable=True),
    sa.Column('OBTN', sa.String(), nullable=True),
    sa.Column('PCF_number', sa.String(), nullable=True),
    sa.Column('defen_xref_id', sa.String(), nullable=True),
    sa.Column('raw_text', sa.String(), nullable=True),
    sa.Column('img_key', sa.String(), nullable=True),
    sa.Column('aws_bucket', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('cc_id')
    )
    op.create_index(op.f('ix_criminal_complaints_cc_id'), 'criminal_complaints', ['cc_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_criminal_complaints_cc_id'), table_name='criminal_complaints')
    op.drop_table('criminal_complaints')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
