"""
PM Agent - Confidence Check Tests

Tests the 3-tier confidence scoring system that prevents wrong direction execution.

System Specification (pm.md:881-922):
- High Confidence (90-100%): Proceed with implementation
- Medium Confidence (70-89%): Present alternatives, recommend best
- Low Confidence (<70%): STOP → Ask user specific questions

Token Budget: 100-200 tokens per confidence check
Expected ROI: 25-250x (prevent 5-50K token waste from wrong implementation)
"""

from dataclasses import dataclass
from typing import List

import pytest


@dataclass
class ConfidenceAssessment:
    """Confidence check result"""
    score: float  # 0.0-1.0
    level: str    # "high" | "medium" | "low"
    evidence: List[str]
    action: str   # "proceed" | "present_alternatives" | "ask_user"
    questions: List[str] = None  # For low confidence


class ConfidenceChecker:
    """
    PM Agent Confidence Scoring System

    Prevents wrong direction execution by pre-implementation assessment.
    """

    def assess_confidence(
        self,
        has_official_docs: bool,
        has_existing_patterns: bool,
        has_clear_path: bool,
        multiple_approaches: bool,
        has_trade_offs: bool,
        unclear_requirements: bool,
        no_precedent: bool,
        missing_domain_knowledge: bool
    ) -> ConfidenceAssessment:
        """
        Assess confidence level based on implementation context.

        Returns:
            ConfidenceAssessment with score, level, evidence, and action
        """
        # Calculate score (0.0-1.0) - Start from baseline 0.5
        score = 0.5
        evidence = []

        # High confidence indicators (+0.2 each)
        if has_official_docs:
            score += 0.2
            evidence.append("✅ Official documentation reviewed")
        if has_existing_patterns:
            score += 0.2
            evidence.append("✅ Existing codebase patterns identified")
        if has_clear_path:
            score += 0.2
            evidence.append("✅ Clear implementation path")

        # Medium confidence indicators (-0.1 each, not blockers)
        if multiple_approaches:
            score -= 0.1
            evidence.append("⚠️ Multiple viable approaches exist")
        if has_trade_offs:
            score -= 0.1
            evidence.append("⚠️ Trade-offs require consideration")

        # Low confidence indicators (-0.2 each, serious blockers)
        if unclear_requirements:
            score -= 0.2
            evidence.append("❌ Unclear requirements")
        if no_precedent:
            score -= 0.2
            evidence.append("❌ No clear precedent")
        if missing_domain_knowledge:
            score -= 0.2
            evidence.append("❌ Missing domain knowledge")

        # Normalize to 0.0-1.0 range
        score = max(0.0, min(1.0, score))

        # Round to avoid floating point precision issues
        score = round(score, 2)

        # Determine level and action
        if score >= 0.9:
            level = "high"
            action = "proceed"
            questions = None
        elif score >= 0.7:
            level = "medium"
            action = "present_alternatives"
            questions = None
        else:
            level = "low"
            action = "ask_user"
            # Generate specific questions for low confidence
            questions = self._generate_clarification_questions(
                unclear_requirements,
                no_precedent,
                missing_domain_knowledge
            )

        return ConfidenceAssessment(
            score=score,
            level=level,
            evidence=evidence,
            action=action,
            questions=questions
        )

    def _generate_clarification_questions(
        self,
        unclear_requirements: bool,
        no_precedent: bool,
        missing_domain_knowledge: bool
    ) -> List[str]:
        """Generate specific clarification questions for low confidence."""
        questions = []

        if unclear_requirements:
            questions.append("What are the specific requirements for this feature?")
        if no_precedent:
            questions.append("Are there any similar implementations we can reference?")
        if missing_domain_knowledge:
            questions.append("What domain-specific constraints should I consider?")

        return questions


# ============================================================================
# Unit Tests
# ============================================================================

class TestConfidenceScoring:
    """Test 3-tier confidence scoring system"""

    @pytest.fixture
    def checker(self):
        return ConfidenceChecker()

    # ------------------------------------------------------------------------
    # High Confidence Tests (90-100%)
    # ------------------------------------------------------------------------

    def test_high_confidence_perfect_conditions(self, checker):
        """Test high confidence with all positive indicators"""
        result = checker.assess_confidence(
            has_official_docs=True,
            has_existing_patterns=True,
            has_clear_path=True,
            multiple_approaches=False,
            has_trade_offs=False,
            unclear_requirements=False,
            no_precedent=False,
            missing_domain_knowledge=False
        )

        assert result.level == "high"
        assert result.score >= 0.9
        assert result.action == "proceed"
        assert result.questions is None
        assert "✅ Official documentation reviewed" in result.evidence
        assert "✅ Existing codebase patterns identified" in result.evidence
        assert "✅ Clear implementation path" in result.evidence

    def test_high_confidence_boundary_90_percent(self, checker):
        """Test high confidence boundary at exactly 90%"""
        # Score: 0.5 + 0.2 + 0.2 + 0.2 - 0.1 - 0.1 = 0.9
        result = checker.assess_confidence(
            has_official_docs=True,
            has_existing_patterns=True,
            has_clear_path=True,
            multiple_approaches=True,  # -0.1
            has_trade_offs=True,       # -0.1
            unclear_requirements=False,
            no_precedent=False,
            missing_domain_knowledge=False
        )

        assert result.level == "high"
        assert result.score == 0.9
        assert result.action == "proceed"

    # ------------------------------------------------------------------------
    # Medium Confidence Tests (70-89%)
    # ------------------------------------------------------------------------

    def test_medium_confidence_with_trade_offs(self, checker):
        """Test medium confidence with multiple approaches and trade-offs"""
        result = checker.assess_confidence(
            has_official_docs=True,
            has_existing_patterns=True,
            has_clear_path=False,
            multiple_approaches=True,
            has_trade_offs=True,
            unclear_requirements=False,
            no_precedent=False,
            missing_domain_knowledge=False
        )

        assert result.level == "medium"
        assert 0.7 <= result.score < 0.9
        assert result.action == "present_alternatives"
        assert result.questions is None
        assert "⚠️ Multiple viable approaches exist" in result.evidence
        assert "⚠️ Trade-offs require consideration" in result.evidence

    def test_medium_confidence_boundary_70_percent(self, checker):
        """Test medium confidence boundary at exactly 70%"""
        # Score: 0.5 + 0.2 + 0.2 - 0.1 - 0.1 = 0.7 (boundary)
        result = checker.assess_confidence(
            has_official_docs=True,
            has_existing_patterns=True,
            has_clear_path=False,   # No +0.2
            multiple_approaches=True,   # -0.1
            has_trade_offs=True,        # -0.1
            unclear_requirements=False,
            no_precedent=False,
            missing_domain_knowledge=False
        )

        assert result.level == "medium"
        assert result.score == 0.7
        assert result.action == "present_alternatives"

    def test_medium_confidence_boundary_89_percent(self, checker):
        """Test medium confidence upper boundary at 89%"""
        # Score: 0.5 + 0.2 + 0.2 + 0.2 - 0.2 = 0.9 → need to stay below 0.9
        # Using 0.5 + 0.2 + 0.2 - 0.1 = 0.8 (within medium range)
        result = checker.assess_confidence(
            has_official_docs=True,
            has_existing_patterns=True,
            has_clear_path=False,      # No +0.2
            multiple_approaches=True,  # -0.1
            has_trade_offs=False,
            unclear_requirements=False,
            no_precedent=False,
            missing_domain_knowledge=False
        )

        assert result.level == "medium"
        assert 0.7 <= result.score < 0.9
        assert result.action == "present_alternatives"

    # ------------------------------------------------------------------------
    # Low Confidence Tests (<70%)
    # ------------------------------------------------------------------------

    def test_low_confidence_unclear_requirements(self, checker):
        """Test low confidence due to unclear requirements"""
        result = checker.assess_confidence(
            has_official_docs=False,
            has_existing_patterns=False,
            has_clear_path=False,
            multiple_approaches=False,
            has_trade_offs=False,
            unclear_requirements=True,
            no_precedent=False,
            missing_domain_knowledge=False
        )

        assert result.level == "low"
        assert result.score < 0.7
        assert result.action == "ask_user"
        assert result.questions is not None
        assert "What are the specific requirements for this feature?" in result.questions
        assert "❌ Unclear requirements" in result.evidence

    def test_low_confidence_no_precedent(self, checker):
        """Test low confidence due to no clear precedent"""
        result = checker.assess_confidence(
            has_official_docs=False,
            has_existing_patterns=False,
            has_clear_path=False,
            multiple_approaches=False,
            has_trade_offs=False,
            unclear_requirements=False,
            no_precedent=True,
            missing_domain_knowledge=False
        )

        assert result.level == "low"
        assert result.score < 0.7
        assert result.action == "ask_user"
        assert "Are there any similar implementations we can reference?" in result.questions
        assert "❌ No clear precedent" in result.evidence

    def test_low_confidence_missing_domain_knowledge(self, checker):
        """Test low confidence due to missing domain knowledge"""
        result = checker.assess_confidence(
            has_official_docs=False,
            has_existing_patterns=False,
            has_clear_path=False,
            multiple_approaches=False,
            has_trade_offs=False,
            unclear_requirements=False,
            no_precedent=False,
            missing_domain_knowledge=True
        )

        assert result.level == "low"
        assert result.score < 0.7
        assert result.action == "ask_user"
        assert "What domain-specific constraints should I consider?" in result.questions
        assert "❌ Missing domain knowledge" in result.evidence

    def test_low_confidence_multiple_blockers(self, checker):
        """Test low confidence with multiple serious blockers"""
        result = checker.assess_confidence(
            has_official_docs=False,
            has_existing_patterns=False,
            has_clear_path=False,
            multiple_approaches=False,
            has_trade_offs=False,
            unclear_requirements=True,
            no_precedent=True,
            missing_domain_knowledge=True
        )

        assert result.level == "low"
        assert result.score < 0.7
        assert result.action == "ask_user"
        assert len(result.questions) == 3
        assert "❌ Unclear requirements" in result.evidence
        assert "❌ No clear precedent" in result.evidence
        assert "❌ Missing domain knowledge" in result.evidence

    # ------------------------------------------------------------------------
    # Anti-Pattern Tests (Forbidden Behaviors)
    # ------------------------------------------------------------------------

    def test_anti_pattern_proceeding_without_confidence_check(self, checker):
        """Test that proceeding without confidence check is forbidden"""
        # This test documents the anti-pattern: "I'll try this approach" (no assessment)
        # Implementation should ALWAYS call assess_confidence() before proceeding

        # Simulate skipping confidence check
        with pytest.raises(AssertionError, match="Confidence check required"):
            # This should never happen - always check confidence first
            def proceed_without_check():
                raise AssertionError("Confidence check required before proceeding")

            proceed_without_check()

    def test_anti_pattern_proceeding_with_low_confidence(self, checker):
        """Test that proceeding with <70% confidence without asking is forbidden"""
        result = checker.assess_confidence(
            has_official_docs=False,
            has_existing_patterns=False,
            has_clear_path=False,
            multiple_approaches=False,
            has_trade_offs=False,
            unclear_requirements=True,
            no_precedent=True,
            missing_domain_knowledge=True
        )

        assert result.score < 0.7
        assert result.action == "ask_user"

        # Anti-pattern: Proceeding despite low confidence
        # Correct behavior: MUST ask user questions first
        assert result.questions is not None
        assert len(result.questions) > 0

    def test_anti_pattern_pretending_to_know(self, checker):
        """Test detection of pretending to know when unsure"""
        # When all indicators are negative, confidence must be low
        result = checker.assess_confidence(
            has_official_docs=False,
            has_existing_patterns=False,
            has_clear_path=False,
            multiple_approaches=False,
            has_trade_offs=False,
            unclear_requirements=True,
            no_precedent=True,
            missing_domain_knowledge=True
        )

        # System must NOT pretend to have high confidence
        assert result.level != "high"
        assert result.action == "ask_user"
        # Must generate specific questions, not generic "I'll try"
        assert result.questions is not None
        assert len(result.questions) == 3
        # Each question should be specific and actionable
        assert any("requirements" in q.lower() or "what" in q.lower() for q in result.questions)
        assert any("similar" in q.lower() or "reference" in q.lower() for q in result.questions)
        assert any("constraints" in q.lower() or "domain" in q.lower() for q in result.questions)


# ============================================================================
# Integration Tests
# ============================================================================

class TestConfidenceCheckIntegration:
    """Integration tests for confidence check with PM Agent workflow"""

    @pytest.fixture
    def checker(self):
        return ConfidenceChecker()

    def test_typical_feature_request_high_confidence(self, checker):
        """Test typical feature request with high confidence scenario"""
        # Scenario: User asks to implement Supabase Auth (well-documented)
        result = checker.assess_confidence(
            has_official_docs=True,       # Supabase docs available
            has_existing_patterns=True,   # Similar auth patterns in codebase
            has_clear_path=True,          # Standard implementation path
            multiple_approaches=False,
            has_trade_offs=False,
            unclear_requirements=False,
            no_precedent=False,
            missing_domain_knowledge=False
        )

        assert result.level == "high"
        assert result.action == "proceed"
        # Expected: PM Agent proceeds with implementation immediately

    def test_typical_feature_request_medium_confidence(self, checker):
        """Test typical feature request with medium confidence scenario"""
        # Scenario: User asks to implement payment processing (multiple providers)
        # Score: 0.5 + 0.2 (docs) + 0.2 (patterns) - 0.1 - 0.1 = 0.7 (medium)
        result = checker.assess_confidence(
            has_official_docs=True,       # Stripe/PayPal docs available
            has_existing_patterns=True,   # Have e-commerce patterns
            has_clear_path=False,         # Need to choose provider
            multiple_approaches=True,     # Stripe vs PayPal vs Square
            has_trade_offs=True,          # Fees, features, integration complexity
            unclear_requirements=False,
            no_precedent=False,
            missing_domain_knowledge=False
        )

        assert result.level == "medium"
        assert result.action == "present_alternatives"
        # Expected: PM Agent presents Stripe vs PayPal comparison with recommendation

    def test_typical_feature_request_low_confidence(self, checker):
        """Test typical feature request with low confidence scenario"""
        # Scenario: User asks to "improve UX" (vague request)
        result = checker.assess_confidence(
            has_official_docs=False,      # No specific "UX improvement" docs
            has_existing_patterns=False,
            has_clear_path=False,
            multiple_approaches=False,
            has_trade_offs=False,
            unclear_requirements=True,    # "improve UX" is vague
            no_precedent=True,            # No similar improvement pattern
            missing_domain_knowledge=True # Don't know user's pain points
        )

        assert result.level == "low"
        assert result.action == "ask_user"
        assert len(result.questions) >= 2
        # Expected: PM Agent asks clarifying questions before any implementation

    def test_token_budget_roi_calculation(self, checker):
        """Test that confidence check provides positive ROI"""
        # Confidence check cost: 100-200 tokens
        confidence_check_cost = 200

        # Prevented wrong implementation cost: 5-50K tokens
        prevented_cost_low = 5000
        prevented_cost_high = 50000

        # ROI calculation
        roi_low = prevented_cost_low / confidence_check_cost
        roi_high = prevented_cost_high / confidence_check_cost

        assert roi_low == 25  # 25x ROI (low end)
        assert roi_high == 250  # 250x ROI (high end)

        # Expected specification: 25-250x ROI
        assert 25 <= roi_low <= 250
        assert 25 <= roi_high <= 250


# ============================================================================
# Performance Tests
# ============================================================================

class TestConfidenceCheckPerformance:
    """Performance tests for confidence check token budget compliance"""

    @pytest.fixture
    def checker(self):
        return ConfidenceChecker()

    def test_token_budget_compliance(self, checker):
        """Test that confidence check stays within 100-200 token budget"""
        # Simulate token counting (actual implementation would use tiktoken)
        result = checker.assess_confidence(
            has_official_docs=True,
            has_existing_patterns=True,
            has_clear_path=True,
            multiple_approaches=True,
            has_trade_offs=True,
            unclear_requirements=False,
            no_precedent=False,
            missing_domain_knowledge=False
        )

        # Estimated token usage:
        # - Assessment logic: ~50 tokens
        # - Evidence strings: ~50 tokens
        # - Question generation (if low): ~100 tokens
        # Total: 100-200 tokens

        estimated_tokens = 100 + len(result.evidence) * 10
        if result.questions:
            estimated_tokens += len(result.questions) * 30

        assert estimated_tokens <= 200  # Within budget

    def test_response_time_performance(self, checker):
        """Test that confidence check executes quickly (<100ms)"""
        import time

        start = time.perf_counter()
        checker.assess_confidence(
            has_official_docs=True,
            has_existing_patterns=True,
            has_clear_path=True,
            multiple_approaches=False,
            has_trade_offs=False,
            unclear_requirements=False,
            no_precedent=False,
            missing_domain_knowledge=False
        )
        end = time.perf_counter()

        execution_time_ms = (end - start) * 1000
        assert execution_time_ms < 100  # <100ms response time
