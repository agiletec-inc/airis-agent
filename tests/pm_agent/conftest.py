"""
Pytest Configuration for PM Agent Reflection Tests

Provides fixtures and configuration for all test modules.
"""

from datetime import datetime

import pytest


@pytest.fixture
def current_timestamp() -> datetime:
    """Provide current timestamp for tests"""
    return datetime.now()


@pytest.fixture
def mock_mindbase_available() -> bool:
    """Mock mindbase availability"""
    return True


@pytest.fixture
def mock_mindbase_unavailable() -> bool:
    """Mock mindbase unavailability (fallback mode)"""
    return False


# pytest configuration
def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line(
        "markers", "unit: Unit tests for individual components"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests for workflows"
    )
    config.addinivalue_line(
        "markers", "performance: Performance and efficiency tests"
    )
    config.addinivalue_line(
        "markers", "hallucination: Hallucination detection tests"
    )


# pytest collection hook
def pytest_collection_modifyitems(config, items):
    """Auto-mark tests based on class names"""
    for item in items:
        # Auto-mark based on test class names
        if "Integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif "Performance" in item.nodeid:
            item.add_marker(pytest.mark.performance)
        elif "Hallucination" in item.nodeid:
            item.add_marker(pytest.mark.hallucination)
        else:
            item.add_marker(pytest.mark.unit)
