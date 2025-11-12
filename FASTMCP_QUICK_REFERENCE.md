# FastMCP Quick Reference for Superagent Integration

## What is FastMCP at a Glance?

**FastMCP** = Production-ready Python framework for building MCP (Model Context Protocol) servers and clients.

Think of it as:
- Django/Flask for MCP (but way simpler)
- Provides decorators for tools, resources, prompts
- Handles all protocol complexity automatically
- Enterprise auth, middleware, deployment built-in

## Why it matters for Superagent

1. **Expose Superagent as MCP service**: Any IDE/CLI can use it (Claude, Cursor, Gemini, etc.)
2. **No code duplication**: Single Python API serves multiple clients
3. **Built-in auth**: Protect endpoints without custom work
4. **Enterprise-ready**: Logging, middleware, deployments included

## Minimal Example

```python
from fastmcp import FastMCP

mcp = FastMCP("My Server")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    mcp.run()
```

Run it:
```bash
fastmcp run server.py
```

## Core Concepts (5 minutes)

### 1. Tools (RPC-like functions)
```python
@mcp.tool
async def search(query: str) -> str:
    """Search for something"""
    return f"Results for {query}"
```

### 2. Resources (Read-only data)
```python
@mcp.resource("config://version")
def get_version():
    return "1.0.0"

@mcp.resource("users://{user_id}/profile")
def get_profile(user_id: int):
    return {"name": f"User {user_id}"}
```

### 3. Prompts (Reusable templates)
```python
@mcp.prompt
def summarize(text: str) -> str:
    return f"Summarize: {text}"
```

### 4. Context (Access MCP capabilities)
```python
@mcp.tool
async def process(uri: str, ctx: Context):
    await ctx.info(f"Processing {uri}...")
    result = await ctx.sample("Summarize this")
    return result.text
```

### 5. Client (Connect to MCP servers)
```python
async with Client("server.py") as client:
    result = await client.call_tool("add", {"a": 1, "b": 2})
```

## Superagent Integration Opportunities

### A. Expose confidence checker as MCP tool
```python
from superagent.api import evaluate_confidence

mcp = FastMCP("Superagent")

@mcp.tool
async def check_confidence(task: str) -> dict:
    """Pre-implementation confidence assessment"""
    result = await evaluate_confidence(task)
    return {
        "score": result.score,
        "action": result.action,
        "checklist": result.checklist
    }
```

### B. Repository indexing as resource
```python
from superagent.api import generate_repo_index

@mcp.resource("repo://index")
async def get_repo_index(path: str):
    index = await generate_repo_index(path)
    return index.content
```

### C. Protect with authentication
```python
from fastmcp.server.auth.providers.google import GoogleProvider

auth = GoogleProvider(
    client_id="...",
    client_secret="...",
    base_url="https://myserver.com"
)
mcp = FastMCP("Superagent", auth=auth)
```

### D. Middleware for PM patterns
```python
from fastmcp.server.middleware import Middleware

class ConfidenceCheckMiddleware(Middleware):
    async def process_request(self, request, call_next):
        if request.tool_name == "risky_tool":
            confidence = await evaluate_confidence(request.tool_name)
            if confidence.score < 0.7:
                return {"error": "Confidence too low"}
        return await call_next(request)

mcp = FastMCP("Superagent", middleware=[ConfidenceCheckMiddleware()])
```

## Key FastMCP Features

| Feature | Use Case |
|---------|----------|
| **Decorators** | Simple syntax for tools/resources/prompts |
| **Type hints** | Auto JSON schema generation (Pydantic) |
| **Async support** | Async/await in tools |
| **Multiple transports** | STDIO, HTTP, SSE |
| **Enterprise auth** | OAuth2, OIDC, JWT, API keys (8+ providers) |
| **Middleware** | Logging, caching, rate limiting, error handling |
| **Server composition** | Mount multiple servers |
| **Proxy pattern** | Bridge/wrap other MCP servers |
| **OpenAPI generation** | Auto-generate from specs |
| **In-memory testing** | Direct server connection (no process management) |
| **Deployment** | FastMCP Cloud or self-hosted |

## Installation

```bash
# With uv (recommended)
uv pip install fastmcp

# Or standard pip
pip install fastmcp
```

## File Structure

Key locations in FastMCP repo:

```
src/fastmcp/
├── server/          # FastMCP class + core
│   ├── server.py    # Main FastMCP class
│   ├── auth/        # Enterprise auth providers
│   ├── middleware/  # Logging, caching, rate limiting
│   └── context.py   # Context injection
├── client/          # Client SDK
│   ├── client.py    # Client class
│   └── transports.py # STDIO, HTTP, SSE, in-memory
├── tools/           # Tool implementation
├── resources/       # Resources + templates
├── prompts/         # Prompt templates
└── experimental/    # OpenAPI generation
```

## Testing Pattern

```python
from fastmcp import FastMCP, Client

mcp = FastMCP("Test")

@mcp.tool
def add(a: int, b: int) -> int:
    return a + b

# Test with in-memory connection (no processes)
async def test_add():
    async with Client(mcp) as client:
        result = await client.call_tool("add", {"a": 2, "b": 3})
        assert result.content[0].text == "5"
```

## Deployment Options

1. **Local (Development)**
   ```bash
   fastmcp run server.py
   ```

2. **FastMCP Cloud (SaaS)**
   - Instant HTTPS endpoints
   - Built-in auth
   - Free for personal servers

3. **Self-Hosted (HTTP)**
   ```python
   mcp.run(transport="http", host="0.0.0.0", port=8000)
   ```

4. **Self-Hosted (SSE)**
   ```python
   mcp.run(transport="sse", host="0.0.0.0", port=8000)
   ```

## Enterprise Auth Providers

FastMCP has built-in support for:
- Google OAuth
- GitHub OAuth
- Microsoft Azure
- Auth0
- WorkOS SSO
- Descope
- JWT/Custom
- API Keys

Usage:
```python
from fastmcp.server.auth.providers.github import GitHubProvider

auth = GitHubProvider(client_id="...", client_secret="...")
mcp = FastMCP("Protected", auth=auth)
```

## Common Patterns

### Pattern 1: Tool with complex validation
```python
from typing import Annotated
from pydantic import Field

@mcp.tool
def process(
    items: Annotated[list[str], Field(description="Items to process", min_items=1)],
    batch_size: Annotated[int, Field(gt=0, le=100)] = 10
) -> dict:
    return {"processed": len(items)}
```

### Pattern 2: Async tool with context
```python
@mcp.tool
async def search_web(query: str, ctx: Context) -> str:
    await ctx.info(f"Searching for: {query}")
    # ... do work
    await ctx.report_progress(50)
    # ... more work
    return "results"
```

### Pattern 3: Resource with dynamic parameters
```python
@mcp.resource("database://{db_name}/tables/{table_name}")
def get_table_schema(db_name: str, table_name: str):
    return fetch_schema(db_name, table_name)
```

### Pattern 4: Server composition
```python
parent = FastMCP("Parent")
auth_server = FastMCP("Auth")
data_server = FastMCP("Data")

parent.mount(auth_server, name="auth")
parent.mount(data_server, name="data")
```

## Resources

- **Docs**: https://gofastmcp.com
- **GitHub**: https://github.com/jlowin/fastmcp
- **Discord**: https://discord.gg/uu8dJCgttd
- **PyPI**: https://pypi.org/project/fastmcp

## Summary

| Aspect | FastMCP |
|--------|---------|
| **Problem solved** | Simplifying MCP server/client development |
| **Primary use** | Building production MCP services |
| **Language** | Python 3.10+ |
| **Complexity** | Low (decorators + Python) |
| **Production ready** | Yes (v2.0) |
| **Enterprise ready** | Yes (auth, middleware, deployment) |
| **Best for** | Production MCP services with multiple clients |

FastMCP is to MCP what FastAPI is to REST: dramatically simpler, production-ready, and with all the enterprise features included.
