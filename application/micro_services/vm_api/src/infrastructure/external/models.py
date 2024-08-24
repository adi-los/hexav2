from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Tenant Table
class Tenant(Base):
    __tablename__ = 'tenants'
    id = Column(Integer, Sequence('tenant_id_seq'), primary_key=True)
    tenant_id = Column(String(50), unique=True)
    tenant_name = Column(String(50))

# VNet Table
class VNet(Base):
    __tablename__ = 'vnets'
    id = Column(Integer, Sequence('vnet_id_seq'), primary_key=True)
    vnet_id = Column(String(50), unique=True)
    cidr = Column(String(50))
    name = Column(String(50))
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    
    tenant = relationship("Tenant", back_populates="vnets")

Tenant.vnets = relationship("VNet", order_by=VNet.id, back_populates="tenant")

# Bridge Table
class Bridge(Base):
    __tablename__ = 'bridges'
    id = Column(Integer, Sequence('bridge_id_seq'), primary_key=True)
    bridge_id = Column(String(50), unique=True)
    name = Column(String(50))

# VNIC Table
class VNIC(Base):
    __tablename__ = 'vnics'
    id = Column(Integer, Sequence('vnic_id_seq'), primary_key=True)
    vnic_id = Column(String(50), unique=True)
    mac_address = Column(String(50))
    bridge_id = Column(Integer, ForeignKey('bridges.id'))
    
    bridge = relationship("Bridge")

# Flavor Table
class Flavor(Base):
    __tablename__ = 'flavors'
    id = Column(Integer, Sequence('flavor_id_seq'), primary_key=True)
    flavor_id = Column(String(50), unique=True)
    name = Column(String(50))
    vcpus = Column(Integer)
    ram = Column(Integer)
    disk = Column(Integer)

# VM Table
class VM(Base):
    __tablename__ = 'vms'
    id = Column(Integer, Sequence('vm_id_seq'), primary_key=True)
    uuid = Column(String, Sequence('vm_uuid_seq'), primary_key=True)
    hostname = Column(String(50))
    uptime = Column(String(50))
    status = Column(String(50))
    
    flavor_id = Column(Integer, ForeignKey('flavors.id'))
    flavor = relationship("Flavor")
    
    os = Column(String(50))
    image = Column(String(50))
    
    vnet_id = Column(Integer, ForeignKey('vnets.id'))
    vnet = relationship("VNet")
    
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    tenant = relationship("Tenant")
    
    vnic_id = Column(Integer, ForeignKey('vnics.id'))
    vnic = relationship("VNIC")
    
    ip = Column(String(50))
    os_version = Column(String(50))
    key_name = Column(String(50))
    hypervisor = Column(String(50))
    availability_zone = Column(String(50))
    _metadata = Column(String(50))


