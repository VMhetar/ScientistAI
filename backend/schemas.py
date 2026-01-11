from pydantic import BaseModel
from typing import Any,Dict

class PaperRequest(BaseModel):
    paper_text: str


class ResearchResponse(BaseModel):
    experiment_id: int
    assumptions: Dict[str, Any]
    hypotheses: Dict[str, Any]
    experiments: Dict[str, Any]