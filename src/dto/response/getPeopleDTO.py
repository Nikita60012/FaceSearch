from datetime import date

from pydantic import BaseModel


class GetPeople(BaseModel):
    id: int = 0
    fullname: str = "name"
