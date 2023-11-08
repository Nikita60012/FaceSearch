from sqlalchemy import MetaData, Integer, String, TIMESTAMP, Table, Column, LargeBinary

metadata = MetaData()

worker = Table(
    'worker',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('fullname', String, nullable=True),
    Column('birthdate', TIMESTAMP, nullable=True),
    Column('phone', String, nullable=True),
    Column('photo', LargeBinary, nullable=True),
    Column('descriptor', String, nullable=True)
)
