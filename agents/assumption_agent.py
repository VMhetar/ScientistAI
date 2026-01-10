import os
from llm_base import llm_call
from mcp.server.fastmcp import FastMCP
from typing import List, Dict

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

async def assumption_agent(paper_text: str, experiment_id: int = 1):
    prompt = f"""
{prompt_base}

PAPER TEXT:
\"\"\"
{paper_text}
\"\"\"
"""
    response = await llm_call(prompt)
    return response
