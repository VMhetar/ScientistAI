import json
from typing import Dict

from  agent.assumption_agent import assumption_agent
from agent.hypothesis_agent import hypothesis_agent
from agent.experiment_agent import experiment_agent


import json
import time
import uuid
import logging

logging.basicConfig(level=logging.INFO)


class ResearchOrchestrator:
    async def run(self, paper_text: str):
        request_id = str(uuid.uuid4())
        experiment_id = 1

        logging.info(f"[{request_id}] Pipeline started")

        assumptions = await self._run_stage(
            name="assumption_agent",
            func=lambda: assumption_agent(paper_text, experiment_id),
            request_id=request_id
        )

        hypotheses = await self._run_stage(
            name="hypothesis_agent",
            func=lambda: hypothesis_agent(json.dumps(assumptions), experiment_id),
            request_id=request_id
        )

        experiments = await self._run_stage(
            name="experiment_agent",
            func=lambda: experiment_agent(json.dumps(hypotheses), experiment_id),
            request_id=request_id
        )

        logging.info(f"[{request_id}] Pipeline completed")

        return {
            "experiment_id": experiment_id,
            "assumptions": assumptions,
            "hypotheses": hypotheses,
            "experiments": experiments
        }

    async def _run_stage(self, name, func, request_id):
        logging.info(f"[{request_id}] {name} started")
        start = time.time()

        raw = await func()

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            logging.error(
                f"[{request_id}] {name} returned invalid JSON:\n{raw}"
            )
            raise

        duration = time.time() - start
        logging.info(
            f"[{request_id}] {name} completed in {duration:.2f}s"
        )

        return parsed
