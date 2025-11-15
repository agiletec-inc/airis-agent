"""
Super Agent

AI-enhanced development framework for Claude Code.
Provides pytest plugin for enhanced testing and optional skills system.
"""

__version__ = "0.4.0"
__author__ = "Kazuki Nakai"

# Expose main components
from .api.confidence import ConfidenceRequest, ConfidenceResponse, evaluate_confidence
from .api.deep_research import ResearchRequest, ResearchResponse, perform_research
from .api.repo_index import RepoIndexRequest, RepoIndexResponse, generate_repo_index
from .airis_agent.confidence import ConfidenceChecker
from .airis_agent.reflexion import ReflexionPattern
from .airis_agent.self_check import SelfCheckProtocol

__all__ = [
    "ConfidenceChecker",
    "SelfCheckProtocol",
    "ReflexionPattern",
    "ConfidenceRequest",
    "ConfidenceResponse",
    "evaluate_confidence",
    "RepoIndexRequest",
    "RepoIndexResponse",
    "generate_repo_index",
    "ResearchRequest",
    "ResearchResponse",
    "perform_research",
    "__version__",
]
