from pydantic import BaseModel


class GetIdentificationResult(BaseModel):
    human_id: int = 0
    conclusion: str = "conclusion"
