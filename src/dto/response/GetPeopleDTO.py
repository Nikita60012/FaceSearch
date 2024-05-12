import datetime

from pydantic import BaseModel
from typing_extensions import Union, Type


class GetPeople(BaseModel):
    fullname: str = "name"
    birthdate: str = "2000-01-01"
    phone: str = "phone"
    photo: str
