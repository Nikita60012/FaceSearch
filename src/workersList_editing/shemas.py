import json
from datetime import date
from pydantic import BaseModel, model_validator


class AddWorker(BaseModel):
    id: int = '0'
    fullname: str = 'name'
    birthdate: date = '2000-01-01'
    phone: str = 'phone'

    @model_validator(mode="before")
    @classmethod
    def to_py_dict(cls, data):
        return json.loads(data)


class UpdateWorker(BaseModel):
    fullname: str
    birthdate: date
    phone: str
