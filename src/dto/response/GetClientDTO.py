from pydantic import BaseModel


class GetClient(BaseModel):
    email: str = 'email'
    phone: str = 'phone'
    slots: int = 0
    days: int = 0
    slots_occupied: int = 0
