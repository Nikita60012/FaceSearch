from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.orm import relationship

metadata = MetaData()

client = Table(
    'client',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String(100), nullable=False, unique=True),
    Column('password', String(100), nullable=False),
    Column('phone', String(12), nullable=True),
)
