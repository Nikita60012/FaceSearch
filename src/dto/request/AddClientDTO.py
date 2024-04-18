from pydantic import BaseModel


class AddClient(BaseModel):
    email: str = 'email'
    password: str = ''
    phone: str = 'phone'

