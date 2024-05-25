from pydantic import BaseModel


class GetTokenClientDTO(BaseModel):
    enter: bool = False,
    token: str = "xxx.xxx.xxx"
