"""Model client — wraps Azure OpenAI Responses API via openai/v1 path."""

from __future__ import annotations

import json
import logging
from typing import Any

from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

from config import Config

logger = logging.getLogger("aloop")


def create_client() -> OpenAI:
    """Create an OpenAI client pointed at Azure OpenAI via /openai/v1/ path."""
    if Config.LOCAL_MODE and not Config.AZURE_OPENAI_ENDPOINT:
        # For local dev with API key
        import os
        endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
        return OpenAI(
            base_url=f"{endpoint.rstrip('/')}/openai/v1/",
            api_key=os.environ.get("AZURE_OPENAI_API_KEY", ""),
        )

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default",
    )
    endpoint = Config.AZURE_OPENAI_ENDPOINT
    return OpenAI(
        base_url=f"{endpoint.rstrip('/')}/openai/v1/",
        api_key=token_provider,
    )


def call_model(
    client: OpenAI,
    instructions: str,
    prompt: str,
    tools: list[dict] | None = None,
    tool_executor: Any = None,
    max_tool_rounds: int = 15,
) -> str:
    """Call the model using the Responses API with optional tool use loop.

    Uses the OpenAI Responses API (client.responses.create) which supports
    built-in tools and multi-turn tool use natively.
    """
    input_messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": prompt},
    ]

    if not tools:
        # Simple call without tools
        response = client.responses.create(
            model=Config.AZURE_OPENAI_DEPLOYMENT,
            input=input_messages,
        )
        return _extract_text(response)

    # Tool-use loop using Responses API
    for round_num in range(max_tool_rounds):
        response = client.responses.create(
            model=Config.AZURE_OPENAI_DEPLOYMENT,
            input=input_messages,
            tools=tools,
        )

        # Check if model wants to call tools
        tool_calls = [
            item for item in response.output
            if item.type == "function_call"
        ]

        if not tool_calls:
            # Model is done — extract final text
            return _extract_text(response)

        # Append the full response output (including reasoning items) so the
        # next request has the required reasoning → function_call pairing.
        input_messages.extend(response.output)

        # Execute each tool call and feed results back
        for tc in tool_calls:
            logger.info(f"  Tool call [{round_num+1}]: {tc.name}({tc.arguments[:100]}...)")
            try:
                args = json.loads(tc.arguments)
            except json.JSONDecodeError:
                args = {}

            result = tool_executor(tc.name, args)

            input_messages.append({
                "type": "function_call_output",
                "call_id": tc.call_id,
                "output": result if isinstance(result, str) else json.dumps(result),
            })

    # Hit max rounds — get whatever the model has
    response = client.responses.create(
        model=Config.AZURE_OPENAI_DEPLOYMENT,
        input=input_messages,
    )
    return _extract_text(response)


def _extract_text(response) -> str:
    """Extract text content from a Responses API response."""
    parts = []
    for item in response.output:
        if item.type == "message":
            for content in item.content:
                if content.type == "output_text":
                    parts.append(content.text)
    return "\n".join(parts) if parts else ""
