from fastapi import APIRouter, UploadFile, File, HTTPException
from orchestrator.pipeline import ResearchOrchestrator

router = APIRouter()
orchestrator = ResearchOrchestrator()

@router.post("/analyze")
async def analyze_paper(file: UploadFile = File(...)):
    try:
        content = await file.read()
        paper_text = content.decode("utf-8", errors="ignore")

        result = await orchestrator.run(paper_text)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
