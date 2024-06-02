import json
from datetime import date
from pydantic import BaseModel, model_validator


class UpdateHuman(BaseModel):
    fullname: str = 'name'
    birthdate: str = '2000-01-01'
    phone: str = 'phone'
    photo: str
