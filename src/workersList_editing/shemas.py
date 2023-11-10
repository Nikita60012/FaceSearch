import json
from datetime import datetime
from pydantic import BaseModel, model_validator


class AddWorker(BaseModel):
    id: int = '0'
    fullname: str = 'name'
    birthdate: datetime = '2000-01-01T00:00:00'
    phone: str = 'phone'

    @model_validator(mode="before")
    @classmethod
    def to_py_dict(cls, data):
        return json.loads(data)


class UpdateWorker(BaseModel):
    id: int
    fullname: str
    birthdate: datetime
    phone: str
