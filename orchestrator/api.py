from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from orchestrator.pipeline import ResearchOrchestrator

app = FastAPI(title="ScientistAI")

orchestrator = ResearchOrchestrator()


class PaperRequest(BaseModel):
    paper_text: str


@app.post("/analyze")
async def analyze_paper(request: PaperRequest):
    try:
        result = await orchestrator.run(request.paper_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
