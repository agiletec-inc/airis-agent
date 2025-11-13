"""
PM Agent Reflection Systems Test Suite

Tests for the autonomous reflection system that prevents hallucination
and optimizes token usage.

Test Coverage:
- test_confidence_check.py: 3-tier confidence scoring (90-100%, 70-89%, <70%)
- test_self_check_protocol.py: 4-question verification + hallucination detection (94%)
- test_token_budget.py: Budget allocation (200/1K/2.5K tokens) + 80-95% savings
- test_reflexion_pattern.py: Past error lookup + learning capture + <10% recurrence

Expected Quality Metrics:
- Hallucination Detection: 94% (Reflexion benchmark)
- Token Efficiency: 60% average reduction
- Error Recurrence: <10% (vs 30-50% baseline)
- Confidence Accuracy: >85%
"""

__version__ = "1.0.0"
__author__ = "PM Agent Team"
