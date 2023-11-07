from datetime import datetime
from PIL.JpegImagePlugin import JpegImageFile
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import LargeBinary, BLOB


class BinaryLarge(BLOB):
    pass


class AddWorker(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: int
    fullname: str
    birthdate: datetime
    phone: str
    # photo: BLOB = Field(None, alias='BLOB')


class UpdateWorker(BaseModel):
    id: int
    fullname: str
    birthdate: datetime
    phone: str
