from datetime import datetime
from pydantic import BaseModel


class AddWorker(BaseModel):

    id: int
    fullname: str
    birthdate: datetime
    phone: str


class UpdateWorker(BaseModel):
    id: int
    fullname: str
    birthdate: datetime
    phone: str
