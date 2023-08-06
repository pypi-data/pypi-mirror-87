import enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class CPEProvTypeENUM(enum.Enum):
    bridge = 'bridge'
    gateway = 'gateway'


class ServiceProvStatusENUM(enum.Enum):
    provisioned = 'provisioned'
    suspended = 'suspended'


def repr(obj):
    cols = []
    for k in obj.__class__.__dict__.keys():
        if not str(k).startswith('_'):
            cols.append(f'{k}={obj.__getattribute__(k)}')
    return f'<{obj.__class__.__name__}({",".join(cols)})>'


class SUBSCRIPTION(Base):
    __tablename__ = 'subscription'

    id = Column(Integer, primary_key=True)
    ont_id = Column(Integer, ForeignKey('ont.id'), nullable=False)
    cust_id = Column(String(length=128), nullable=False, comment='Billing system customer ID')
    subs_id = Column(String(length=128), nullable=False, unique=True, comment='Billing system subscription ID')
    cid = Column(String(length=128), nullable=False, unique=True, comment='Circuit ID')
    name = Column(String(length=64), nullable=False, comment='Name of the service')
    status = Column(Enum(ServiceProvStatusENUM), nullable=False, comment='Service status')
    provision_datetime = Column(DateTime, comment='Datetime when service was provisioned')

    ont = relationship('ONT', back_populates='subscription')

    def __repr__(self):
        return repr(self)


class RADCHECK(Base):
    __tablename__ = 'radcheck'

    id = Column(Integer, primary_key=True)
    username = Column(String(length=128), unique=True, nullable=False, default='')
    attribute = Column(String(length=128), nullable=False, default='')
    op = Column(String(length=2), nullable=False, default='==')
    value = Column(String(length=128), nullable=False, default='')

    def __repr__(self):
        return repr(self)


class RADUSERGROUP(Base):
    __tablename__ = 'radusergroup'

    id = Column(Integer, primary_key=True)
    username = Column(String(length=128), nullable=False, default='')
    groupname = Column(String(length=128), nullable=False, default='')
    priority = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return repr(self)
