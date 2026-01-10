import os
import httpx
import asyncio
from typing import Dict, List
from llm_base import llm_call
from assumption_agent import assumption_agent
from mcp.server.fastmcp import FastMCP

mcp = FastMCP('Hypothesis-Agent')

prompt_base = f"""
You are an helpful research assistant. 
Help the researchers by generating hypotheses out of the assumptions which are creted.
Hypothesis should be strcutired ONLY and should be in the format:
{
    'Experiment': str,
    'Hypothesis': List[str]
    'Reasons': List[str]
}
"""
