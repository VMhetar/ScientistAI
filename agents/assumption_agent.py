import os
import httpx
import asyncio
from llm_base import llm_call
from mcp.server.fastmcp import FastMCP
from typing import Dict, List
mcp = FastMCP('Assumption-Agent')

api_key = os.getenv('OPENROUTER_API_KEY')

headers = {
    'Auhorization': f'Bearer {api_key}',
    'Content-type': 'application/json'
}

url = 'https://openrouter.ai/api/v1/chat/completions'

prompt_base = f"""
    You are a research assistant whose work is to understand the papers and make assumtions out of them.
    Response should be in the form of a list of assumptions in this format ONLY :
    {
        'Experiment': int,
        'Assumptions': List[str]
        'Reasons': List[str]
    }
Do NOT write anything else.
"""

async def assumption_agent(prompt:str):
    prompt = prompt_base
    response = await llm_call(prompt)
    return response