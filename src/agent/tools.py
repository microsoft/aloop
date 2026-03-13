"""Tool definitions for the agent — OpenAI Responses API function tools."""

from __future__ import annotations

import json
import subprocess
import sys
import textwrap
import urllib.request
import urllib.error
from typing import Any

from storage import Storage

# ---------------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------------

TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "type": "function",
        "name": "read_file",
        "description": "Read a file from the agent workspace.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path relative to workspace root.",
                }
            },
            "required": ["path"],
        },
    },
    {
        "type": "function",
        "name": "write_file",
        "description": "Write content to a file in the agent workspace. Creates parent directories.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path relative to workspace root.",
                },
                "content": {
                    "type": "string",
                    "description": "File content to write.",
                },
            },
            "required": ["path", "content"],
        },
    },
    {
        "type": "function",
        "name": "list_files",
        "description": "List files in the agent workspace under a prefix.",
        "parameters": {
            "type": "object",
            "properties": {
                "prefix": {
                    "type": "string",
                    "description": "Directory prefix. Empty string for root.",
                    "default": "",
                }
            },
            "required": [],
        },
    },
    {
        "type": "function",
        "name": "web_search",
        "description": "Search the web and return top results. Use for research tasks.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query.",
                }
            },
            "required": ["query"],
        },
    },
    {
        "type": "function",
        "name": "fetch_url",
        "description": "Fetch a URL and return its text content (HTML stripped to text).",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to fetch.",
                }
            },
            "required": ["url"],
        },
    },
    {
        "type": "function",
        "name": "run_python",
        "description": "Execute a Python code snippet and return stdout/stderr. Use for data analysis, file generation, calculations.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python code to execute.",
                }
            },
            "required": ["code"],
        },
    },
    {
        "type": "function",
        "name": "read_iteration_log",
        "description": "Read the iteration log to see past attempts, scores, and learnings.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]

# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

_storage: Storage | None = None


def _get_storage() -> Storage:
    global _storage
    if _storage is None:
        _storage = Storage()
    return _storage


def init_tools(storage: Storage) -> None:
    """Initialize tools with the shared storage instance."""
    global _storage
    _storage = storage


def execute_tool(name: str, arguments: dict[str, Any]) -> str:
    """Execute a tool by name and return the result as a string."""
    try:
        if name == "read_file":
            return _tool_read_file(arguments["path"])
        elif name == "write_file":
            return _tool_write_file(arguments["path"], arguments["content"])
        elif name == "list_files":
            return _tool_list_files(arguments.get("prefix", ""))
        elif name == "web_search":
            return _tool_web_search(arguments["query"])
        elif name == "fetch_url":
            return _tool_fetch_url(arguments["url"])
        elif name == "run_python":
            return _tool_run_python(arguments["code"])
        elif name == "read_iteration_log":
            return _tool_read_iteration_log()
        else:
            return json.dumps({"error": f"Unknown tool: {name}"})
    except Exception as e:
        return json.dumps({"error": str(e)})


def _tool_read_file(path: str) -> str:
    content = _get_storage().read(path)
    if content is None:
        return json.dumps({"error": f"File not found: {path}"})
    # Truncate very large files
    if len(content) > 50_000:
        content = content[:50_000] + "\n\n... [truncated, file too large] ..."
    return content


def _tool_write_file(path: str, content: str) -> str:
    _get_storage().write(path, content)
    return json.dumps({"success": True, "path": path, "bytes": len(content)})


def _tool_list_files(prefix: str) -> str:
    files = _get_storage().list_files(prefix)
    return json.dumps(files[:200])  # Cap at 200 entries


def _tool_web_search(query: str) -> str:
    """Simple web search using Bing Search API if available, else DuckDuckGo lite."""
    import os

    bing_key = os.environ.get("BING_API_KEY", "")
    if bing_key:
        return _bing_search(query, bing_key)
    # Fallback: use a simple approach
    return _ddg_search(query)


def _bing_search(query: str, api_key: str) -> str:
    """Search using Bing Web Search API."""
    import urllib.parse

    url = f"https://api.bing.microsoft.com/v7.0/search?q={urllib.parse.quote(query)}&count=5"
    req = urllib.request.Request(url, headers={"Ocp-Apim-Subscription-Key": api_key})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        results = []
        for item in data.get("webPages", {}).get("value", [])[:5]:
            results.append(
                {
                    "title": item.get("name", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("snippet", ""),
                }
            )
        return json.dumps(results)
    except Exception as e:
        return json.dumps({"error": f"Bing search failed: {e}"})


def _ddg_search(query: str) -> str:
    """Minimal DuckDuckGo instant answer as fallback."""
    import urllib.parse

    url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1"
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "aloop/1.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        results = []
        if data.get("Abstract"):
            results.append(
                {
                    "title": data.get("Heading", ""),
                    "snippet": data["Abstract"],
                    "url": data.get("AbstractURL", ""),
                }
            )
        for topic in data.get("RelatedTopics", [])[:5]:
            if isinstance(topic, dict) and "Text" in topic:
                results.append(
                    {
                        "title": topic.get("Text", "")[:80],
                        "snippet": topic.get("Text", ""),
                        "url": topic.get("FirstURL", ""),
                    }
                )
        return json.dumps(results) if results else json.dumps(
            [{"note": "No results found. Try a different query."}]
        )
    except Exception as e:
        return json.dumps({"error": f"Search failed: {e}"})


def _tool_fetch_url(url: str) -> str:
    """Fetch a URL and return text content."""
    # Basic URL validation
    if not url.startswith(("http://", "https://")):
        return json.dumps({"error": "URL must start with http:// or https://"})
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "aloop/1.0"}
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        # Strip HTML tags for readability
        import re

        text = re.sub(r"<script[^>]*>.*?</script>", "", raw, flags=re.DOTALL)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        # Truncate
        if len(text) > 30_000:
            text = text[:30_000] + "\n\n... [truncated] ..."
        return text
    except Exception as e:
        return json.dumps({"error": f"Fetch failed: {e}"})


def _tool_run_python(code: str) -> str:
    """Execute Python code in a subprocess with timeout."""
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=60,
            cwd="/tmp",
        )
        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += "\nSTDERR:\n" + result.stderr
        if result.returncode != 0:
            output += f"\n[exit code: {result.returncode}]"
        return output[:20_000] if output else "(no output)"
    except subprocess.TimeoutExpired:
        return json.dumps({"error": "Code execution timed out (60s limit)"})
    except Exception as e:
        return json.dumps({"error": f"Execution failed: {e}"})


def _tool_read_iteration_log() -> str:
    """Read all iteration logs."""
    content = _get_storage().read("iteration_log.jsonl")
    if content is None:
        return "No iterations yet. This is the first run."
    # Return last 20 iterations to avoid context overflow
    lines = content.strip().split("\n")
    if len(lines) > 20:
        return f"[Showing last 20 of {len(lines)} iterations]\n" + "\n".join(
            lines[-20:]
        )
    return content
