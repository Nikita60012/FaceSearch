from sqlalchemy import MetaData, Integer, String, TIMESTAMP, Table, Column, LargeBinary, ForeignKey
from src.dao.ClientDAO import client

metadata = MetaData()

worker_identifications = Table(
    'worker_identifications',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('id_client', Integer, ForeignKey(client.c.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    Column('name', String(32), nullable=False),
    Column('date', TIMESTAMP, nullable=False),
    Column('worker_photo', LargeBinary, nullable=False),
    Column('person_to_detect', LargeBinary, nullable=False),
    Column('conclusion', String(100), nullable=False)
)
