from pydantic import BaseModel


class AnalyzeSessionsData(BaseModel):
    auction_id: str
