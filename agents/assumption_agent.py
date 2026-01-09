import os
import httpx
import asyncio
from llm_base import llm_call
from mcp.server.fastmcp import FastMCP

mcp = FastMCP('Assumption-Agent')

api_key = os.getenv('OPENROUTER_API_KEY')

headers = {
    'Auhorization': f'Bearer {api_key}',
    'Content-type': 'application/json'
}

url = 'https://openrouter.ai/api/v1/chat/completions'

prompt_base = f"""
    You are a research assistant whose work is to understand the papers and make assumtions out of them.
"""

async def assumption_agent(prompt:str):
    prompt = prompt_base
    response = llm_call(prompt)
    return response

