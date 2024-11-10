import time

from fastapi import APIRouter

from src.models.request import AnalyzeSessionsData
from helpers.parser import get_documents
from helpers.prompt_generation import generate_prompts

router = APIRouter()


@router.post("/session/analyze", tags=["session"])
async def analyze_session(data: AnalyzeSessionsData):
    for url in data.urls:
        await get_documents(url)
        promts = generate_prompts(url)
        time.sleep(5)
