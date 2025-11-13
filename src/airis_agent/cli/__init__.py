"""
Super Agent CLI

Commands:
    - superagent install-skill pm-agent  # Install PM Agent skill
    - superagent doctor                   # Check installation health
    - superagent version                  # Show version
"""

from .main import main

__all__ = ["main"]
