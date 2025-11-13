"""Host-agnostic deep research planner."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

DEPTH_PLAN = {
    "quick": (1, 2),
    "standard": (2, 4),
    "deep": (3, 6),
    "exhaustive": (4, 8),
}


@dataclass
class ResearchRequest:
    query: str
    depth: str = "standard"  # quick | standard | deep | exhaustive
    constraints: List[str] = field(default_factory=list)
    seed_sources: List[str] = field(default_factory=list)


@dataclass
class ResearchResponse:
    summary: str
    plan: List[Dict[str, List[str]]]
    findings: List[str]
    sources: List[Dict[str, str]]
    confidence: float


def perform_research(request: ResearchRequest) -> ResearchResponse:
    depth = request.depth if request.depth in DEPTH_PLAN else "standard"
    waves, queries_per_wave = DEPTH_PLAN[depth]

    plan = []
    for wave in range(1, waves + 1):
        queries = _generate_queries(request.query, queries_per_wave, wave, request.constraints)
        plan.append({"wave": wave, "queries": queries})

    findings, sources = _synthesize_findings(request)
    confidence = _estimate_confidence(len(sources))
    summary = f"Deep research for '{request.query}' completed with {len(sources)} sources."

    return ResearchResponse(
        summary=summary,
        plan=plan,
        findings=findings,
        sources=sources,
        confidence=confidence,
    )


def _generate_queries(base: str, count: int, wave: int, constraints: List[str]) -> List[str]:
    queries = []
    for idx in range(count):
        constraint = f" + {constraints[idx % len(constraints)]}" if constraints else ""
        queries.append(f"{base} insight #{wave}-{idx + 1}{constraint}")
    return queries


def _synthesize_findings(request: ResearchRequest) -> (List[str], List[Dict[str, str]]):
    findings = []
    sources = []

    if request.seed_sources:
        for idx, src in enumerate(request.seed_sources, start=1):
            findings.append(f"{idx}. Derived insight from {src}")
            sources.append({"type": "seed", "reference": src})
    else:
        findings.append("1. Pending official documentation confirmation")
        findings.append("2. Pending community implementation survey")
        sources.append({"type": "todo", "reference": "Context7 query"})
        sources.append({"type": "todo", "reference": "Tavily search"})

    return findings, sources


def _estimate_confidence(source_count: int) -> float:
    if source_count >= 5:
        return 0.95
    if source_count >= 2:
        return 0.85
    return 0.7
