from sqlalchemy import MetaData, Integer, String, Table, Column, LargeBinary, Date, ARRAY, Float, ForeignKey
from src.dao.ClientDAO import client

metadata = MetaData()

human = Table(
    'human',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('id_client', Integer, ForeignKey(client.c.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    Column('fullname', String(32), nullable=False, unique=True),
    Column('birthdate', Date, nullable=True),
    Column('phone', String(12), nullable=True),
    Column('photo', LargeBinary, nullable=False),
    Column('descriptor', ARRAY(Float), nullable=False)
)
