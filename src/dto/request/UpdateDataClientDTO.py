from pydantic import BaseModel


class UpdateDataClient(BaseModel):
    email: str = 'email'
    password: str = ''
    phone: str = 'phone'
