from pydantic import BaseModel


class UpdateClient(BaseModel):
    email: str = 'email'
    new_password: str = ''
    old_password: str = ''
    phone: str = 'phone'
