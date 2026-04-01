from fastapi import APIRouter
from pydantic import BaseModel
from rag.rag_service import RagSummarizeService

router = APIRouter()
rag_service = RagSummarizeService()

class RagRequest(BaseModel):
    query: str

@router.post("/summarize")
async def rag_summarize(request: RagRequest):
    result = rag_service.rag_summarize(request.query)
    return {"result": result}