from pydantic import BaseModel


class GetStatus(BaseModel):
    status: bool
    type: str
