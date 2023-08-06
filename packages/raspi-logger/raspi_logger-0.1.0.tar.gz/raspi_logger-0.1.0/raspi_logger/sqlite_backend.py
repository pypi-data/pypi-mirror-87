import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, BigInteger, String, Boolean


Base = declarative_base()


class RawData(Base):
    __tablename__ = 'raw_data'

    id = Column(BigInteger, primary_key=True)
    raw_dump = Column(String, nullable=False)
    uploaded = Column(Boolean, default=False)


def connect(path) -> Session:
    engine = create_engine(path)
    SessionCls = sessionmaker(bind=engine)

    return SessionCls()


def append_data(data, conf, path=None):
    # create the correct connection path
    if path is None:
        p = os.path.join(conf.get('loggerPath'), 'rawDataLogger.db')
        path = 'sqlite://{%s}' % p
    
    # if the db file does not exist, a call of create_all is needed
    if not os.path.exists(conf.get('loggerPath')):
        session = connect(path)
        Base.metadata.create_all(session.bind)
    else:
        # file was initialized before
        session = connect(path)

    # append the data
    if not isinstance(data, list):
        data = [data]
    
    try:
        session.add_all([RawData(raw_dump=record) for record in data])
        session.commit()
    except Exception as e:
        session.rollback()
        
        # TODO, some kind of logs would be necessary here
        print(str(e))
    
    return data
    



