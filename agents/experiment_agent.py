from typing import Dict, List
from llm_base import llm_call
from mcp.server.fastmcp import FastMCP

mcp = FastMCP('Experiment-Agent')

prompt_base = f"""
You are a scientific research assistant.

Your task:
1. Read the extracted hypotheses.
2. Generate testable experiment steps derived from these hypotheses.
3. Explain steps in easy and scientific manner.
4. Explain the reasoning over the experiment steps.

STRICT OUTPUT FORMAT (valid JSON only, no markdown, no commentary):

{
  "experiment_id": 1,
  "ExperimentSteps": [
    {
      "step_id": int",
      "ExperimentStep": "<steps text>",
      "reason": "<why these are steps>"
    }
  ]
}

Rules:
- Experiment steps must be logically derived from assumptions.
- Do NOT restate assumptions verbatim.
- Do NOT summarize the paper.
- Do NOT restate hypotheses verbatim.
- Do NOT output anything outside the JSON object.
"""

