"""
This module contains the logic for assumption agent.
This agent helps in creating assumptions from the provided paper.
After reading the paper, this is stored in a structured JSON format. 
"""
import os
import json
from llm_base import llm_call
from mcp.server.fastmcp import FastMCP
from typing import List, Dict,Any

mcp = FastMCP("Assumption-Agent")

prompt_base = """
You are a scientific research assistant.

Your task:
1. Read the provided research paper text.
2. Extract BOTH explicit and implicit assumptions.
3. Explain briefly why each item is an assumption.

STRICT OUTPUT FORMAT (valid JSON only, no markdown, no commentary):

{
  "experiment_id": 1,
  "assumptions": [
    {
      "type": "explicit | implicit",
      "statement": "<assumption text>",
      "reason": "<why this is an assumption>"
    }
  ]
}

Rules:
- Do NOT summarize the paper.
- Do NOT invent experiments not mentioned.
- Do NOT output anything outside the JSON object.
"""

async def assumption_agent(paper_text: str,experiment_id: int = 1) -> Dict[str, Any]:

    prompt = f"""
{prompt_base}

PAPER TEXT:
\"\"\"
{paper_text}
\"\"\"
"""

    try:
        llm_result = await llm_call(prompt)

        # Handle LLM transport-level errors
        if "error" in llm_result:
            return {
                "experiment_id": experiment_id,
                "error": llm_result["error"],
                "details": llm_result
            }

        raw_content = llm_result["content"]
        parsed = json.loads(raw_content)

        # Minimal schema validation
        if "assumptions" not in parsed:
            raise ValueError("Missing 'assumptions' field in LLM response")

        return parsed

    except json.JSONDecodeError as e:
        return {
            "experiment_id": experiment_id,
            "error": "INVALID_JSON",
            "details": str(e),
            "raw_response": raw_content
        }

    except Exception as e:
        return {
            "experiment_id": experiment_id,
            "error": "ASSUMPTION_AGENT_FAILURE",
            "details": str(e)
        }
