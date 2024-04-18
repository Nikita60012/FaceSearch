from datetime import date

from pydantic import BaseModel


class BuySubscribe(BaseModel):
    days: int = 0
    slots: int = 0
    last_authorization: date = date.today()
