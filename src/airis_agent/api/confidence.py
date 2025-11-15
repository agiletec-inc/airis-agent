"""ABI wrapper around the ConfidenceChecker implementation."""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from airis_agent.airis_agent.confidence import ConfidenceChecker


@dataclass
class ConfidenceRequest:
    """Structured request for the confidence gate."""

    task: str
    duplicate_check_complete: bool = False
    architecture_check_complete: bool = False
    official_docs_verified: bool = False
    oss_reference_complete: bool = False
    root_cause_identified: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_context(self) -> Dict[str, Any]:
        """Convert request into the dict format used internally."""

        context = dict(self.metadata)
        context.update(
            {
                "task": self.task,
                "duplicate_check_complete": self.duplicate_check_complete,
                "architecture_check_complete": self.architecture_check_complete,
                "official_docs_verified": self.official_docs_verified,
                "oss_reference_complete": self.oss_reference_complete,
                "root_cause_identified": self.root_cause_identified,
            }
        )
        return context


@dataclass
class ConfidenceResponse:
    """Result returned by the confidence gate."""

    score: float
    action: str
    checks: List[str]


def evaluate_confidence(request: ConfidenceRequest) -> ConfidenceResponse:
    """Evaluate implementation readiness via Super Agent's confidence logic."""

    checker = ConfidenceChecker()
    context = request.to_context()
    score = checker.assess(context)
    checks = context.get("confidence_checks", [])

    if score >= 0.9:
        action = "proceed"
    elif score >= 0.7:
        action = "investigate"
    else:
        action = "stop"

    return ConfidenceResponse(score=score, action=action, checks=checks)
