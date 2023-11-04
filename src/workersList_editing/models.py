from sqlalchemy import MetaData, Integer, String, TIMESTAMP, Table, Column
from sqlalchemy.orm import Mapped, mapped_column

# from sqlalchemy_imageattach.entity import Image, image_attachment
from src.database import Base

metadata = MetaData()

worker = Table(
    'worker',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('fullname', String, nullable=True),
    Column('birthdate', TIMESTAMP, nullable=True),
    Column('phone', String, nullable=True),
    # Column('photo', image_attachment(), primary_key=True),
)


# class Worker(Base):
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     fullname: Mapped[str] = mapped_column(String, nullable=True)
#     birthdate: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=True)
#     phone: Mapped[str] = mapped_column(String, nullable=True)
