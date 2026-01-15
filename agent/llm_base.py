import os
import httpx
import asyncio
from typing import Dict, Any

api_key = os.getenv("OPENROUTER_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

URL = "https://openrouter.ai/api/v1/chat/completions"

PROMPT_BASE = (
    "You are a research assistant. "
    "Follow the task instructions strictly."
)

# Simple semaphore for load protection
_semaphore = asyncio.Semaphore(5)  # max 5 concurrent calls


async def llm_call(prompt: str) -> Dict[str, Any]:
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": PROMPT_BASE},
            {"role": "user", "content": prompt}
        ]
    }

    async with _semaphore:
        async with httpx.AsyncClient(timeout=20) as client:
            try:
                response = await client.post(URL, json=data, headers=HEADERS)

                if response.status_code == 429:
                    return {
                        "error": "RATE_LIMITED",
                        "status": 429
                    }

                if response.status_code != 200:
                    return {
                        "error": "LLM_HTTP_ERROR",
                        "status": response.status_code,
                        "body": response.text
                    }

                result = response.json()

                return {
                    "content": result["choices"][0]["message"]["content"],
                    "usage": result.get("usage", {})
                }

            except httpx.TimeoutException:
                return {
                    "error": "TIMEOUT"
                }

            except Exception as e:
                return {
                    "error": "LLM_CALL_FAILED",
                    "details": str(e)
                }
