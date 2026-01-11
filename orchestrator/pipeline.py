import json
from typing import Dict

from  agent.assumption_agent import assumption_agent
from agent.hypothesis_agent import hypothesis_agent
from agent.experiment_agent import experiment_agent


class ResearchOrchestrator:
    def __init__(self):
        pass

    async def run(self, paper_text: str) -> Dict:
        """
        Runs the full research reasoning pipeline:
        Paper -> Assumptions -> Hypotheses -> Experiments
        """

        experiment_id = 1

        # ---- Step 1: Assumption Extraction ----
        assumptions_raw = await assumption_agent(
            paper_text=paper_text,
            experiment_id=experiment_id
        )

        assumptions = self._safe_json_parse(
            assumptions_raw,
            stage="assumption_agent"
        )

        # ---- Step 2: Hypothesis Generation ----
        hypotheses_raw = await hypothesis_agent(
            assumptions_json=json.dumps(assumptions),
            experiment_id=experiment_id
        )

        hypotheses = self._safe_json_parse(
            hypotheses_raw,
            stage="hypothesis_agent"
        )

        # ---- Step 3: Experiment Design ----
        experiments_raw = await experiment_agent(
            hypotheses_json=json.dumps(hypotheses),
            experiment_id=experiment_id
        )

        experiments = self._safe_json_parse(
            experiments_raw,
            stage="experiment_agent"
        )

        return {
            "experiment_id": experiment_id,
            "assumptions": assumptions,
            "hypotheses": hypotheses,
            "experiments": experiments
        }

    def _safe_json_parse(self, raw_output: str, stage: str) -> Dict:
        """
        Strict JSON parser with failure visibility.
        """
        try:
            return json.loads(raw_output)
        except json.JSONDecodeError as e:
            raise RuntimeError(
                f"[{stage}] Invalid JSON output:\n{raw_output}"
            ) from e
