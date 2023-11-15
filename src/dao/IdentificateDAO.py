from sqlalchemy import MetaData, Integer, String, TIMESTAMP, Table, Column, LargeBinary

metadata = MetaData()

worker_identifications = Table(
    'worker_identifications',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=True),
    Column('date', TIMESTAMP, nullable=True),
    Column('worker_photo', LargeBinary, nullable=True),
    Column('person_to_detect', LargeBinary, nullable=True),
    Column('conclusion', String, nullable=True)
)
