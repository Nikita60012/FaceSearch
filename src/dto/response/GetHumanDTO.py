import datetime

from pydantic import BaseModel
from typing_extensions import Union, Type


class GetHuman(BaseModel):
    fullname: str = "name"
    birthdate: str = "2000-01-01"
    phone: str = "phone"
