"""
Super Agent CLI

Commands:
    - airis-agent install-skill pm-agent  # Install PM Agent skill
    - airis-agent doctor                   # Check installation health
    - airis-agent version                  # Show version
"""

from .main import main

__all__ = ["main"]
