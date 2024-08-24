"""third migration

Revision ID: 8ae86a240afb
Revises: 86a283dfc88f
Create Date: 2024-08-21 14:30:57.176864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ae86a240afb'
down_revision: Union[str, None] = '86a283dfc88f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bridges',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bridge_id', sa.String(length=50), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('bridge_id')
    )
    op.create_table('flavors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('flavor_id', sa.String(length=50), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('vcpus', sa.Integer(), nullable=True),
    sa.Column('ram', sa.Integer(), nullable=True),
    sa.Column('disk', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('flavor_id')
    )
    op.create_table('tenants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tenant_id', sa.String(length=50), nullable=True),
    sa.Column('tenant_name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tenant_id')
    )
    op.create_table('vnets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vnet_id', sa.String(length=50), nullable=True),
    sa.Column('cidr', sa.String(length=50), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('tenant_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('vnet_id')
    )
    op.create_table('vnics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vnic_id', sa.String(length=50), nullable=True),
    sa.Column('mac_address', sa.String(length=50), nullable=True),
    sa.Column('bridge_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bridge_id'], ['bridges.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('vnic_id')
    )
    op.drop_table('users')
    op.add_column('vms', sa.Column('uuid', sa.String(), nullable=False))
    op.add_column('vms', sa.Column('hostname', sa.String(length=50), nullable=True))
    op.add_column('vms', sa.Column('uptime', sa.String(length=50), nullable=True))
    op.add_column('vms', sa.Column('status', sa.String(length=50), nullable=True))
    op.add_column('vms', sa.Column('flavor_id', sa.Integer(), nullable=True))
    op.add_column('vms', sa.Column('os', sa.String(length=50), nullable=True))
    op.add_column('vms', sa.Column('image', sa.String(length=50), nullable=True))
    op.add_column('vms', sa.Column('vnet_id', sa.Integer(), nullable=True))
    op.add_column('vms', sa.Column('tenant_id', sa.Integer(), nullable=True))
    op.add_column('vms', sa.Column('vnic_id', sa.Integer(), nullable=True))
    op.add_column('vms', sa.Column('ip', sa.String(length=50), nullable=True))
    op.add_column('vms', sa.Column('os_version', sa.String(length=50), nullable=True))
    op.add_column('vms', sa.Column('key_name', sa.String(length=50), nullable=True))
    op.add_column('vms', sa.Column('hypervisor', sa.String(length=50), nullable=True))
    op.add_column('vms', sa.Column('availability_zone', sa.String(length=50), nullable=True))
    op.add_column('vms', sa.Column('_metadata', sa.String(length=50), nullable=True))
    op.create_foreign_key(None, 'vms', 'tenants', ['tenant_id'], ['id'])
    op.create_foreign_key(None, 'vms', 'flavors', ['flavor_id'], ['id'])
    op.create_foreign_key(None, 'vms', 'vnets', ['vnet_id'], ['id'])
    op.create_foreign_key(None, 'vms', 'vnics', ['vnic_id'], ['id'])
    op.drop_column('vms', 'cpu')
    op.drop_column('vms', 'ram')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vms', sa.Column('ram', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.add_column('vms', sa.Column('cpu', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'vms', type_='foreignkey')
    op.drop_constraint(None, 'vms', type_='foreignkey')
    op.drop_constraint(None, 'vms', type_='foreignkey')
    op.drop_constraint(None, 'vms', type_='foreignkey')
    op.drop_column('vms', '_metadata')
    op.drop_column('vms', 'availability_zone')
    op.drop_column('vms', 'hypervisor')
    op.drop_column('vms', 'key_name')
    op.drop_column('vms', 'os_version')
    op.drop_column('vms', 'ip')
    op.drop_column('vms', 'vnic_id')
    op.drop_column('vms', 'tenant_id')
    op.drop_column('vms', 'vnet_id')
    op.drop_column('vms', 'image')
    op.drop_column('vms', 'os')
    op.drop_column('vms', 'flavor_id')
    op.drop_column('vms', 'status')
    op.drop_column('vms', 'uptime')
    op.drop_column('vms', 'hostname')
    op.drop_column('vms', 'uuid')
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_key')
    )
    op.drop_table('vnics')
    op.drop_table('vnets')
    op.drop_table('tenants')
    op.drop_table('flavors')
    op.drop_table('bridges')
    # ### end Alembic commands ###
