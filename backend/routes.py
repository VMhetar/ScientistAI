from fastapi import APIRouter, HTTPException
from schemas import PaperRequest, ResearchResponse
from orchestrator.pipeline import ResearchOrchestrator

router = APIRouter()
orchestrator = ResearchOrchestrator()

@router.post("/analyze", response_model=ResearchResponse)
async def analyze_paper(request: PaperRequest):
    try:
        result = await orchestrator.run(request.paper_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))