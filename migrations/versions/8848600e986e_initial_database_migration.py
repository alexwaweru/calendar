"""initial database migration

Revision ID: 8848600e986e
Revises: 
Create Date: 2019-10-11 17:25:37.513029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8848600e986e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('eventId', sa.String(length=255), nullable=False),
    sa.Column('createdByEmail', sa.String(length=255), nullable=False),
    sa.Column('eventDateAndTime', sa.DateTime(), nullable=False),
    sa.Column('timeFormat', sa.String(), nullable=False),
    sa.Column('attendees', sa.Text(), nullable=False),
    sa.Column('createdAt', sa.DateTime(), nullable=False),
    sa.Column('updatedAt', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('eventId')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uid', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('firstName', sa.String(length=255), nullable=False),
    sa.Column('lastName', sa.String(length=255), nullable=False),
    sa.Column('country', sa.String(length=255), nullable=False),
    sa.Column('phoneNumber', sa.String(length=255), nullable=False),
    sa.Column('legalName', sa.String(length=255), nullable=False),
    sa.Column('businessLegalEntity', sa.String(length=255), nullable=False),
    sa.Column('businessLegalEntityOrg', sa.String(length=255), nullable=False),
    sa.Column('insurerRepresenting', sa.String(length=255), nullable=False),
    sa.Column('insurerAdminEmail', sa.String(length=255), nullable=False),
    sa.Column('userType', sa.String(length=255), nullable=False),
    sa.Column('emailConfirmed', sa.Boolean(), nullable=False),
    sa.Column('phoneConfirmed', sa.Boolean(), nullable=False),
    sa.Column('profileComplete', sa.Boolean(), nullable=False),
    sa.Column('isActive', sa.Boolean(), nullable=False),
    sa.Column('createdAt', sa.DateTime(), nullable=False),
    sa.Column('updatedAt', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phoneNumber'),
    sa.UniqueConstraint('uid')
    )
    op.create_table('user_group',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('userGroupId', sa.String(length=255), nullable=False),
    sa.Column('groupName', sa.String(length=255), nullable=False),
    sa.Column('createdAt', sa.DateTime(), nullable=False),
    sa.Column('updatedAt', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('groupName'),
    sa.UniqueConstraint('userGroupId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_group')
    op.drop_table('user')
    op.drop_table('event')
    # ### end Alembic commands ###