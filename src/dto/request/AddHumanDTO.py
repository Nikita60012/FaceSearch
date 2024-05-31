from pydantic import BaseModel


class HumanAdd(BaseModel):
    fullname: str = 'name'
    birthdate: str = '2000-01-01'
    phone: str = 'phone'
    photo: str
