# Super Agent Common Issues - Quick Reference 🚀

**Problem Solving Guide**: Most frequent issues with practical solutions.

## Top 5 Quick Fixes (90% of Issues)

### 1. Commands Not Working in Claude Code ⚡
```
Problem: /sc:brainstorm doesn't work
Solution: Restart Claude Code completely
Test: /sc:brainstorm "test" should ask questions
```

### 2. Installation Verification
```bash
python3 -m Super Agent --version    # Should show 4.1.5

# If not working:
# For pipx users
pipx upgrade Super Agent

# For pip users
pip install --upgrade Super Agent

# Then reinstall
python3 -m Super Agent install
```

### 3. Permission Issues
```bash
# Permission denied / PEP 668 errors:
# Option 1: Use pipx (recommended)
pipx install Super Agent

# Option 2: Use pip with --user
pip install --user Super Agent

# Option 3: Fix permissions
sudo chown -R $USER ~/.claude
```

### 4. MCP Server Issues
```bash
/sc:analyze . --no-mcp              # Test without MCP servers
node --version                      # Check Node.js 16+ if needed
```

### 5. Component Missing
```bash
python3 -m Super Agent install --components core commands agents modes --force
```

## Platform-Specific Issues

**Windows:**
```cmd
set CLAUDE_CONFIG_DIR=%USERPROFILE%\.claude
python -m Super Agent install --install-dir "%CLAUDE_CONFIG_DIR%"
```

**macOS:**
```bash
brew install python3 node
pip3 install Super Agent
```

**Linux:**
```bash
sudo apt install python3 python3-pip nodejs
pip3 install Super Agent
```

## Verification Checklist
- [ ] `python3 -m Super Agent --version` returns 4.1.5
- [ ] `/sc:brainstorm "test"` works in Claude Code
- [ ] `Super Agent install --list-components` shows components

## When Quick Fixes Don't Work
See [Troubleshooting Guide](troubleshooting.md) for advanced diagnostics.