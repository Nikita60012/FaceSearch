from datetime import date

from pydantic import BaseModel


class UpdateSubscribe(BaseModel):
    email: str = 'email'
    end_date_of_subscribe: date = date.today()
    slots: int = 0
    last_authorization: date = date.today()
