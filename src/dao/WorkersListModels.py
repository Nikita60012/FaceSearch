from sqlalchemy import MetaData, Integer, String, Table, Column, LargeBinary, Date, ARRAY, Float

metadata = MetaData()

worker = Table(
    'worker',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('fullname', String, nullable=True, unique=True),
    Column('birthdate', Date, nullable=True),
    Column('phone', String, nullable=True),
    Column('photo', LargeBinary, nullable=True),
    Column('descriptor', ARRAY(Float), nullable=True)
)
