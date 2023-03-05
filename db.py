from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String , VARCHAR , DATE, TEXT , TIMESTAMP , text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import MEDIUMINT, TINYINT

from sqlalchemy.orm import Session

SQLALCHEMY_MY_URL = 'mysql+pymysql://codeaccess:dfdfdfd544545@192.168.x.x:3309/dns'

mydb = create_engine(SQLALCHEMY_MY_URL)

Sessionmy = sessionmaker(autocommit=False, autoflush=False, bind=mydb)
Base = declarative_base()

def get_my():
    db = Sessionmy()
    try:
        yield db
    finally:
        db.close()



class Domain(Base):
    __tablename__ = 'arvan_domains'
    id = Column(Integer, primary_key=True)
    domain = Column(VARCHAR(255))
    message = Column(VARCHAR(255))
    arvan_id = Column(VARCHAR(255))
    is_deleted = Column(TINYINT,default=0)
    updated_at = Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_at = Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))


class Subdomain(Base):
    __tablename__ = 'arvan_sub_domains'
    id = Column(Integer, primary_key=True)
    domain = Column(VARCHAR(255))
    sub_domain = Column(VARCHAR(255))
    arvan_id = Column(VARCHAR(255))


class Dnsrecord(Base):
    __tablename__ = 'arvan_dns'
    id = Column(Integer, primary_key=True)
    domain = Column(VARCHAR(255))
    message = Column(VARCHAR(255))
    updated_at = Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_at = Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))


def domain_insert(domain,message,a_id):
    db : Session = next(get_my())
    insert = Domain(domain=domain, message=message, arvan_id=a_id)
    db.add(insert)
    db.commit()
    db.refresh(insert)
    return insert.id

def sub_domain_insert(domain,sub,a_id):
    db : Session = next(get_my())
    insert = Subdomain(domain=domain, sub_domain=sub,arvan_id=a_id)
    db.add(insert)
    db.commit()
    db.refresh(insert)
    return insert.id


def dns_record(domain,message):
    db : Session = next(get_my())
    insert = Dnsrecord(domain=domain , message=message)
    db.add(insert)
    db.commit()
    db.refresh(insert)
    return insert.id





# Base.metadata.create_all(bind=mydb)
