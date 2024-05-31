import json
from datetime import date
from pydantic import BaseModel, model_validator


class UpdateWorker(BaseModel):
    id_client: int
    fullname: str = 'name'
    birthdate: date = '2000-01-01'
    phone: str = 'phone'
    photo: str
