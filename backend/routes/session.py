import time

from fastapi import APIRouter

from src.models.request import AnalyzeSessionsData
from helpers.parser import get_documents

router = APIRouter()


@router.post("/session/analyze", tags=["session"])
async def analyze_session(data: AnalyzeSessionsData):
    for i in data.urls:
        await get_documents(i)
        time.sleep(5)
