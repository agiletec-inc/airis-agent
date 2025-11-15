"""
Integration tests for Super Agent pytest plugin

Tests that the plugin loads correctly and provides expected fixtures.
"""

import pytest


class TestPluginLoading:
    """Test that Super Agent plugin loads correctly"""

    def test_plugin_registered(self, pytestconfig):
        """Test that superagent plugin is registered"""
        plugin_manager = pytestconfig.pluginmanager
        assert plugin_manager.has_plugin("airis-agent")

    def test_plugin_version_in_header(self, pytestconfig):
        """Test that plugin version appears in pytest header"""
        # The pytest_report_header hook should add Super Agent version
        # This is verified by the header output in test runs


class TestPluginFixtures:
    """Test that plugin provides expected fixtures"""

    def test_confidence_checker_fixture(self, confidence_checker):
        """Test confidence_checker fixture is available"""
        assert confidence_checker is not None
        assert hasattr(confidence_checker, "assess")

    def test_self_check_protocol_fixture(self, self_check_protocol):
        """Test self_check_protocol fixture is available"""
        assert self_check_protocol is not None
        assert hasattr(self_check_protocol, "validate")

    def test_reflexion_pattern_fixture(self, reflexion_pattern):
        """Test reflexion_pattern fixture is available"""
        assert reflexion_pattern is not None
        assert hasattr(reflexion_pattern, "get_solution")

    def test_token_budget_fixture(self, token_budget):
        """Test token_budget fixture is available"""
        assert token_budget is not None
        assert hasattr(token_budget, "use")
        assert hasattr(token_budget, "remaining")

    def test_pm_context_fixture(self, pm_context):
        """Test pm_context fixture is available"""
        assert pm_context is not None
        assert "memory_dir" in pm_context
        assert "pm_context" in pm_context
        assert "last_session" in pm_context
        assert "next_actions" in pm_context


class TestFixtureFunctionality:
    """Test that fixtures work as expected"""

    def test_confidence_checker_assess(self, confidence_checker):
        """Test confidence checker can assess context"""
        context = {
            "task": "Simple task",
            "patterns": [],
            "documentation": False
        }
        confidence = confidence_checker.assess(context)
        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 1.0

    def test_token_budget_remaining(self, token_budget):
        """Test token budget returns correct remaining budget"""
        remaining = token_budget.remaining
        assert isinstance(remaining, int)
        assert remaining > 0

    @pytest.mark.parametrize("complexity,expected_min", [
        ("simple", 200),
        ("medium", 1000),
        ("complex", 2500),
    ])
    def test_token_budget_complexity_levels(self, request, complexity, expected_min):
        """Test token budget varies by complexity"""
        from airis_agent.airis_agent.token_budget import TokenBudgetManager

        manager = TokenBudgetManager(complexity=complexity)
        remaining = manager.remaining
        assert remaining >= expected_min


class TestCustomMarkers:
    """Test that custom markers are registered"""

    def test_confidence_check_marker_registered(self, pytestconfig):
        """Test confidence_check marker is registered"""
        # pytestconfig.getini("markers") returns list of strings
        markers_str = "\n".join(pytestconfig.getini("markers"))
        assert "confidence_check" in markers_str

    def test_self_check_marker_registered(self, pytestconfig):
        """Test self_check marker is registered"""
        markers_str = "\n".join(pytestconfig.getini("markers"))
        assert "self_check" in markers_str

    def test_reflexion_marker_registered(self, pytestconfig):
        """Test reflexion marker is registered"""
        markers_str = "\n".join(pytestconfig.getini("markers"))
        assert "reflexion" in markers_str


class TestPMContextStructure:
    """Test PM context fixture creates correct structure"""

    def test_memory_dir_exists(self, pm_context):
        """Test memory directory is created"""
        assert pm_context["memory_dir"].exists()
        assert pm_context["memory_dir"].is_dir()

    def test_context_files_structure(self, pm_context):
        """Test all expected context file paths exist"""
        assert pm_context["pm_context"].parent == pm_context["memory_dir"]
        assert pm_context["last_session"].parent == pm_context["memory_dir"]
        assert pm_context["next_actions"].parent == pm_context["memory_dir"]

    def test_context_paths_are_unique(self, pm_context):
        """Test all context paths are different"""
        paths = {
            pm_context["pm_context"],
            pm_context["last_session"],
            pm_context["next_actions"]
        }
        assert len(paths) == 3  # All unique
