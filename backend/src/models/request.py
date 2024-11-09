from pydantic import BaseModel


class AnalyzeSessionsData(BaseModel):
    urls: list[str]
    parameters: list[int]
