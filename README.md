# Airis Agent

> **Autonomous AI workflow orchestrator for Claude Code**

Airis Agent is the intelligence layer of the Airis Suite, providing autonomous workflow orchestration with confidence gating, deep research, repository indexing, and self-review capabilities for AI-enhanced development.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-blue)](https://claude.com/code)

---

## What is Airis Agent?

Airis Agent is an autonomous workflow orchestrator that enhances Claude Code with:

- **Pre-implementation Confidence Checks** - Validates readiness before coding (≥90% confidence required)
- **Deep Research** - Parallel web search with evidence-based synthesis using Tavily/Context7
- **Repository Indexing** - 94% token reduction through intelligent codebase analysis
- **Self-Review** - Post-implementation validation with evidence requirements

**Philosophy**: Prevent wrong-direction work through confidence gating, not post-hoc fixes.

---

## Installation

### From GitHub Marketplace (Recommended)

```bash
# In Claude Code, run:
/plugin marketplace add agiletec-inc/airis-agent
/plugin install airis-agent@agiletec-inc
```

### Local Development

```bash
# Clone the repository
git clone https://github.com/agiletec-inc/airis-agent.git
cd airis-agent

# Add local marketplace
/plugin marketplace add /path/to/airis-agent

# Install plugin
/plugin install airis-agent@agiletec
```

### Verification

```bash
# Check installed plugins
/plugin list

# You should see: airis-agent@agiletec-inc (enabled)
```

---

## Quick Start

### Automatic Session Initialization

Airis Agent automatically activates at session start via `SessionStart` hook:

```
📊 Git: clean
✅ CLAUDE.md: 115 lines (適切な範囲)
📦 PROJECT_INDEX.md: 3 days old (fresh)
📂 Context available: docs/memory/

🛠️  Core Services Available:
  ✅ Confidence Check (pre-implementation validation)
  ✅ Deep Research (web/MCP integration)
  ✅ Repository Index (token-efficient exploration)

Airis Agent ready — awaiting task assignment.
```

### Basic Workflow

```bash
# 1. Start a task
User: "Add user authentication to the API"

# 2. Airis Agent orchestrates automatically:
#    - Runs confidence check
#    - Triggers deep research if needed
#    - Implements with evidence
#    - Self-reviews results

# 3. Manual commands (optional)
/airis:research "Best practices for JWT authentication 2025"
/airis:index-repo
```

---

## Available Components

### Commands

| Command | Description |
|---------|-------------|
| `/airis:research` | Deep research with parallel web search |
| `/airis:index-repo` | Generate PROJECT_INDEX.md (94% token reduction) |

### Agents

| Agent | Description | Invocation |
|-------|-------------|------------|
| `deep-research` | External knowledge gathering specialist | `@deep-research` via Task tool |
| `repo-index` | Codebase briefing assistant | `@repo-index` via Task tool |
| `self-review` | Post-implementation validation | `@self-review` via Task tool |

### Skills

| Skill | Description | Activation |
|-------|-------------|------------|
| `confidence-check` | Pre-implementation confidence assessment (≥90% required) | Automatic (Claude decides) |

### Hooks

- **SessionStart**: Automatic initialization with Git status, CLAUDE.md optimization check, PROJECT_INDEX.md freshness check, and context restoration

---

## Session Initialization Features

Airis Agent's `SessionStart` hook automatically checks:

### 1. CLAUDE.md Optimization
```
⚠️  CLAUDE.md: 315 lines (推奨: 100-200)
   💡 Optimize with: /init
      (Re-analyzes codebase and refreshes CLAUDE.md)
```

### 2. PROJECT_INDEX.md Freshness
```
⚠️  PROJECT_INDEX.md: 12 days old (stale)
   💡 Regenerate with: /airis:index-repo
```

### 3. Context Restoration
```
📂 Context available: docs/memory/
📋 Next actions:
   [Content from next_actions.md]
🕐 Last session: 2025-11-13
```

---

## Configuration

### Team-Wide Installation

Add to your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "agiletec": {
      "source": {
        "source": "github",
        "repo": "agiletec-inc/airis-agent"
      }
    }
  },
  "enabledPlugins": ["airis-agent@agiletec"]
}
```

Team members will automatically receive Airis Agent when they trust the repository.

### Disable Auto-Activation

If you prefer manual activation, modify `hooks/hooks.json` in the plugin:

```json
{
  "hooks": {
    "SessionStart": []
  }
}
```

---

## Development

### Prerequisites

- Python 3.10+
- UV (Python package manager)
- Node.js 16+ (for NPM wrapper)

### Setup

```bash
# Install in editable mode
make install

# Or manually:
uv pip install -e ".[dev]"

# Verify installation
make verify
airis-agent doctor
```

### Building the Plugin

```bash
# Build plugin artifacts
make build-plugin

# Output: dist/plugins/airis-agent/
```

### Testing

```bash
# Run all tests
make test

# Run specific tests
uv run pytest tests/airis_agent/ -v

# With coverage
make test-coverage
```

### Project Structure

```
airis-agent/
├── .claude-plugin/
│   └── marketplace.json       # Plugin marketplace manifest
├── plugins/airis-agent/
│   ├── agents/                # Agent definitions
│   ├── commands/              # Slash commands
│   ├── skills/                # Skills (auto-invoked)
│   ├── hooks/                 # Event handlers
│   ├── scripts/               # Utility scripts
│   └── manifest/              # Plugin metadata
├── src/airis_agent/
│   ├── api/                   # Public API (confidence, research, index)
│   ├── cli/                   # CLI commands
│   ├── execution/             # Parallel execution, reflexion
│   └── pm_agent/              # PM Agent patterns
├── tests/airis_agent/         # Test suite
└── dist/plugins/airis-agent/  # Built plugin (generated)
```

---

## Python API

Airis Agent provides a Python API for programmatic access:

```python
from airis_agent.api import confidence, deep_research, repo_index

# Confidence check
result = confidence.assess({
    "task": "Implement user authentication",
    "has_official_docs": True
})

if result["confidence"] >= 0.90:
    # Proceed with implementation
    pass
else:
    # Gather more information
    research = deep_research.execute({
        "query": "JWT authentication best practices 2025",
        "depth": "standard"
    })
```

---

## Why Airis Agent Exists

**Problem**: LLMs often implement solutions confidently even when lacking complete information, leading to wasted tokens and wrong-direction work.

**Solution**: Confidence-first workflow with evidence requirements:

1. **Pre-implementation**: Assess confidence (≥90% required)
2. **Research**: Gather authoritative information if needed
3. **Implementation**: Execute with validated approach
4. **Post-review**: Verify with evidence (no speculation)

**ROI**: Spending 100-200 tokens on confidence checks saves 5,000-50,000 tokens on wrong implementations.

---

## Airis Suite Integration

Airis Agent is part of the Airis Suite:

- **Airis Workspace** - Docker-based development OS
- **Airis Code** - AI-enhanced coding environment
- **Airis Agent** - Autonomous workflow orchestrator (this project)
- **Airis Voice** - AI phone automation
- **Airis MCP** - Model Context Protocol tools
- **MindBase** - Cross-session memory database

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Support

- **Issues**: https://github.com/agiletec-inc/airis-agent/issues
- **Documentation**: See `docs/` directory
- **Homepage**: https://github.com/agiletec-inc/airis-agent

---

**Built with ❤️ by Agiletec Inc.**
