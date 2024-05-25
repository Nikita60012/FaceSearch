from pydantic import BaseModel


class AddClient(BaseModel):
    email: str = 'email'
    password: str = ''
    phone: str = 'phone'
    ip: str = "0.0.0.0"

