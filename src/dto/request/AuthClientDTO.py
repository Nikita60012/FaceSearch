from pydantic import BaseModel


class AuthClient(BaseModel):
    email: str = 'email'
    password: str = '*********'
