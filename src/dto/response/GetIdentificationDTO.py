from pydantic import BaseModel


class GetIdentification(BaseModel):
    success: bool = False
    identification_id: int = -1
