"""
This is the Base LLM module which is used to configure the LLM model required for the agents.
This module includes the url, the base prompt and a function llm_call to call the LLM.
"""

import os
import httpx
import asyncio
from mcp.server.fastmcp import FastMCP

mcp = FastMCP('127.0.0.1')

api_key = os.getenv('OPENROUTER_API_KEY')

headers = {
    'Auhorization': f'Bearer {api_key}',
    'Content-type': 'application/json'
}

url = 'https://openrouter.ai/api/v1/chat/completions'
prompt_base = f"""
You are a research assistant. Help the researcher with multiple tasks and each time you are called for a specific task, work over it
"""

async def llm_call(prompt:str):
    prompt =prompt_base
    data = {
        'model':'gpt-3.5-turbo',
        'messages':[
            {
                'role':'user',
                'content':prompt
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url=url, headers=headers, json=data)
        result = response.json()
        return result