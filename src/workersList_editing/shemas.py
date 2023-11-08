from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AddWorker(BaseModel):
    # model_config = ConfigDict(arbitrary_types_allowed=True)

    id: int
    fullname: str
    birthdate: datetime
    phone: str


class UpdateWorker(BaseModel):
    id: int
    fullname: str
    birthdate: datetime
    phone: str
