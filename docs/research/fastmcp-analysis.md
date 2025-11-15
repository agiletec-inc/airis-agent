# FastMCP Repository Analysis

## Executive Summary

FastMCP is the production-ready, actively maintained Python framework for building Model Context Protocol (MCP) servers and clients. It represents the standard for Python MCP development after FastMCP 1.0 was incorporated into the official MCP SDK in 2024. FastMCP 2.0 extends far beyond basic protocol implementation with enterprise authentication, deployment tools, testing utilities, and comprehensive client libraries.

**Key Facts:**
- Maintained by Prefect (https://www.prefect.io/)
- 511 lines of comprehensive README
- Python 3.10+ with full type annotations
- Apache 2.0 license
- Published at https://gofastmcp.com
- Trending on Trendshift

---

## What is FastMCP?

FastMCP solves the complexity problem of MCP server/client development. While the official MCP SDK provides core protocol functionality, FastMCP provides a high-level, Pythonic interface that handles all protocol details, enabling developers to focus on business logic.

**Problem it solves:**
1. **Boilerplate burden**: Decorating a function is all that's needed for most use cases
2. **Protocol complexity**: Handles MCP protocol details automatically
3. **Production gaps**: Enterprise auth, testing, deployment, composition patterns
4. **Type safety**: Full Pydantic integration with automatic schema generation

**Official MCP (SDK) vs FastMCP 2.0:**
- Official SDK: Core protocol implementation
- FastMCP 2.0: Production-ready framework with advanced patterns (proxy, composition, OpenAPI generation, enterprise auth)

---

## Core Architecture

### 1. Server Implementation (FastMCP)

Location: `src/fastmcp/server/server.py`

```python
from fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool
def my_function(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    mcp.run()  # Default: STDIO transport
```

**Key Components:**
- **FastMCP class**: Central server object managing tools, resources, prompts
- **Tool Manager**: Handles tool registration and schema generation
- **Resource Manager**: Manages read-only data sources with templating
- **Prompt Manager**: Manages reusable message templates
- **Middleware system**: For logging, caching, rate limiting, error handling
- **Authentication**: Enterprise auth providers (Google, GitHub, Azure, WorkOS, etc.)

### 2. Tools (RPC-like Functions)

Location: `src/fastmcp/tools/tool.py`

Tools allow LLMs to perform actions by executing Python functions.

```python
@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers."""
    return a * b

# Complex inputs
@mcp.tool
def process(
    items: Annotated[list[str], Field(description="Items to process")],
    mode: Literal["fast", "accurate"] = "fast"
) -> dict:
    return {"processed": len(items), "mode": mode}
```

**Features:**
- Sync or async functions
- Automatic JSON schema generation from type hints
- Media support: text, JSON, images, audio via helper classes
- Custom serializers
- Result wrapping with metadata

### 3. Resources & Templates

Location: `src/fastmcp/resources/`

Resources expose read-only data sources (like GET requests).

```python
# Static resource
@mcp.resource("config://version")
def get_version():
    return "2.0.1"

# Dynamic template with parameters
@mcp.resource("users://{user_id}/profile")
def get_profile(user_id: int):
    return {"name": f"User {user_id}", "status": "active"}
```

### 4. Prompts

Location: `src/fastmcp/prompts/`

Reusable message templates for LLM interactions.

```python
@mcp.prompt
def summarize_request(text: str) -> str:
    """Generate a prompt asking for a summary."""
    return f"Please summarize:\n\n{text}"
```

### 5. Context

Location: `src/fastmcp/server/context.py`

Access MCP session capabilities within tools/resources/prompts:

```python
from fastmcp import Context

@mcp.tool
async def process_data(uri: str, ctx: Context):
    await ctx.info(f"Processing {uri}...")
    data = await ctx.read_resource(uri)
    summary = await ctx.sample(f"Summarize: {data.content[:500]}")
    return summary.text
```

**Context Methods:**
- Logging: `ctx.info()`, `ctx.error()`, etc.
- LLM Sampling: `ctx.sample()` - request completions from client's LLM
- Resource Access: `ctx.read_resource()` - access other resources
- Progress: `ctx.report_progress()` - report progress to client

### 6. Client Implementation

Location: `src/fastmcp/client/client.py`

Programmatic interaction with any MCP server.

```python
from fastmcp import Client

# Connect via stdio to a local script
async with Client("my_server.py") as client:
    tools = await client.list_tools()
    result = await client.call_tool("add", {"a": 5, "b": 3})

# In-memory testing (no network overhead)
async with Client(mcp) as client:
    result = await client.call_tool("my_tool", {...})

# Multiple servers via MCP config
config = {
    "mcpServers": {
        "weather": {"url": "https://weather-api.example.com/mcp"},
        "assistant": {"command": "python", "args": ["./assistant.py"]}
    }
}
client = Client(config)
```

**Transport Support:**
- STDIO (default, local tools)
- Streamable HTTP (web deployments)
- SSE (Server-Sent Events)
- In-Memory (direct FastMCP instances)

---

## Key Features

### 1. Enterprise Authentication (Zero Configuration)

Location: `src/fastmcp/server/auth/providers/`

**Supported Providers:**
- Google OAuth
- GitHub OAuth
- Microsoft Azure
- Auth0
- WorkOS SSO
- Descope
- JWT/Custom
- API Keys

```python
from fastmcp.server.auth.providers.google import GoogleProvider

auth = GoogleProvider(
    client_id="...",
    client_secret="...",
    base_url="https://myserver.com"
)
mcp = FastMCP("Protected Server", auth=auth)
```

Client connection:
```python
async with Client("https://protected-server.com/mcp", auth="oauth") as client:
    result = await client.call_tool("protected_tool")
```

**Why it matters:**
- Production-ready with persistent storage and token refresh
- Zero-config OAuth: pass `auth="oauth"`
- Enterprise integration: SSO, Active Directory, Auth0 tenants
- Unique OIDC support with Dynamic Client Registration (DCR)

### 2. Middleware System

Location: `src/fastmcp/server/middleware/`

**Built-in Middleware:**
- **Error Handling**: Automatic exception mapping with optional detail masking
- **Logging**: Request/response logging with configurable levels
- **Caching**: Tool result caching with TTL
- **Rate Limiting**: Per-tool rate limiting
- **Tool Injection**: Dynamically inject dependencies into tools
- **Timing**: Measure execution time

```python
from fastmcp.server.middleware import LoggingMiddleware, RateLimitMiddleware

mcp = FastMCP(
    "MyServer",
    middleware=[
        LoggingMiddleware(level="INFO"),
        RateLimitMiddleware(max_calls=100, window_seconds=60)
    ]
)
```

### 3. Advanced Patterns

#### Proxy Servers

Location: `src/fastmcp/server/proxy.py`

Create a FastMCP server that acts as intermediary for another MCP server:
- Bridge transports (e.g., remote SSE to local stdio)
- Add logic layer to servers you don't control
- Caching, authentication, filtering

```python
mcp = FastMCP.as_proxy("http://remote-server.com/mcp")
```

#### Server Composition

Location: (Mounted servers concept)

Mount multiple FastMCP instances onto a parent server:
```python
parent = FastMCP("Parent")
child1 = FastMCP("Child1")
child2 = FastMCP("Child2")

parent.mount(child1, name="child1")
parent.mount(child2, name="child2")
```

#### OpenAPI Integration

Location: `src/fastmcp/experimental/server/openapi/`

Automatically generate MCP servers from OpenAPI specs:
```python
mcp = FastMCP.from_openapi("https://api.example.com/openapi.json")
```

### 4. Deployment Options

**Development:**
```bash
fastmcp run server.py
```

**FastMCP Cloud** (Official SaaS):
- Remote MCP with instant HTTPS endpoints
- Built-in authentication
- Zero configuration
- Free for personal servers

**Self-Hosted:**
```python
mcp.run(transport="http", host="0.0.0.0", port=8000)
mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

---

## API/Interface Overview

### Server Decorators

```python
@mcp.tool                           # RPC-like tools
@mcp.resource("uri://path")         # Read-only resources
@mcp.prompt                         # Message templates
```

### Tool Signature Flexibility

```python
@mcp.tool
async def tool_name(
    param1: str,
    param2: int = 10,
    param3: Annotated[list[str], Field(description="...")] = None,
    ctx: Context = None  # Optional context injection
) -> ToolResult | dict | str | bytes:
    pass
```

### Client API

```python
async with Client(...) as client:
    # Discovery
    tools = await client.list_tools()
    resources = await client.list_resources()
    prompts = await client.list_prompts()
    
    # Execution
    result = await client.call_tool(name, args)
    content = await client.read_resource(uri)
    prompt_content = await client.get_prompt(name)
    
    # Advanced
    roots = await client.list_roots()
    await client.set_sampling_handler(handler)
```

### Server Configuration

```python
mcp = FastMCP(
    name="MyServer",
    instructions="How to use this server",
    version="1.0.0",
    auth=AuthProvider(),
    middleware=[...],
    lifespan=lifespan_context_manager,
    tool_transformations={...},
    tool_serializer=custom_serializer,
    on_duplicate_tools="warn" | "error" | "replace" | "ignore"
)
```

---

## Dependencies & Technology Stack

**Core Dependencies:**
- `mcp>=1.19.0,<2.0.0` - Official MCP SDK (provides protocol)
- `pydantic[email]>=2.11.7` - Schema validation and generation
- `httpx>=0.28.1` - HTTP client
- `uvicorn>=0.35` - ASGI server
- `authlib>=1.6.5` - OAuth/OIDC support
- `cyclopts>=4.0.0` - CLI framework
- `py-key-value-aio` - Async key-value storage

**Optional:**
- `openai>=1.102.0` - For OpenAI integration (sampling)

**Development:**
- `pytest>=8.3.3` - Testing
- `pytest-asyncio>=1.2.0` - Async test support
- `ruff>=0.12.8` - Linting and formatting
- `prek>=0.2.12` - Pre-commit hooks (format, lint, type-check)

---

## Comparison: FastMCP vs Official MCP SDK vs openmcp

### FastMCP vs Official MCP SDK

| Feature | FastMCP 2.0 | Official SDK |
|---------|------------|--------------|
| **Basics** | ✓ | ✓ |
| **High-level API** | ✓ Pythonic decorators | Manual protocol handling |
| **Enterprise Auth** | ✓ 8+ providers | ✗ |
| **Middleware** | ✓ Built-in | ✗ |
| **Server Composition** | ✓ Mount/proxy | ✗ |
| **OpenAPI Generation** | ✓ | ✗ |
| **Client Libraries** | ✓ Full SDK | Basic |
| **Testing Utilities** | ✓ In-memory transport | ✗ |
| **Deployment Tools** | ✓ FastMCP Cloud + self-hosted | ✗ |
| **Production Ready** | ✓ Mature | Core only |

**History:** FastMCP 1.0 was incorporated into official SDK in 2024. FastMCP 2.0 is the continuation with extended features.

### FastMCP vs openmcp

| Aspect | FastMCP | openmcp |
|--------|---------|---------|
| **Status** | Actively maintained, production (v2+) | Alternative/less established |
| **Community** | Large (trending on Trendshift) | Smaller |
| **Auth** | Comprehensive enterprise | Limited |
| **Documentation** | Extensive (gofastmcp.com) | Variable |
| **Enterprise Features** | Full suite | Limited |

---

## Installation & Usage Patterns

### Installation

```bash
# With uv (recommended)
uv pip install fastmcp

# Standard pip
pip install fastmcp

# From source
git clone https://github.com/jlowin/fastmcp.git
cd fastmcp
uv sync
```

### Running Servers

```bash
# CLI command
fastmcp run server.py

# Or directly
python server.py

# In Python
if __name__ == "__main__":
    mcp.run()  # Uses STDIO by default
```

### Testing Pattern

```python
from fastmcp import FastMCP, Client

mcp = FastMCP("TestServer")

@mcp.tool
def add(a: int, b: int) -> int:
    return a + b

async def test_add():
    async with Client(mcp) as client:  # In-memory connection
        result = await client.call_tool("add", {"a": 2, "b": 3})
        assert result.content[0].text == "5"
```

### Example: Memory System with Vector Embeddings

Location: `examples/memory.py`

Demonstrates:
- PostgreSQL integration with pgvector
- LLM sampling via context
- Async operations
- Complex data structures

---

## Integration Potential with Airis Agent

### 1. **MCP Gateway for Airis Agent Tools**

FastMCP could provide an MCP wrapper layer for Airis Agent's PM Agent patterns:

```python
# Expose confidence checker as MCP server
mcp = FastMCP("Airis Agent PM Agent")

@mcp.tool
async def evaluate_confidence(task: str, context: dict) -> dict:
    """Pre-implementation confidence assessment"""
    from airis_agent.api import evaluate_confidence
    result = await evaluate_confidence(task, context)
    return {
        "score": result.score,
        "action": result.action,
        "checklist": result.checklist
    }

@mcp.tool
async def generate_repo_index(repo_path: str) -> str:
    """Generate repository index"""
    from airis_agent.api import generate_repo_index
    index = await generate_repo_index(repo_path)
    return index.content

@mcp.resource("airis-agent://reflexion/{error_id}")
async def get_error_pattern(error_id: str):
    """Access learned error patterns"""
    from airis_agent.airis_agent import reflexion
    return await reflexion.get_pattern(error_id)
```

**Benefits:**
- Makes Airis Agent accessible to any MCP client (Claude, Cursor, etc.)
- Automatic schema generation from Airis Agent APIs
- Authentication built-in
- No need to maintain separate integrations

### 2. **Parallel Execution via FastMCP Tools**

Airis Agent's parallel execution could be exposed as distributed tools:

```python
@mcp.tool
async def parallel_execute(
    waves: Annotated[list[dict], Field(description="Execution waves")]
) -> dict:
    """Execute tasks in parallel waves with dependency management"""
    from airis_agent.execution import parallel
    return await parallel.execute_waves(waves)
```

### 3. **Authentication & Deployment**

FastMCP's enterprise auth and deployment tools complement Airis Agent:
- Protect Airis Agent PM Agent endpoints with OAuth
- Deploy to FastMCP Cloud or self-hosted infrastructure
- Automatic credential management

### 4. **Resource-Based Research Integration**

Deep Research as MCP resources:

```python
@mcp.resource("research://tavily/search")
async def web_search(query: str):
    """Search the web using Tavily"""
    from airis_agent.api import deep_research
    return await deep_research.search_web(query)

@mcp.resource("research://docs/context7")
async def fetch_official_docs(query: str):
    """Fetch official documentation via Context7"""
    from airis_agent.api import deep_research
    return await deep_research.fetch_docs(query)
```

### 5. **Middleware for PM Patterns**

Use FastMCP middleware to inject Airis Agent patterns:

```python
class ConfidenceCheckMiddleware(Middleware):
    async def process_request(self, request, call_next):
        # Run confidence check before tool execution
        confidence = await evaluate_confidence(request.tool_name)
        if confidence.score < 0.7:
            return {"error": "Confidence too low", "action": confidence.action}
        return await call_next(request)

mcp = FastMCP("PM Agent", middleware=[ConfidenceCheckMiddleware()])
```

### 6. **Testing Integration**

FastMCP's in-memory client could test Airis Agent plugins:

```python
from airis_agent.integration.fastmcp import create_airis_agent_mcp

mcp = create_airis_agent_mcp()

async def test_pm_agent():
    async with Client(mcp) as client:
        result = await client.call_tool("evaluate_confidence", {
            "task": "Implement authentication",
            "has_docs": True
        })
        assert result.content[0].structured_content["score"] > 0.7
```

---

## Key Differences from Airis Agent

| Aspect | FastMCP | Airis Agent |
|--------|---------|-----------|
| **Purpose** | MCP framework for building servers/clients | PM Agent patterns for LLM development |
| **Scope** | Protocol implementation + production patterns | Confidence, parallelization, reflexion |
| **API** | Decorators (tools, resources, prompts) | Python APIs for checkers and validators |
| **Deployment** | HTTP, STDIO, SSE, FastMCP Cloud | Pytest plugin + CLI |
| **Auth** | Enterprise auth providers | Not primary focus |
| **Use case** | Building production MCP services | Enhancing LLM development workflows |

---

## Documentation & Resources

- **Official Docs**: https://gofastmcp.com
- **LLM-Friendly Docs**: 
  - Sitemap: https://gofastmcp.com/llms.txt
  - Full docs: https://gofastmcp.com/llms-full.txt
- **GitHub**: https://github.com/jlowin/fastmcp
- **Discord**: https://discord.gg/uu8dJCgttd
- **PyPI**: https://pypi.org/project/fastmcp

---

## Development Guidelines for FastMCP

(From AGENTS.md)

**Required Workflow:**
```bash
uv sync                      # Install dependencies
uv run prek run --all-files  # Ruff + Prettier + ty (linting/formatting/typing)
uv run pytest               # Full test suite
```

**Key Rules:**
- Python 3.10+ with full type annotations
- Use `inline-snapshot` for testing complex data
- Always use in-memory transport for testing
- Full test coverage required for new features
- Prek hooks auto-run on commits

---

## Summary: Integration Opportunities

FastMCP provides three main integration points with Airis Agent:

1. **MCP Gateway Layer**: Wrap Airis Agent APIs as MCP server with automatic schema generation
2. **Middleware Integration**: Use FastMCP middleware for confidence checks and PM patterns
3. **Testing Framework**: Leverage in-memory client for testing Airis Agent patterns
4. **Deployment**: Package Airis Agent as FastMCP server for cloud/self-hosted deployment

The integration is natural because:
- Both are production-focused frameworks
- FastMCP handles protocol; Airis Agent handles LLM patterns
- No overlap in functionality
- Complementary deployment/auth/testing capabilities
