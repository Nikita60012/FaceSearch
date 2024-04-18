from pydantic import BaseModel


class GetClient(BaseModel):
    email: str = 'email'
    phone: str = 'phone'
