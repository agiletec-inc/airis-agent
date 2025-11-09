.PHONY: install test test-plugin doctor verify clean lint format build-plugin sync-plugin-repo help

# Installation (local source, editable) - RECOMMENDED
install:
	@echo "🔧 Installing Super Agent (development mode)..."
	uv pip install -e ".[dev]"
	@echo ""
	@echo "✅ Installation complete!"
	@echo "   Run 'make verify' to check installation"

# Run tests
test:
	@echo "Running tests..."
	uv run pytest

# Test pytest plugin loading
test-plugin:
	@echo "Testing pytest plugin auto-discovery..."
	@uv run python -m pytest --trace-config 2>&1 | grep -A2 "registered third-party plugins:" | grep superagent && echo "✅ Plugin loaded successfully" || echo "❌ Plugin not loaded"

# Run doctor command
doctor:
	@echo "Running Super Agent health check..."
	@uv run superagent doctor

# Verify Phase 1 installation
verify:
	@echo "🔍 Phase 1 Installation Verification"
	@echo "======================================"
	@echo ""
	@echo "1. Package location:"
	@uv run python -c "import superagent; print(f'   {superagent.__file__}')"
	@echo ""
	@echo "2. Package version:"
	@uv run superagent --version | sed 's/^/   /'
	@echo ""
	@echo "3. Pytest plugin:"
	@uv run python -m pytest --trace-config 2>&1 | grep "registered third-party plugins:" -A2 | grep superagent | sed 's/^/   /' && echo "   ✅ Plugin loaded" || echo "   ❌ Plugin not loaded"
	@echo ""
	@echo "4. Health check:"
	@uv run superagent doctor | grep "Super Agent is healthy" > /dev/null && echo "   ✅ All checks passed" || echo "   ❌ Some checks failed"
	@echo ""
	@echo "======================================"
	@echo "✅ Phase 1 verification complete"

# Linting
lint:
	@echo "Running linter..."
	uv run ruff check .

# Format code
format:
	@echo "Formatting code..."
	uv run ruff format .

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .ruff_cache -exec rm -rf {} +

PLUGIN_DIST := dist/plugins/superagent
PLUGIN_REPO ?= ../Super Agent_Plugin

.PHONY: build-plugin
build-plugin: ## Build Super Agent plugin artefacts into dist/
	@echo "🛠️  Building Super Agent plugin from unified sources..."
	@uv run python scripts/build_superagent_plugin.py

.PHONY: sync-plugin-repo
sync-plugin-repo: build-plugin ## Sync built plugin artefacts into ../Super Agent_Plugin
	@if [ ! -d "$(PLUGIN_REPO)" ]; then \
		echo "❌ Target plugin repository not found at $(PLUGIN_REPO)"; \
		echo "   Set PLUGIN_REPO=/path/to/Super Agent_Plugin when running make."; \
		exit 1; \
	fi
	@echo "📦 Syncing artefacts to $(PLUGIN_REPO)..."
	@rsync -a --delete $(PLUGIN_DIST)/agents/ $(PLUGIN_REPO)/agents/
	@rsync -a --delete $(PLUGIN_DIST)/commands/ $(PLUGIN_REPO)/commands/
	@rsync -a --delete $(PLUGIN_DIST)/hooks/ $(PLUGIN_REPO)/hooks/
	@rsync -a --delete $(PLUGIN_DIST)/scripts/ $(PLUGIN_REPO)/scripts/
	@rsync -a --delete $(PLUGIN_DIST)/skills/ $(PLUGIN_REPO)/skills/
	@rsync -a --delete $(PLUGIN_DIST)/.claude-plugin/ $(PLUGIN_REPO)/.claude-plugin/
	@echo "✅ Sync complete."

# Show help
help:
	@echo "Super Agent - Available commands:"
	@echo ""
	@echo "🚀 Quick Start:"
	@echo "  make install         - Install in development mode (RECOMMENDED)"
	@echo "  make verify          - Verify installation is working"
	@echo ""
	@echo "🔧 Development:"
	@echo "  make test            - Run test suite"
	@echo "  make test-plugin     - Test pytest plugin auto-discovery"
	@echo "  make doctor          - Run health check"
	@echo "  make lint            - Run linter (ruff check)"
	@echo "  make format          - Format code (ruff format)"
	@echo "  make clean           - Clean build artifacts"
	@echo ""
	@echo "🔌 Plugin Packaging:"
	@echo "  make build-plugin    - Build Super Agent plugin artefacts into dist/"
	@echo "  make sync-plugin-repo - Sync artefacts into ../Super Agent_Plugin"
	@echo ""
	@echo "📚 Documentation:"
	@echo "  make translate       - Translate README to Chinese and Japanese"
	@echo "  make help            - Show this help message"
	@echo ""
