from pydantic import BaseModel


class CheckSubscribe(BaseModel):
    date_status: bool = False
    slots_status: bool = False
