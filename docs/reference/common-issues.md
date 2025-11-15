# Airis Agent Common Issues - Quick Reference 🚀

**Problem Solving Guide**: Most frequent issues with practical solutions.

## Top 5 Quick Fixes (90% of Issues)

### 1. Commands Not Working in Claude Code ⚡
```
Problem: /airis:brainstorm doesn't work
Solution: Restart Claude Code completely
Test: /airis:brainstorm "test" should ask questions
```

### 2. Installation Verification
```bash
python3 -m Airis Agent --version    # Should show 4.1.5

# If not working:
# For pipx users
pipx upgrade Airis Agent

# For pip users
pip install --upgrade Airis Agent

# Then reinstall
python3 -m Airis Agent install
```

### 3. Permission Issues
```bash
# Permission denied / PEP 668 errors:
# Option 1: Use pipx (recommended)
pipx install Airis Agent

# Option 2: Use pip with --user
pip install --user Airis Agent

# Option 3: Fix permissions
sudo chown -R $USER ~/.claude
```

### 4. MCP Server Issues
```bash
/airis:analyze . --no-mcp              # Test without MCP servers
node --version                      # Check Node.js 16+ if needed
```

### 5. Component Missing
```bash
python3 -m Airis Agent install --components core commands agents modes --force
```

## Platform-Specific Issues

**Windows:**
```cmd
set CLAUDE_CONFIG_DIR=%USERPROFILE%\.claude
python -m Airis Agent install --install-dir "%CLAUDE_CONFIG_DIR%"
```

**macOS:**
```bash
brew install python3 node
pip3 install Airis Agent
```

**Linux:**
```bash
sudo apt install python3 python3-pip nodejs
pip3 install Airis Agent
```

## Verification Checklist
- [ ] `python3 -m Airis Agent --version` returns 4.1.5
- [ ] `/airis:brainstorm "test"` works in Claude Code
- [ ] `Airis Agent install --list-components` shows components

## When Quick Fixes Don't Work
See [Troubleshooting Guide](troubleshooting.md) for advanced diagnostics.