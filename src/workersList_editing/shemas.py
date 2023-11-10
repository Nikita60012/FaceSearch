from datetime import datetime
from pydantic import BaseModel


class AddWorker(BaseModel):

    id: int = '0'
    fullname: str = 'name'
    birthdate: datetime = '2000-01-01T00:00:00'
    phone: str = 'phone'


class UpdateWorker(BaseModel):
    id: int
    fullname: str
    birthdate: datetime
    phone: str
