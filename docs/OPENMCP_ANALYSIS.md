# OpenMCP: Comprehensive Analysis

## 1. What is OpenMCP? What Problem Does it Solve?

OpenMCP is a **Model Context Protocol (MCP) server framework** that solves the problem of easily exposing external APIs and services as MCP tools to AI chat clients like Claude, Cursor, and others.

### Core Problem Solved:
- Converting any OpenAPI specification into MCP-compatible tools without manual integration code
- Composing multiple MCP servers into a single unified interface
- Managing authentication, configuration, and transport for multiple servers
- Reducing the friction of adding external capabilities to AI chat clients

### Key Insight:
Instead of building separate integrations for each API + each chat client combination, OpenMCP provides a **single standardized format** (openmcp.json) that works across all major chat clients.

---

## 2. Key Features and Capabilities

### 2.1 Core Capabilities

#### **OpenAPI-to-MCP Translation**
- Automatically converts OpenAPI specifications (v3.x, v2.x) into MCP tools
- Parses operations, parameters, request/response schemas
- Generates proper tool schemas and descriptions
- Supports tool filtering (expose only specific endpoints)

#### **Multi-Transport Support**
The framework supports 4 transport types:
1. **OpenAPI** - HTTP-based APIs converted to MCP tools
2. **SSE (Server-Sent Events)** - Streaming HTTP protocol
3. **Stdio** - Child process communication (stdio MCP servers)
4. **Streamable-HTTP** - Streaming HTTP variant

#### **Server Composition/Remixing**
- Combine multiple MCP servers into a single unified server
- Selectivity: expose only specific tools from each server
- Centralized configuration through `openmcp.json`

#### **Authentication & Configuration Management**
- Support for multiple auth schemes (API keys, OAuth, basic auth, etc.)
- Environment variable substitution
- Configuration inheritance and templating
- Per-server secret management

#### **Chat Client Integration**
- Auto-installation for Cursor, Claude, VS Code, etc.
- Automatic MCP config file generation and updates
- Install/uninstall commands
- One-command setup: `npx openmcp install <openapi-url> --client cursor`

#### **Tool Metadata & Annotations**
- Tool descriptions from OpenAPI
- Parameter schemas
- Output schemas with structured outputs support
- Tool annotations: readOnly, destructive, idempotent hints
- Tool title customization

#### **Management API**
- Manager class for programmatic server/client management
- Connect clients to servers
- Query available tools
- Call tools with configuration

---

## 3. API/Interface It Provides

### 3.1 CLI Commands

```bash
# Install OpenAPI as MCP tool
openmcp install <url-or-path> --client <cursor|claude|vscode>

# Run openmcp server
openmcp run --config <openmcp.json>
openmcp run --server <server-id> --secret <secret>

# Auth/Discovery
openmcp login
openmcp logout
openmcp whoami

# Upload custom servers
openmcp upload <config>

# Uninstall
openmcp uninstall <server-id>
```

### 3.2 Configuration Format (openmcp.json)

```jsonc
{
  "configs": {
    // Environment variables and secrets
    "server-name": {
      "API_KEY": "value or {{ENV_VAR}}"
    }
  },
  "servers": {
    // Server definitions
    "openapi-server": {
      "type": "openapi",
      "openapi": "https://api.example.com/openapi.json",
      "serverUrl": "https://api.example.com",
      "headers": { "User-Agent": "{{API_KEY}}" },
      "tools": ["tool1", "tool2"]  // Optional: allowlist specific tools
    },
    "stdio-server": {
      "type": "stdio",
      "command": "npx",
      "args": ["@modelcontextprotocol/server-postgres", "{{DB_URL}}"],
      "tools": ["query"]  // Tool filtering
    }
  }
}
```

### 3.3 Programmatic API (TypeScript/Node.js)

#### Manager API
```typescript
import { createMcpManager } from '@openmcp/manager';

const manager = createMcpManager({ id: 'my-manager' });

// Register a server
const server = manager.registerServer({
  id: 'linear',
  configSchema: z.object({ apiKey: z.string() }),
  capabilities: { tools: { createIssue: {...} } },
  transport: { type: 'sse', url: 'https://...' }
});

// Connect a client
const client = await manager.connectClient({
  id: 'user-1',
  servers: { linear: { apiKey: 'secret' } }
});

// Call tools
const result = await client.callTool({
  name: 'createIssue',
  input: { title: '...', description: '...' }
});
```

#### Server Implementation
```typescript
import { OpenMcpServer } from '@openmcp/server';
import { z } from 'zod';

const server = new OpenMcpServer({
  name: 'My Server',
  version: '1.0.0',
  tools: {
    greet: {
      description: 'Greet a user',
      parameters: z.object({ name: z.string() }),
      execute: async ({ name }) => `Hello, ${name}!`
    }
  }
});

// Connect to transport
await server.connect(transport);
```

#### OpenAPI Integration
```typescript
import { openApiToMcpServerOptions } from '@openmcp/openapi';

const serverOptions = await openApiToMcpServerOptions({
  openapi: 'https://api.example.com/openapi.json',
  serverUrl: 'https://api.example.com'
});

const server = new OpenMcpServer(serverOptions);
```

---

## 4. How It Relates to MCP (Model Context Protocol)

### 4.1 MCP Foundation
OpenMCP is built **on top of the official MCP SDK** (`@modelcontextprotocol/sdk`):
- Implements the MCP specification for server-client communication
- Extends the base MCP Server with convenience features
- Supports both MCP v1.0 request/response schemas

### 4.2 What OpenMCP Adds to MCP

| Aspect | MCP SDK | OpenMCP |
|--------|---------|---------|
| **Core Protocol** | Defines messages, tools, resources | ✓ Uses MCP |
| **Transport** | Abstract transport interface | Implements: OpenAPI, SSE, Stdio, HTTP |
| **Tool Definition** | Basic schema support | ✓ Plus: Zod + TS types, output schemas, annotations |
| **Tool Execution** | Manual handler registration | ✓ Automatic from OpenAPI specs |
| **Server Management** | Single server instance | Multiple servers with composition |
| **Configuration** | Programmatic only | ✓ Plus: JSON config files, env vars |
| **CLI** | None | ✓ Install, run, manage servers |
| **Client Integration** | None | ✓ Auto-integration with chat clients |

### 4.3 MCP Compatibility
- Uses official MCP SDK types and handlers
- Implements ListTools, CallTool, ListResources, ReadResource
- Supports structured outputs, tool annotations
- Works with any MCP-compatible client (Claude, Cursor, VS Code, etc.)

---

## 5. Installation and Usage Patterns

### 5.1 For End Users (Chat Client Users)

**Quick Start:**
```bash
# Add weather API to Cursor
npx openmcp install https://api.weather.gov/openapi.json --client cursor

# Prompts for configuration, creates openmcp.json, updates Cursor config
```

**Manual Setup:**
1. Create `openmcp.json` with server configurations
2. Run `openmcp run --config ./openmcp.json`
3. Configure chat client to use openmcp server

### 5.2 For Developers (TypeScript/Node.js)

**Installation:**
```bash
npm install @openmcp/server @openmcp/openapi
# or individual packages:
# @openmcp/manager - Server/client management
# @openmcp/openapi - OpenAPI-to-MCP conversion
# @openmcp/schemas - Config validation
# @openmcp/utils - Utilities (auto-trim, etc.)
# @openmcp/cli - CLI commands
```

**Pattern 1: Convert OpenAPI to MCP**
```typescript
import { openApiToMcpServerOptions } from '@openmcp/openapi';
import { OpenMcpServer } from '@openmcp/server';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const serverOptions = await openApiToMcpServerOptions({
  openapi: 'https://api.linear.app/graphql',  // Can be URL or file path
  serverUrl: 'https://api.linear.app'
});

const server = new OpenMcpServer(serverOptions);
const transport = new StdioServerTransport();
await server.connect(transport);
```

**Pattern 2: Build Custom MCP Server**
```typescript
import { OpenMcpServer } from '@openmcp/server';
import { z } from 'zod';

const server = new OpenMcpServer({
  name: 'My Tool Server',
  version: '1.0.0',
  tools: {
    fetchUser: {
      description: 'Fetch user by ID',
      parameters: z.object({ userId: z.string() }),
      output: z.object({ id: z.string(), name: z.string() }),
      execute: async ({ userId }) => {
        // Implementation
        return { id: userId, name: 'John' };
      }
    }
  },
  resources: [
    // Optional: expose resources (files, data)
  ]
});
```

**Pattern 3: Server Composition**
```typescript
// Using manager for multiple servers
const manager = createMcpManager();

// Register servers (from configs)
const servers = [
  { id: 'api1', config: {...} },
  { id: 'api2', config: {...} }
];

servers.forEach(s => manager.registerServer(s.config));

// One client talks to all
const client = await manager.connectClient({
  id: 'assistant',
  servers: { api1: {...}, api2: {...} }
});

const tools = await client.listTools(); // All tools from both servers
```

### 5.3 Configuration Patterns

**Pattern 1: Environment Variables**
```json
{
  "configs": {
    "github": {
      "GITHUB_TOKEN": ""  // Reads from env.GITHUB_TOKEN
    }
  }
}
```

**Pattern 2: Selective Tool Exposure**
```json
{
  "servers": {
    "database": {
      "type": "stdio",
      "command": "mcp-server-postgres",
      "tools": ["query", "execute"]  // Only expose safe tools
    }
  }
}
```

**Pattern 3: Multi-Environment**
```json
{
  "servers": {
    "api": {
      "type": "openapi",
      "openapi": "https://api.example.com/spec.json",
      "headers": { "Authorization": "Bearer {{API_TOKEN}}" }
    }
  }
}
```

---

## 6. Whether It Can Be Integrated with Airis Agent

### 6.1 Integration Points - YES, Multiple Options

#### **Option 1: Use OpenMCP as MCP Server Backend**
Airis Agent could wrap OpenAPI specifications using OpenMCP:

```typescript
// In superagent plugin or CLI command
import { openApiToMcpServerOptions } from '@openmcp/openapi';
import { OpenMcpServer } from '@openmcp/server';

// When user adds an API to superagent
const createApiTool = async (openapiUrl: string, config: any) => {
  const serverOptions = await openApiToMcpServerOptions({
    openapi: openapiUrl,
    serverUrl: config.baseUrl
  });
  
  const server = new OpenMcpServer({
    ...serverOptions,
    // Add superagent-specific metadata
    onInitialize: (clientInfo) => {
      console.log(`Connected to ${clientInfo.name}`);
    }
  });
  
  return server;
};
```

#### **Option 2: Server Composition for Multi-API Agents**
Airis Agent could use OpenMCP Manager for agent orchestration:

```typescript
import { createMcpManager } from '@openmcp/manager';

// Create manager for agent
const agentManager = createMcpManager({ id: `agent-${agentId}` });

// Register all APIs the agent needs
for (const api of agent.connectedApis) {
  agentManager.registerServer({
    id: api.id,
    configSchema: z.object({ apiKey: z.string() }),
    createServer: () => openApiToMcpServer(api)
  });
}

// Connect agent as client
const agentClient = await agentManager.connectClient({
  id: agentId,
  servers: { /* all connected APIs */ }
});

// Now agent can call any tool from any connected API
await agentClient.callTool({ server: 'linear', name: 'createIssue', ... });
```

#### **Option 3: CLI Skill for Easy API Integration**
Add an OpenMCP-based skill to superagent CLI:

```bash
# User-friendly command
superagent add-api https://api.github.com/openapi.json \
  --name github \
  --token $GITHUB_TOKEN

# Under the hood: uses openmcp to convert, creates tool definitions
```

#### **Option 4: Pytest Plugin Integration**
Test APIs using OpenMCP + Airis Agent's PM Agent:

```python
# In pytest plugin
@pytest.mark.confidence_check
def test_external_api_integration(confidence_checker):
    """Confidence check before converting OpenAPI to tools"""
    context = {
        "openapi_url": "https://api.example.com/spec.json",
        "has_official_docs": True,
        "transport_type": "openapi",
        "requires_auth": True
    }
    assert confidence_checker.assess(context) >= 0.7
```

### 6.2 Key Integration Benefits

1. **Reduce Tool Definition Code**
   - No manual tool definitions for OpenAPI-based APIs
   - One JSON file replaces hundreds of lines

2. **Standardized API Integration**
   - Consistent pattern: OpenAPI → MCP tools
   - Same approach works for all REST APIs

3. **Easy Composability**
   - Agents can be created with multiple API tools
   - Manager handles multi-server orchestration

4. **Flexible Configuration**
   - YAML/JSON config supports environment variables
   - Easy to swap APIs without code changes

5. **Client Agnostic**
   - OpenMCP works with any MCP client
   - Airis Agent could offer to users via MCP transport

### 6.3 Potential Challenges

1. **OpenAPI Quality Variability**
   - Some APIs have incomplete/incorrect specs
   - May need OpenAPI validation/fixing hooks

2. **Type Safety**
   - Dynamically generated from specs
   - Consider Airis Agent's type-first approach

3. **Error Handling**
   - HTTP errors from external APIs
   - Need retry/fallback strategies

4. **Performance**
   - OpenAPI parsing/dereferencing overhead
   - Consider caching converted servers

### 6.4 Integration Recommendation

**RECOMMENDED: Hybrid Approach**

1. **Leverage OpenMCP for API-First Tools**
   - Use `openApiToMcpServerOptions` for REST APIs
   - Build OpenMCP servers for databases, GraphQL endpoints
   
2. **Custom Airis Agent Tools for Complex Logic**
   - Keep error handling, retry logic in Python/TypeScript
   - Use OpenMCP tools as building blocks

3. **Add CLI Command for Easy Integration**
   ```bash
   superagent tool add <openapi-url> [--config <openmcp.json>]
   ```

4. **Use Manager API for Programmatic Composition**
   - Build agents with multiple API tools
   - Expose unified tool interface to agents

---

## 7. Architecture Overview

### 7.1 Package Structure

```
openmcp/
├── packages/
│   ├── cli/          # CLI tool (install, run, manage)
│   ├── server/       # OpenMcpServer class + core
│   ├── manager/      # Manager for multi-server composition
│   ├── openapi/      # OpenAPI-to-MCP conversion
│   ├── schemas/      # Config validation schemas (Zod)
│   └── utils/        # Helpers (auto-trim results, etc.)
└── apps/
    └── web/          # Web dashboard (optional)
```

### 7.2 Data Flow

```
OpenAPI Spec
    ↓
[openApiToMcpServerOptions]
    ↓
Tool Definitions (JSON Schema)
    ↓
[OpenMcpServer]
    ↓
MCP Protocol Messages
    ↓
[Transport: Stdio/SSE/HTTP]
    ↓
Chat Client (Claude/Cursor)
```

### 7.3 Configuration Flow

```
openmcp.json
    ↓
[Config Validation: @openmcp/schemas]
    ↓
[Manager registers servers]
    ↓
[Client connects to servers]
    ↓
Tools available in chat client
```

---

## 8. Comparison Matrix: Airis Agent vs OpenMCP

| Dimension | Airis Agent | OpenMCP |
|-----------|-----------|---------|
| **Purpose** | Agent framework + orchestration | MCP server framework |
| **Core Use** | Build autonomous agents | Expose APIs as MCP tools |
| **Config** | Python + JSON | JSON (openmcp.json) |
| **Multi-Server** | Via Python agent logic | Via Manager + composition |
| **OpenAPI Support** | Limited | First-class (auto-conversion) |
| **Chat Client Support** | Claude via MCP | All MCP-compatible clients |
| **Authentication** | OAuth provider pattern | Header/param substitution |
| **Community** | Anthropic/Enterprise | Datanaut OSS community |

---

## 9. Quick Reference: Key Files

| Path | Purpose |
|------|---------|
| `/packages/server/src/server.ts` | Core OpenMcpServer implementation |
| `/packages/manager/src/manager.ts` | Manager for multi-server composition |
| `/packages/openapi/src/openapi-to-mcp.ts` | OpenAPI → MCP conversion logic |
| `/packages/cli/src/commands/install` | Install command implementation |
| `/packages/schemas/src/mcp.ts` | Configuration validation schemas |

---

## 10. Integration Checklist for Airis Agent

- [ ] Evaluate OpenAPI specification coverage needed
- [ ] Design tool auto-generation strategy
- [ ] Decide: use OpenMCP server vs integrate code directly
- [ ] Handle authentication/secret management
- [ ] Build validation/testing for generated tools
- [ ] Create CLI command for API integration
- [ ] Document OpenAPI requirements for users
- [ ] Consider OpenAPI v3.1 support
- [ ] Plan error handling strategy
- [ ] Design caching strategy for spec parsing

