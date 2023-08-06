from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


def repr(obj):
    cols = []
    for k in obj.__class__.__dict__.keys():
        if not str(k).startswith('_'):
            cols.append(f'{k}={obj.__getattribute__(k)}')
    return f'<{obj.__class__.__name__}({",".join(cols)})>'


class Site(Base):
    __tablename__ = 'sites'

    site_id = Column(INTEGER(11), primary_key=True)
    site_name = Column(String(120), nullable=False, unique=True)
    short_name = Column(String(6), nullable=False, unique=True)
    bt_vlan = Column(INTEGER(11), nullable=False, unique=True)
    postcode = Column(String(12), nullable=False)
    hub = Column(Enum('Lond', 'Manc', 'None'))
    access_ref = Column(String(20))
    service_id = Column(String(20))
    or_onea_ref = Column(String(20))
    cab_type = Column(Enum('T300', 'T500', 'None'))
    prov_state = Column(Enum('NOT_STARTED', 'ADDRESS_ALLOCATED', 'CONFIG_CREATED', 'CONFIG_PUSHED', 'CONFIG_APPLIED', 'TEST_PASS', 'ONLINE', 'CORE_CONFIG_APPLIED'), server_default=text("'NOT_STARTED'"), comment='provisioning state')
    ipam_state = Column(Enum('NOT_STARTED', 'ADDED'), nullable=False, server_default=text("'NOT_STARTED'"), comment='ipam state')

    ips = relationship('CommonIpDetail')

    def __repr__(self):
        return repr(self)


class CommonIpDetail(Base):
    __tablename__ = 'common_ip_details'

    id = Column(INTEGER(11), primary_key=True)
    site_id = Column(ForeignKey('sites.site_id'), unique=True)
    olt_in_band_management_ip = Column(String(32), unique=True)
    olt_gateway_ip = Column(String(32), unique=True)
    olt_vlan4001_ip = Column(String(32), unique=True)
    ne05_mgmt_vpn_rd = Column(INTEGER(11), unique=True)
    ne05_hsi_voice_vpn_rd = Column(INTEGER(11), unique=True)
    ne05_ont_mgmt_vpn_rd = Column(INTEGER(11), unique=True)
    ne05_public_loopback_ip = Column(String(32), unique=True)
    ne05_isis_net = Column(String(64), unique=True)
    ne05_vlan4001_ip = Column(String(32), unique=True)
    ne05_public_intf_ip = Column(String(32), unique=True)
    hub_connected_bng_public_intf_ip = Column(String(32), unique=True)
    ne05_in_band_mgmt_ip = Column(String(32), unique=True)
    ne05_olt_in_band_mgmt_network = Column(String(32), unique=True)

    site = relationship('Site')

    def __repr__(self):
        return repr(self)


class Service(Base):
    __tablename__ = 'service'

    id = Column(INTEGER(11), primary_key=True)
    site_id = Column(ForeignKey('sites.site_id'), index=True)
    pon = Column(String(32), unique=True)
    ont_id = Column(INTEGER(11))
    gpon_slot = Column(INTEGER(11), server_default=text("'1'"), comment='this is gpon_slot')
    splitter = Column(INTEGER(11), comment='this is gpon_port')
    ucr = Column(String(12), nullable=False, unique=True)
    cust_id = Column(String(32), unique=True, comment='Chargebee customer id')
    service = Column(String(12))
    prov_type = Column(String(12))
    service_profile = Column(String(10), comment='service-profile if applicable')
    ppp_prov_state = Column(Enum('NOT_STARTED', 'RADIUS_RECORD_CREATED', 'PPP_DETAILS_SET', 'FAIL'), nullable=False, server_default=text("'NOT_STARTED'"), comment='ppp provisioning state')
    ont_prov_state = Column(Enum('NOT_STARTED', 'ONT_ADDED', 'FAIL', 'REGISTERED'), nullable=False, server_default=text("'NOT_STARTED'"), comment='Ont state on OLT')
    subs_status = Column(Enum('SUSPENDED', 'DELETED'), comment='Subscription status. Null means active')
    legal_completion_date = Column(Date)
    lock_legal_comp = Column(Enum('FALSE', 'TRUE'), server_default=text("'FALSE'"), comment='if legal completion is updated manually')
    suspend_delete_datetime = Column(DateTime, comment='Datetime when subs suspended or deleted')
    ppp_set_date = Column(DateTime)
    ont_reg_date = Column(DateTime)
    pon_first_seen = Column(DateTime)

    site = relationship('Site')

    def __repr__(self):
        return repr(self)

