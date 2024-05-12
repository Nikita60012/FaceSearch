from datetime import date

from pydantic import BaseModel


class GetPeoples(BaseModel):
    id: int = 0
    fullname: str = "name"
