from pydantic import BaseModel


class AuthClient(BaseModel):
    email: str = 'email'
    ip: str = "0.0.0.0"
    password: str = '*********'
