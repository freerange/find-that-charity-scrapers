"""Table setup

Revision ID: e8f5209ff685
Revises: 
Create Date: 2019-09-13 13:54:30.178701

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8f5209ff685'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('organisation',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('charityNumber', sa.String(), nullable=True),
    sa.Column('companyNumber', sa.String(), nullable=True),
    sa.Column('addressLocality', sa.String(), nullable=True),
    sa.Column('addressRegion', sa.String(), nullable=True),
    sa.Column('addressCountry', sa.String(), nullable=True),
    sa.Column('postalCode', sa.String(), nullable=True),
    sa.Column('telephone', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('latestIncome', sa.BigInteger(), nullable=True),
    sa.Column('latestIncomeDate', sa.Date(), nullable=True),
    sa.Column('dateRegistered', sa.Date(), nullable=True),
    sa.Column('dateRemoved', sa.Date(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('parent', sa.String(), nullable=True),
    sa.Column('dateModified', sa.DateTime(), nullable=True),
    sa.Column('location', sa.JSON(), nullable=True),
    sa.Column('OrgIDs', sa.JSON(), nullable=True),
    sa.Column('alternateName', sa.JSON(), nullable=True),
    sa.Column('organisationType', sa.JSON(), nullable=True),
    sa.Column('organisationTypePrimary', sa.String(), nullable=True),
    sa.Column('source', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organisation_links',
    sa.Column('organisation_id_a', sa.String(), nullable=False),
    sa.Column('organisation_id_b', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('source', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('organisation_id_a', 'organisation_id_b')
    )
    op.create_table('source',
    sa.Column('identifier', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('license', sa.String(), nullable=True),
    sa.Column('license_name', sa.String(), nullable=True),
    sa.Column('issued', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('publisher_name', sa.String(), nullable=True),
    sa.Column('publisher_website', sa.String(), nullable=True),
    sa.Column('distribution', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('identifier')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('source')
    op.drop_table('organisation_links')
    op.drop_table('organisation')
    # ### end Alembic commands ###
