import enum

from fibrenest_db_models.common import *
from sqlalchemy.dialects.postgresql import INET, MACADDR
from sqlalchemy import Text, text, BigInteger, Index


class ONTSwapType(enum.Enum):
    old_to_new = 'old_to_new'
    old_to_old = 'old_to_old'
    new_to_new = 'new_to_new'


class ONTSwapStatus(enum.Enum):
    pending = 'pending'
    started = 'started'
    success = 'success'
    failed = 'failed'
    cancelled = 'cancelled'


class ONTMigrationStatus(enum.Enum):
    pending = 'pending'
    started = 'started'
    success = 'success'
    failed = 'failed'
    cancelled = 'cancelled'


class VelopType(enum.Enum):
    branded = 'branded'
    unbranded = 'unbranded'


class ONT(Base):
    __tablename__ = 'ont'

    id = Column(Integer, primary_key=True)
    sn = Column(String(length=64), nullable=False, unique=True)
    portid = Column(Integer, nullable=False)
    slotid = Column(Integer, nullable=False)
    frameid = Column(Integer, nullable=False)
    ontid = Column(Integer)
    model = Column(String(length=64))
    netbox_siteid = Column(Integer)
    olt_ip = Column(INET, nullable=False)
    sitename = Column(String(length=256))
    ont_registered = Column(Boolean, nullable=False, default=False, comment='If the ONT is registered on the OLT or not')
    ont_register_datetime = Column(DateTime)
    prov_type = Column(Enum(CPEProvTypeENUM), comment='Provisioning type of the ONT. Valid values: bridge or gateway')
    s_vlan = Column(Integer)
    c_vlan = Column(Integer)

    subscription = relationship('SUBSCRIPTION', back_populates='ont')

    def __repr__(self):
        return repr(self)


class RADACCT(Base):
    __tablename__ = 'radacct'
    __table_args__ = (
        Index('radacct_bulk_close', 'nasipaddress', 'acctstarttime'),
        Index('radacct_start_user_idx', 'acctstarttime', 'username')
    )

    radacctid = Column(BigInteger, primary_key=True, server_default=text("nextval('radacct_radacctid_seq'::regclass)"))
    acctsessionid = Column(Text, nullable=False)
    acctuniqueid = Column(Text, nullable=False, unique=True)
    username = Column(Text)
    realm = Column(Text)
    nasipaddress = Column(INET, nullable=False)
    nasportid = Column(Text)
    nasporttype = Column(Text)
    acctstarttime = Column(DateTime(True))
    acctupdatetime = Column(DateTime(True))
    acctstoptime = Column(DateTime(True))
    acctinterval = Column(BigInteger)
    acctsessiontime = Column(BigInteger)
    acctauthentic = Column(Text)
    connectinfo_start = Column(Text)
    connectinfo_stop = Column(Text)
    acctinputoctets = Column(BigInteger)
    acctoutputoctets = Column(BigInteger)
    calledstationid = Column(Text)
    callingstationid = Column(Text)
    acctterminatecause = Column(Text)
    servicetype = Column(Text)
    framedprotocol = Column(Text)
    framedipaddress = Column(INET)
    qos_profile = Column(Text)
    framedipv6address = Column(INET)
    delegatedipv6prefix = Column(INET)
    acctipv6inputoctets = Column(BigInteger)
    acctipv6outputoctets = Column(BigInteger)
    cpe_mac = Column(MACADDR)
    user_group = Column(Text)

    def __repr__(self):
        return repr(self)


class ONTSWAP(Base):
    __tablename__ = 'ont_swaps'

    id = Column(Integer, primary_key=True)
    swap_type = Column(Enum(ONTSwapType), nullable=False, comment='Type of ont swap')
    swap_status = Column(Enum(ONTSwapStatus), default='pending')
    old_sn = Column(String(length=64), nullable=False, comment='OLD ONT SN')
    new_sn = Column(String(length=64), nullable=False, comment='NEW ONT SN')
    old_portid = Column(Integer, nullable=False)
    old_slotid = Column(Integer, nullable=False)
    old_frameid = Column(Integer, nullable=False)
    old_ontid = Column(Integer, nullable=False)
    old_siteid = Column(Integer, nullable=False)
    old_olt_ip = Column(INET, nullable=False)
    old_sitename = Column(String(length=256), nullable=False)
    new_olt_ip = Column(INET, nullable=False)
    new_siteid = Column(Integer, nullable=False)
    new_sitename = Column(String(length=256), nullable=False)
    new_site_shortname = Column(String(length=12), nullable=False)
    cust_id = Column(String(length=64), nullable=False, comment='Billing system Customer ID')
    subs_id = Column(String(length=64), nullable=False, comment='Billing system Subscription ID')
    old_ucr = Column(String(length=64), nullable=False)
    old_ont_register_datetime = Column(DateTime)
    old_service_provision_datetime = Column(DateTime)
    old_ont_expunged = Column(Boolean, default=False)
    old_ont_expunge_datetime = Column(DateTime)
    new_db_record_created = Column(Boolean, default=False)
    new_db_record_created_datetime = Column(DateTime)
    deleted_from_tr069 = Column(Boolean, default=False)
    deleted_from_tr069_datetime = Column(DateTime)
    user = Column(String(length=256), nullable=False, comment='user who requested the swap')
    task_request_datetime = Column(DateTime)
    task_finish_datetime = Column(DateTime)
    notification_sent_type = Column(String(length=24))
    notification_sent_datetime = Column(DateTime)
    cancel_reason = Column(String(length=256))
    cancelled_by = Column(String(length=256), comment='user who cancelled the swap')
    cancelled_at = Column(DateTime)
    error = Column(String(length=256))

    def __repr__(self):
        return repr(self)


class ONTMIGRATION(Base):
    __tablename__ = 'ont_migration'

    id = Column(Integer, primary_key=True)
    migration_status = Column(Enum(ONTMigrationStatus), default='pending')
    sn = Column(String(length=64), nullable=False, comment='ONT SN')
    ont_type = Column(Enum(CPEProvTypeENUM), nullable=False)
    velop_type = Column(Enum(VelopType))
    old_portid = Column(Integer, nullable=False, comment='OLD DB portid')
    old_slotid = Column(Integer, nullable=False, comment='OLD DB slotid')
    old_frameid = Column(Integer, nullable=False, comment='OLD DB frameid')
    old_ontid = Column(Integer, nullable=False)
    old_siteid = Column(Integer, nullable=False)
    old_olt_ip = Column(INET, nullable=False)
    old_sitename = Column(String(length=256), nullable=False)
    old_ucr = Column(String(length=64), nullable=False)
    new_olt_ip = Column(INET)
    new_siteid = Column(Integer)
    new_sitename = Column(String(length=256))
    new_site_shortname = Column(String(length=12))
    cust_id = Column(String(length=64), comment='Billing system Customer ID')
    subs_id = Column(String(length=64), comment='Billing system Subscription ID')
    old_ont_register_datetime = Column(DateTime)
    old_service_provision_datetime = Column(DateTime)
    ont_svc_port_deleted = Column(Boolean, default=False)
    ont_svc_port_deleted_datetime = Column(DateTime)
    ont_deleted_from_olt = Column(Boolean, default=False)
    ont_deleted_from_olt_datetime = Column(DateTime)
    ont_expunged = Column(Boolean, default=False)
    ont_expunge_datetime = Column(DateTime)
    new_db_record_required = Column(Boolean, default=False, comment='If DB records are required to be created')
    new_db_record_created = Column(Boolean, default=False)
    new_db_record_created_datetime = Column(DateTime)
    fr_from_tr069_done = Column(Boolean, default=False, comment='Factory reset ONT from TR069 server')
    fr_from_tr069_datetime = Column(DateTime)
    deleted_from_tr069 = Column(Boolean, default=False)
    deleted_from_tr069_datetime = Column(DateTime)
    user = Column(String(length=256), nullable=False, comment='user who requested the swap')
    task_request_datetime = Column(DateTime)
    task_finish_datetime = Column(DateTime)
    notification_sent_type = Column(String(length=24))
    notification_sent_datetime = Column(DateTime)
    cancel_reason = Column(String(length=256))
    cancelled_by = Column(String(length=256), comment='user who cancelled the migration')
    cancelled_at = Column(DateTime)
    error = Column(String(length=256))

    def __repr__(self):
        return repr(self)
