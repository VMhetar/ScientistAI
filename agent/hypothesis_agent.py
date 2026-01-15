"""
This module contains the logic for hypothesis agent.
This agent helps in creating hypothesis from the created assumptions.
After creating hypothesis, this is stored in a structured JSON format. 
"""
import json
from typing import Dict, List,Any
from llm_base import llm_call
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Hypothesis-Agent")

prompt_base = """
You are a scientific research assistant.

Your task:
1. Read the extracted assumptions.
2. Generate testable hypotheses derived from these assumptions.
3. Classify each hypothesis as explicit or implicit.
4. Explain why each item qualifies as a hypothesis (i.e., can be falsified).

STRICT OUTPUT FORMAT (valid JSON only, no markdown, no commentary):

{
  "experiment_id": 1,
  "hypotheses": [
    {
      "type": "explicit | implicit",
      "statement": "<hypothesis text>",
      "reason": "<why this is a hypothesis>"
    }
  ]
}

Rules:
- Hypotheses must be logically derived from assumptions.
- Do NOT restate assumptions verbatim.
- Do NOT summarize the paper.
- Do NOT invent experiments.
- Do NOT output anything outside the JSON object.
"""

async def hypothesis_agent(assumptions_json: str,experiment_id: int = 1):
    prompt = f"""
{prompt_base}

EXTRACTED ASSUMPTIONS:
\"\"\"
{assumptions_json}
\"\"\"
"""
    try: 
        response = await llm_call(prompt)
        parsed = json.loads(response)

        if "hypotheses" not in parsed:
            raise ValueError("Missing 'hypotheses' field in LLM response")
        return parsed
    
    except json.JSONDecodeError as e:
        return{
            "experiment_id": experiment_id,
            "error": "INVALID_JSON",
            "details": str(e),
            "raw_response": response
        }
    except Exception as e:
        return {
            "experiment_id": experiment_id,
            "error": "HYPOTHESIS_AGENT_FAILURE",
            "details": str(e)
        }