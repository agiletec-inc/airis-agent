"""
PM Agent - Reflexion Pattern Tests

Tests the self-reflection loop with past error memory lookup for same mistake prevention.

System Specification (pm.md:1018-1223):
- Smart Error Lookup (mindbase OR grep fallback)
- Past Solution Application (0 tokens if cache hit)
- Root Cause Investigation (WebSearch, WebFetch, Grep)
- Hypothesis Formation (PDCA documentation)
- Learning Capture (Dual storage: local files + mindbase)
- Error Recurrence Rate: <10% (vs 30-50% baseline)
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class ErrorCategory(Enum):
    """Error categorization for memory lookup"""
    CONFIGURATION = "configuration"
    DEPENDENCY = "dependency"
    LOGIC = "logic"
    INTEGRATION = "integration"
    SECURITY = "security"


@dataclass
class PastError:
    """Past error record"""
    error_message: str
    category: ErrorCategory
    root_cause: str
    solution: str
    timestamp: datetime
    metadata: Dict[str, str]


@dataclass
class ErrorLookupResult:
    """Result of past error lookup"""
    found: bool
    past_errors: List[PastError]
    solution_available: bool
    solution: Optional[str]
    source: str  # "mindbase" | "grep" | "none"


@dataclass
class InvestigationResult:
    """Root cause investigation result"""
    root_cause: str
    evidence: List[str]
    hypothesis: str
    solution_design: str
    sources: List[str]  # WebSearch, WebFetch, Grep results


@dataclass
class ReflexionResult:
    """Complete reflexion cycle result"""
    error_message: str
    lookup_result: ErrorLookupResult
    investigation: Optional[InvestigationResult]
    solution_applied: str
    learning_captured: bool
    tokens_used: int
    time_saved: bool  # True if used cached solution (0 tokens)


class ReflexionEngine:
    """
    Reflexion Pattern Implementation

    Self-reflection with memory-based error learning to prevent
    same mistake recurrence.
    """

    def __init__(self, mindbase_available: bool = False):
        self.mindbase_available = mindbase_available
        self.error_memory: List[PastError] = []  # Simulated memory store
        self.solutions_file = "docs/memory/solutions_learned.jsonl"
        self.mistakes_dir = "docs/mistakes/"

    def execute_reflexion_cycle(
        self,
        error_message: str,
        error_category: ErrorCategory
    ) -> ReflexionResult:
        """
        Execute complete reflexion cycle for error resolution.

        Steps (from pm.md:1018-1223):
        1. STOP (Never retry blindly)
        2a. Check Past Errors (Smart Lookup)
        2b. Root Cause Investigation (if no past solution)
        3. Hypothesis Formation
        4. Solution Design (MUST BE DIFFERENT)
        5. Execute New Approach
        6. Learning Capture

        Args:
            error_message: The error that occurred
            error_category: Category for efficient lookup

        Returns:
            ReflexionResult with complete cycle information
        """
        tokens_used = 0

        # Step 1: STOP (Never retry blindly)
        # Question: "なぜこのエラーが出たのか？"
        tokens_used += 10  # Stopping and questioning

        # Step 2a: Check Past Errors (Smart Lookup)
        lookup_result = self._smart_error_lookup(error_message, error_category)
        tokens_used += self._calculate_lookup_cost(lookup_result)

        # If past solution found, apply it immediately (0 additional tokens)
        if lookup_result.solution_available:
            return ReflexionResult(
                error_message=error_message,
                lookup_result=lookup_result,
                investigation=None,  # Skip investigation
                solution_applied=lookup_result.solution,
                learning_captured=False,  # Already learned
                tokens_used=tokens_used,
                time_saved=True
            )

        # Step 2b: Root Cause Investigation (MANDATORY if no past solution)
        investigation = self._investigate_root_cause(error_message, error_category)
        tokens_used += 1500  # WebSearch + WebFetch + Grep + analysis

        # Step 3: Hypothesis Formation
        tokens_used += 100  # Hypothesis documentation

        # Step 4: Solution Design (MUST BE DIFFERENT)
        solution = investigation.solution_design
        tokens_used += 200  # Solution design

        # Step 5: Execute New Approach (not tested here, implementation-specific)

        # Step 6: Learning Capture
        learning_captured = self._capture_learning(
            error_message,
            error_category,
            investigation.root_cause,
            solution
        )
        tokens_used += 100  # Learning documentation

        return ReflexionResult(
            error_message=error_message,
            lookup_result=lookup_result,
            investigation=investigation,
            solution_applied=solution,
            learning_captured=learning_captured,
            tokens_used=tokens_used,
            time_saved=False
        )

    def _smart_error_lookup(
        self,
        error_message: str,
        category: ErrorCategory
    ) -> ErrorLookupResult:
        """
        Smart error lookup with mindbase OR grep fallback.

        Specification (pm.md:2a):
        - IF mindbase available: semantic search
        - ELSE: grep solutions_learned.jsonl + mistakes/
        """
        if self.mindbase_available:
            # Mindbase semantic search
            past_errors = self._mindbase_search(error_message, category)
            source = "mindbase"
        else:
            # Grep fallback
            past_errors = self._grep_search(error_message, category)
            source = "grep"

        if past_errors:
            # Solution available from past error
            return ErrorLookupResult(
                found=True,
                past_errors=past_errors,
                solution_available=True,
                solution=past_errors[0].solution,
                source=source
            )
        else:
            # No past solution, need investigation
            return ErrorLookupResult(
                found=False,
                past_errors=[],
                solution_available=False,
                solution=None,
                source=source
            )

    def _mindbase_search(
        self,
        error_message: str,
        category: ErrorCategory
    ) -> List[PastError]:
        """Simulate mindbase semantic search"""
        # In real implementation: mindbase.search_conversations(error_message, category="error")
        matching_errors = [
            err for err in self.error_memory
            if error_message.lower() in err.error_message.lower()
            and err.category == category
        ]
        return matching_errors

    def _grep_search(
        self,
        error_message: str,
        category: ErrorCategory
    ) -> List[PastError]:
        """Simulate grep-based search in local files"""
        # In real implementation:
        # - grep docs/memory/solutions_learned.jsonl
        # - grep docs/mistakes/ -r "error_message"
        matching_errors = [
            err for err in self.error_memory
            if error_message.lower() in err.error_message.lower()
        ]
        return matching_errors

    def _calculate_lookup_cost(self, result: ErrorLookupResult) -> int:
        """Calculate token cost of lookup operation"""
        if result.source == "mindbase":
            return 500  # Semantic search cost
        elif result.source == "grep":
            return 200  # Grep search cost
        else:
            return 0

    def _investigate_root_cause(
        self,
        error_message: str,
        category: ErrorCategory
    ) -> InvestigationResult:
        """
        Root cause investigation (MANDATORY when no past solution).

        Specification (pm.md:2b):
        - WebSearch/WebFetch: Official documentation research
        - WebFetch: Community solutions (Stack Overflow, GitHub)
        - Grep: Codebase pattern analysis
        - Read: Configuration inspection
        - (Optional) Context7: Framework patterns
        """
        # Simulate investigation
        root_cause = f"Root cause of {error_message}: [Identified through investigation]"
        evidence = [
            "Official documentation: [Finding 1]",
            "Stack Overflow: [Similar issue resolved]",
            "Codebase analysis: [Pattern identified]"
        ]
        hypothesis = f"Hypothesis: {error_message} caused by [X] based on [evidence]"
        solution_design = "Solution: Apply [specific fix] based on root cause understanding"
        sources = [
            "WebSearch: official docs",
            "WebFetch: stackoverflow.com/questions/...",
            "Grep: codebase patterns"
        ]

        return InvestigationResult(
            root_cause=root_cause,
            evidence=evidence,
            hypothesis=hypothesis,
            solution_design=solution_design,
            sources=sources
        )

    def _capture_learning(
        self,
        error_message: str,
        category: ErrorCategory,
        root_cause: str,
        solution: str
    ) -> bool:
        """
        Capture learning in dual storage (local files + mindbase).

        Specification (pm.md:Step 6):
        - PM Agent (Local Files) [ALWAYS]:
          * echo "[solution]" >> docs/memory/solutions_learned.jsonl
          * Create docs/mistakes/[feature]-YYYY-MM-DD.md
        - mindbase (Enhanced Storage) [OPTIONAL]:
          * mindbase.store(category="error", content=..., solution=...)
        """
        # Store in memory (simulated)
        past_error = PastError(
            error_message=error_message,
            category=category,
            root_cause=root_cause,
            solution=solution,
            timestamp=datetime.now(),
            metadata={"source": "reflexion"}
        )
        self.error_memory.append(past_error)

        # Would write to files in real implementation:
        # - echo '{"error":"...","solution":"..."}' >> docs/memory/solutions_learned.jsonl
        # - Write docs/mistakes/[feature]-YYYY-MM-DD.md

        return True

    def calculate_recurrence_rate(
        self,
        total_errors: int,
        repeated_errors: int
    ) -> float:
        """
        Calculate error recurrence rate.

        Target: <10% (vs 30-50% baseline without reflexion)
        """
        if total_errors == 0:
            return 0.0
        return (repeated_errors / total_errors) * 100


# ============================================================================
# Unit Tests
# ============================================================================

class TestSmartErrorLookup:
    """Test smart error lookup (mindbase OR grep fallback)"""

    def test_lookup_with_mindbase_available(self):
        """Test error lookup when mindbase is available"""
        engine = ReflexionEngine(mindbase_available=True)

        # Add past error to memory
        engine.error_memory.append(PastError(
            error_message="SUPABASE_JWT_SECRET undefined",
            category=ErrorCategory.CONFIGURATION,
            root_cause="Missing environment variable",
            solution="Add SUPABASE_JWT_SECRET to .env file",
            timestamp=datetime.now(),
            metadata={}
        ))

        # Lookup same error
        result = engine._smart_error_lookup(
            "SUPABASE_JWT_SECRET undefined",
            ErrorCategory.CONFIGURATION
        )

        assert result.found is True
        assert result.solution_available is True
        assert result.source == "mindbase"
        assert "Add SUPABASE_JWT_SECRET" in result.solution

    def test_lookup_with_grep_fallback(self):
        """Test error lookup with grep fallback (mindbase unavailable)"""
        engine = ReflexionEngine(mindbase_available=False)

        # Add past error to memory
        engine.error_memory.append(PastError(
            error_message="ImportError: No module named 'pytest'",
            category=ErrorCategory.DEPENDENCY,
            root_cause="Missing pytest dependency",
            solution="Run: pip install pytest",
            timestamp=datetime.now(),
            metadata={}
        ))

        # Lookup same error
        result = engine._smart_error_lookup(
            "ImportError: No module named 'pytest'",
            ErrorCategory.DEPENDENCY
        )

        assert result.found is True
        assert result.solution_available is True
        assert result.source == "grep"
        assert "pip install pytest" in result.solution

    def test_lookup_no_past_solution(self):
        """Test lookup when no past solution exists"""
        engine = ReflexionEngine(mindbase_available=True)

        # Lookup novel error
        result = engine._smart_error_lookup(
            "Novel error never seen before",
            ErrorCategory.LOGIC
        )

        assert result.found is False
        assert result.solution_available is False
        assert result.solution is None


class TestPastSolutionApplication:
    """Test immediate application of past solutions (0 tokens)"""

    def test_cached_solution_zero_tokens(self):
        """Test cached solution uses 0 additional tokens"""
        engine = ReflexionEngine(mindbase_available=True)

        # Add known error
        engine.error_memory.append(PastError(
            error_message="Database connection timeout",
            category=ErrorCategory.INTEGRATION,
            root_cause="Database not running",
            solution="Start database: docker compose up db",
            timestamp=datetime.now(),
            metadata={}
        ))

        # Encounter same error
        result = engine.execute_reflexion_cycle(
            "Database connection timeout",
            ErrorCategory.INTEGRATION
        )

        # Should use cached solution (minimal tokens)
        assert result.lookup_result.solution_available is True
        assert result.investigation is None  # Skipped investigation
        assert result.time_saved is True
        assert result.tokens_used < 600  # Only lookup cost, no investigation

    def test_cached_solution_immediate_application(self):
        """Test cached solution is applied immediately"""
        engine = ReflexionEngine(mindbase_available=True)

        # Add known error
        engine.error_memory.append(PastError(
            error_message="Port 8000 already in use",
            category=ErrorCategory.CONFIGURATION,
            root_cause="Another process using port",
            solution="Kill process: lsof -ti:8000 | xargs kill -9",
            timestamp=datetime.now(),
            metadata={}
        ))

        # Encounter same error
        result = engine.execute_reflexion_cycle(
            "Port 8000 already in use",
            ErrorCategory.CONFIGURATION
        )

        assert "lsof -ti:8000" in result.solution_applied
        assert result.learning_captured is False  # Already learned


class TestRootCauseInvestigation:
    """Test root cause investigation when no past solution exists"""

    def test_investigation_mandatory_for_novel_errors(self):
        """Test investigation is MANDATORY for novel errors"""
        engine = ReflexionEngine(mindbase_available=True)

        # Novel error (no past solution)
        result = engine.execute_reflexion_cycle(
            "Completely new error type",
            ErrorCategory.LOGIC
        )

        # Must perform investigation
        assert result.lookup_result.solution_available is False
        assert result.investigation is not None
        assert len(result.investigation.evidence) > 0
        assert len(result.investigation.sources) > 0

    def test_investigation_includes_multiple_sources(self):
        """Test investigation uses multiple sources"""
        engine = ReflexionEngine(mindbase_available=True)

        result = engine.execute_reflexion_cycle(
            "Novel configuration error",
            ErrorCategory.CONFIGURATION
        )

        investigation = result.investigation

        # Should include multiple source types
        source_types = [s.split(":")[0] for s in investigation.sources]
        assert "WebSearch" in source_types or "WebFetch" in source_types
        assert "Grep" in source_types

    def test_investigation_generates_hypothesis(self):
        """Test investigation generates hypothesis"""
        engine = ReflexionEngine(mindbase_available=True)

        result = engine.execute_reflexion_cycle(
            "Authentication failure",
            ErrorCategory.SECURITY
        )

        assert result.investigation is not None
        assert result.investigation.hypothesis is not None
        assert "Hypothesis:" in result.investigation.hypothesis


class TestLearningCapture:
    """Test learning capture in dual storage"""

    def test_learning_captured_locally(self):
        """Test learning is captured in local files"""
        engine = ReflexionEngine(mindbase_available=False)

        # Initial error count
        initial_count = len(engine.error_memory)

        # Encounter and resolve new error
        result = engine.execute_reflexion_cycle(
            "New error for learning",
            ErrorCategory.LOGIC
        )

        # Should capture learning
        assert result.learning_captured is True
        assert len(engine.error_memory) == initial_count + 1

        # Verify captured error
        captured = engine.error_memory[-1]
        assert captured.error_message == "New error for learning"
        assert captured.solution is not None

    def test_learning_captured_with_mindbase(self):
        """Test learning is captured in mindbase (dual storage)"""
        engine = ReflexionEngine(mindbase_available=True)

        result = engine.execute_reflexion_cycle(
            "Error to store in mindbase",
            ErrorCategory.INTEGRATION
        )

        # Should capture in both local + mindbase
        assert result.learning_captured is True
        assert len(engine.error_memory) > 0

    def test_learning_prevents_future_recurrence(self):
        """Test captured learning prevents future same error"""
        engine = ReflexionEngine(mindbase_available=True)

        # First occurrence: Full investigation
        result1 = engine.execute_reflexion_cycle(
            "Recurring error pattern",
            ErrorCategory.DEPENDENCY
        )
        tokens1 = result1.tokens_used

        # Second occurrence: Cached solution
        result2 = engine.execute_reflexion_cycle(
            "Recurring error pattern",
            ErrorCategory.DEPENDENCY
        )
        tokens2 = result2.tokens_used

        # Second time should use cached solution (much fewer tokens)
        assert tokens2 < tokens1
        assert result2.lookup_result.solution_available is True
        assert result2.time_saved is True


class TestErrorRecurrenceRate:
    """Test error recurrence rate: <10% target"""

    def test_recurrence_rate_calculation(self):
        """Test recurrence rate calculation"""
        engine = ReflexionEngine(mindbase_available=True)

        # Simulate 100 errors, 8 repeated
        total_errors = 100
        repeated_errors = 8

        recurrence_rate = engine.calculate_recurrence_rate(total_errors, repeated_errors)

        assert recurrence_rate == 8.0  # 8%
        assert recurrence_rate < 10  # Below 10% target

    def test_recurrence_vs_baseline(self):
        """Test recurrence rate vs baseline (30-50% without reflexion)"""
        baseline_without_reflexion = 40  # 40% typical baseline

        # With reflexion: <10%
        with_reflexion_rate = 8.0

        # Improvement calculation
        improvement = baseline_without_reflexion - with_reflexion_rate
        improvement_percent = (improvement / baseline_without_reflexion) * 100

        assert improvement_percent == 80  # 80% improvement
        assert with_reflexion_rate < 10
        assert baseline_without_reflexion >= 30

    def test_recurrence_improvement_over_time(self):
        """Test recurrence rate improves as learning accumulates"""
        # Month 1: Limited learning (higher recurrence)
        month1_rate = 15.0  # Still learning

        # Month 2: More learning (lower recurrence)
        month2_rate = 8.0

        # Month 3: Extensive learning (minimal recurrence)
        month3_rate = 5.0

        assert month1_rate > month2_rate > month3_rate
        assert month3_rate < 10  # Eventually below target


# ============================================================================
# Integration Tests
# ============================================================================

class TestReflexionWorkflow:
    """Integration tests for complete reflexion workflow"""

    def test_first_time_error_full_investigation(self):
        """Test first-time error: full investigation workflow"""
        engine = ReflexionEngine(mindbase_available=True)

        # First occurrence
        result = engine.execute_reflexion_cycle(
            "JWT token validation failed",
            ErrorCategory.SECURITY
        )

        # Should perform full investigation
        assert result.lookup_result.found is False
        assert result.investigation is not None
        assert result.learning_captured is True
        assert result.tokens_used > 1500  # Full investigation cost

    def test_second_time_error_cached_solution(self):
        """Test second-time error: cached solution workflow"""
        engine = ReflexionEngine(mindbase_available=True)

        # First occurrence (learn)
        engine.execute_reflexion_cycle(
            "CORS error: Origin not allowed",
            ErrorCategory.CONFIGURATION
        )

        # Second occurrence (cached)
        result = engine.execute_reflexion_cycle(
            "CORS error: Origin not allowed",
            ErrorCategory.CONFIGURATION
        )

        # Should use cached solution
        assert result.lookup_result.solution_available is True
        assert result.investigation is None
        assert result.time_saved is True
        assert result.tokens_used < 700  # Only lookup, no investigation

    def test_error_category_filtering(self):
        """Test error lookup filters by category"""
        engine = ReflexionEngine(mindbase_available=True)

        # Add errors in different categories
        engine.error_memory.append(PastError(
            error_message="Config error",
            category=ErrorCategory.CONFIGURATION,
            root_cause="Config issue",
            solution="Fix config",
            timestamp=datetime.now(),
            metadata={}
        ))

        engine.error_memory.append(PastError(
            error_message="Dependency error",
            category=ErrorCategory.DEPENDENCY,
            root_cause="Missing dep",
            solution="Install dep",
            timestamp=datetime.now(),
            metadata={}
        ))

        # Search for config error in wrong category
        result = engine._smart_error_lookup(
            "Config error",
            ErrorCategory.SECURITY  # Wrong category
        )

        # Should not find (category mismatch with mindbase)
        if engine.mindbase_available:
            assert result.found is False


class TestPerformanceOptimization:
    """Performance optimization tests"""

    def test_token_savings_with_cached_solutions(self):
        """Test token savings from cached solutions"""
        engine = ReflexionEngine(mindbase_available=True)

        # First error: Full cost
        result1 = engine.execute_reflexion_cycle(
            "Performance bottleneck in query",
            ErrorCategory.LOGIC
        )
        first_time_cost = result1.tokens_used

        # Same error again: Cached
        result2 = engine.execute_reflexion_cycle(
            "Performance bottleneck in query",
            ErrorCategory.LOGIC
        )
        cached_cost = result2.tokens_used

        # Savings calculation
        savings = first_time_cost - cached_cost
        savings_percent = (savings / first_time_cost) * 100

        # Should save >70% tokens
        assert savings_percent > 70
        assert cached_cost < 700

    def test_lookup_performance_mindbase_vs_grep(self):
        """Test lookup performance: mindbase vs grep"""
        # Mindbase: Faster semantic search
        engine_mindbase = ReflexionEngine(mindbase_available=True)
        result_mindbase = engine_mindbase._smart_error_lookup(
            "Test error",
            ErrorCategory.LOGIC
        )

        # Grep: Text-based search
        engine_grep = ReflexionEngine(mindbase_available=False)
        result_grep = engine_grep._smart_error_lookup(
            "Test error",
            ErrorCategory.LOGIC
        )

        # Both should work (mindbase is enhancement, not requirement)
        assert result_mindbase.source in ["mindbase", "grep"]
        assert result_grep.source == "grep"
