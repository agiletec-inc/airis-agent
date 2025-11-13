# Airis Agent

AI-enhanced development framework providing confidence gating, parallel execution, and reflexion patterns for LLM-powered development workflows.

> **Host-agnostic orchestration runtime**: Python modules expose typed APIs so MCP gateways, CLIs, and IDEs (Claude Code, Cursor, etc.) can share workflow logic without duplicating implementations.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Why Airis Agent Exists

**ABI-first design**: Python modules under `src/superagent/api/` provide a reusable Application Binary Interface. This means:

- **Single source of truth**: Runtime logic (confidence gate, parallel executor, reflexion/self-check, repo indexer) lives in one package
- **No drift**: Plugin artifacts are generated from source templates, preventing inconsistencies
- **Host-agnostic**: Works with Claude Code, Codex CLI, Gemini CLI, Cursor, or any tool that can call Python APIs
- **MCP-ready**: Can be exposed via MCP gateway for LLM access

## Features

### 🎯 Confidence Gate
Pre-implementation confidence assessment that prevents wrong-direction work:
- Returns score (0.0-1.0), action (proceed/alternatives/ask), and checklist
- ROI: Spend 100-200 tokens to save 5,000-50,000 tokens
- **25-250x token savings** by catching issues before implementation

### 🔄 Parallel Execution
Wave-based dependency planner with automatic parallelization:
- **3.5x faster** than sequential execution
- Automatic dependency analysis
- Example: `[Read files in parallel] → Analyze → [Edit files in parallel]`

### 🧠 Reflexion Pattern
Error learning and prevention across sessions:
- Records failure signatures
- Cross-session pattern matching
- Prevents repeating the same mistakes

### 📦 Repository Indexing
Generates structured codebase summaries:
- Produces `PROJECT_INDEX.{md,json}` with codebase structure
- **94% token reduction** for context
- Optional on-disk output

### 🔍 Deep Research
Multi-step research planning with integrated tools:
- Creates wave/queries plan for complex research
- Integrates with Tavily (web search) and Context7 (official docs)
- Returns findings, sources, and confidence scores

## Quick Start

### Installation

#### Option 1: Claude Code Plugin (Recommended for Claude Code users)

Install directly from the GitHub repository marketplace:

```bash
# In Claude Code, run:
/plugin marketplace add kazuki/superagent
/plugin install superagent
```

Or add to your project's `.claude/settings.json`:

```json
{
  "marketplaces": ["kazuki/superagent"],
  "enabledPlugins": ["superagent"]
}
```

The plugin provides:
- `/agent` - Session orchestrator with confidence checks
- `/research` - Deep research with parallel web search
- `/index-repo` - Repository indexing (94% token reduction)
- `@confidence-check` skill - Pre-implementation validation
- Auto-activation via SessionStart hook

#### Option 2: Python Package (For API/CLI usage)

```bash
# Clone the repository
git clone https://github.com/agiletec-inc/airis-agent.git
cd superagent

# Install with UV (recommended)
make install
# or: uv pip install -e ".[dev]"

# Verify installation
make verify
uv run superagent doctor
```

### Basic Usage

#### As a Python API

```python
from superagent.api import evaluate_confidence, generate_repo_index

# Confidence gate
result = evaluate_confidence({
    "task": "Implement user authentication",
    "has_official_docs": True,
    "complexity": "medium"
})
print(f"Confidence: {result.score}, Action: {result.action}")

# Repository indexing
index = generate_repo_index("/path/to/repo", output_format="markdown")
print(index.content)
```

#### As a Pytest Plugin

The pytest plugin is auto-loaded after installation:

```python
import pytest

@pytest.mark.confidence_check
def test_feature(confidence_checker):
    """Pre-execution confidence check"""
    context = {"test_name": "test_feature", "has_official_docs": True}
    assert confidence_checker.assess(context) >= 0.7

@pytest.mark.reflexion
def test_error_learning(reflexion_pattern):
    """Records failures for future prevention"""
    # Test implementation...
    pass
```

#### As a CLI

```bash
# Check installation health
uv run superagent doctor

# Show version
uv run superagent version

# Install a skill to Claude Code
uv run superagent install-skill confidence-check
```

## Project Structure

```
superagent/
├── src/superagent/
│   ├── api/                 # ABI endpoints (confidence, repo_index, deep_research)
│   ├── cli/                 # CLI commands (doctor, version, install-skill)
│   ├── execution/           # Parallel executor, reflection, self-correction
│   ├── pm_agent/            # Confidence checker, self-check protocol, reflexion
│   ├── pytest_plugin.py     # Auto-loaded pytest integration
│   └── skills/              # TypeScript skills bundled with package
├── plugins/superagent/      # Plugin source (manifest templates, tests)
│   ├── manifest/            # Metadata and manifest templates
│   └── tests/               # Plugin smoke tests
├── dist/plugins/superagent/ # Built plugin artifacts (via make build-plugin)
├── tests/                   # Python test suite
├── docs/                    # Documentation
├── scripts/                 # Build/publish helpers
└── Makefile                 # Development commands
```

## Development Workflow

### Essential Commands

```bash
# Setup
make install          # Install in editable mode with dev dependencies
make verify           # Verify installation

# Testing
make test             # Run full test suite
uv run pytest tests/pm_agent/ -v              # Run specific directory
uv run pytest -m confidence_check             # Run by marker
uv run pytest --cov=superagent               # With coverage

# Code Quality
make lint             # Run ruff linter
make format           # Format code with ruff
make doctor           # Health check diagnostics

# Plugin Packaging
make build-plugin            # Build plugin artifacts
make sync-plugin-repo        # Sync to distribution repo

# Maintenance
make clean            # Remove build artifacts
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test categories
uv run pytest -m unit           # Unit tests only
uv run pytest -m integration    # Integration tests only
uv run pytest -m confidence_check  # Confidence check tests

# Run with coverage
uv run pytest --cov=superagent --cov-report=html
```

## ABI Endpoints

Airis Agent exposes three main API endpoints:

### 1. Confidence Gate (`superagent.api.confidence`)

Pre-implementation confidence assessment:

```python
from superagent.api import evaluate_confidence, ConfidenceRequest

request = ConfidenceRequest(
    task_description="Implement OAuth2 authentication",
    has_official_docs=True,
    has_similar_examples=True,
    complexity="medium"
)

response = evaluate_confidence(request)
# response.score: 0.0-1.0
# response.action: "proceed" | "present_alternatives" | "ask_questions"
# response.checklist: List of verification items
```

### 2. Repository Index (`superagent.api.repo_index`)

Generates structured codebase summaries:

```python
from superagent.api import generate_repo_index, RepoIndexRequest

request = RepoIndexRequest(
    repo_path="/path/to/repo",
    output_format="markdown",
    include_file_tree=True
)

response = generate_repo_index(request)
# response.content: Generated index content
# response.format: "markdown" | "json"
```

### 3. Deep Research (`superagent.api.deep_research`)

Multi-step research planning:

```python
from superagent.api import perform_research, ResearchRequest

request = ResearchRequest(
    topic="React Server Components best practices",
    depth="medium",
    sources=["official_docs", "web"]
)

response = perform_research(request)
# response.findings: Research results
# response.sources: List of sources used
# response.confidence: Confidence score
```

## Pytest Plugin Features

The pytest plugin is automatically loaded and provides:

### Fixtures

- `confidence_checker` - Pre-execution confidence assessment
- `self_check_protocol` - Post-implementation validation
- `reflexion_pattern` - Error learning and prevention
- `token_budget` - Token budget allocation
- `pm_context` - PM Agent context

### Markers

- `@pytest.mark.unit` - Unit tests (auto-applied to `/unit/`)
- `@pytest.mark.integration` - Integration tests (auto-applied to `/integration/`)
- `@pytest.mark.confidence_check` - Pre-execution confidence assessment
- `@pytest.mark.self_check` - Post-implementation validation
- `@pytest.mark.reflexion` - Error learning and prevention
- `@pytest.mark.complexity("simple"|"medium"|"complex")` - Task complexity

## Integration with MCP Servers

Airis Agent integrates with multiple MCP servers via **airis-mcp-gateway**:

- **Tavily**: Web search for deep research
- **Context7**: Official documentation lookup (prevents hallucination)
- **Sequential**: Token-efficient reasoning (30-50% reduction)
- **Serena**: Session persistence and memory
- **Mindbase**: Cross-session learning

## Roadmap (2025)

### Q1: ABI Hardening
- Finalize JSON schemas for all endpoints
- Add streaming/partial responses for progress updates
- Document API contracts under `docs/mcp-api-plan.md`

### Q2: Gateway Integrations
- Connect `airis-mcp-gateway` to ABI endpoints
- Publish sample Codex CLI for host-agnostic proof
- MCP server implementation for confidence gate

### Q3: Runtime Enhancements
- Diff-aware incremental repo indexing
- Deep-research planner with actual MCP tool orchestration
- Trace logging and metrics for parallel executor

### Q4: Documentation & Tooling
- Migration guide from SuperClaude to Airis Agent
- Comprehensive API reference
- Video tutorials and example projects

## Contributing

We welcome contributions! Please:

1. Run tests: `uv run pytest`
2. Run linter: `make lint`
3. Use Conventional Commits: `feat:`, `fix:`, `refactor:`, etc.
4. Open PRs against the `next` branch

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Documentation

- **User Guides**: `docs/user-guide/` - Getting started, commands, agents
- **Developer Guides**: `docs/developer-guide/` - Architecture, API reference
- **Reference**: `docs/reference/` - Advanced patterns, troubleshooting
- **Architecture**: `docs/architecture/` - Design decisions, roadmap

## Requirements

- Python 3.10 or higher
- UV (recommended) or pip
- pytest 7.0.0+
- click 8.0.0+
- rich 13.0.0+

## License

MIT License - see [LICENSE](LICENSE) for details.

## Authors

- Kazuki Nakai
- NomenAK (anton.knoery@gmail.com)
- Mithun Gowda B (mithungowda.b7411@gmail.com)

## Links

- **GitHub**: [github.com/agiletec-inc/airis-agent](https://github.com/agiletec-inc/airis-agent)
- **Issues**: [github.com/agiletec-inc/airis-agent/issues](https://github.com/agiletec-inc/airis-agent/issues)
- **Documentation**: [docs/](docs/)
