from sqlalchemy import MetaData, Integer, String, TIMESTAMP, Table, Column, ForeignKey, Boolean

from src.dao.ClientDAO import client

metadata = MetaData()

authSessions = Table(
    'authorization_session',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('id_client', Integer, ForeignKey(client.c.id, ondelete='CASCADE',)),
    Column('token', String(1000), nullable=False, unique=True),
    Column('enter_date', TIMESTAMP, nullable=False),
    Column('out_date', TIMESTAMP, nullable=True),
    Column('ip', String, nullable=False),
    Column('actual', Boolean, nullable=False)
)
