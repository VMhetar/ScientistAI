"""
This module contains the logic for experiment agent.
This agent helps in creating experiment steps from the created hypothesis.
The experiment steps are stored in a structured JSON format. 
"""
from llm_base import llm_call
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Experiment-Agent")

prompt_base = """
You are a scientific research assistant.

Your task:
1. Read the extracted hypotheses.
2. Design falsifiable experiments to test them.
3. Break each experiment into clear, ordered steps.
4. Explain the reasoning behind each step.

STRICT OUTPUT FORMAT (valid JSON only, no markdown, no commentary):

{
  "experiment_id": 1,
  "experiment_steps": [
    {
      "step_id": 1,
      "step": "<experiment step>",
      "reason": "<why this step is necessary>"
    }
  ]
}

Rules:
- Experiment steps must be logically derived from hypotheses.
- Prefer experiments that could DISPROVE the hypothesis.
- Avoid benchmark-only or confirmatory designs.
- Do NOT restate assumptions verbatim.
- Do NOT restate hypotheses verbatim.
- Do NOT summarize the paper.
- Do NOT output anything outside the JSON object.
"""

async def experiment_agent(
    hypotheses_json: str,
    experiment_id: int = 1
):
    prompt = f"""
{prompt_base}

EXTRACTED HYPOTHESES:
\"\"\"
{hypotheses_json}
\"\"\"
"""
    response = await llm_call(prompt)
    return response
