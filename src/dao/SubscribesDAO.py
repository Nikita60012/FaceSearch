from sqlalchemy import MetaData, Table, Column, Integer, ForeignKey, Date, String
from src.dao.ClientDAO import client

metadata = MetaData()

subscribe = Table(
    'subscribe',
    metadata,
    Column('id_client', Integer, ForeignKey(client.c.id, ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('end_date_of_subscribe', Date, nullable=False),
    Column('slots', Integer, nullable=False),
    Column('last_authorization', Date, nullable=False),
)
