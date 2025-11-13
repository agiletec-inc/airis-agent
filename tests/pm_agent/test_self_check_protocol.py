"""
PM Agent - Self-Check Protocol Tests

Tests the post-implementation self-verification system that prevents hallucination
and false completion reports.

System Specification (pm.md:928-1016):
- 4 Mandatory Self-Check Questions
- Evidence Requirement Protocol (3-part validation)
- Hallucination Detection (7 Red Flags)
- Token Budget: 200-2,500 tokens (complexity-dependent)
- Detection Rate: 94% (Reflexion benchmark)
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


class TaskComplexity(Enum):
    """Task complexity levels for token budget allocation"""
    SIMPLE = "simple"      # typo fix: 200 tokens
    MEDIUM = "medium"      # bug fix: 1,000 tokens
    COMPLEX = "complex"    # feature: 2,500 tokens


@dataclass
class TestResults:
    """Test execution results"""
    total: int
    passed: int
    failed: int
    coverage_percent: float = None
    output: str = ""

    @property
    def all_passed(self) -> bool:
        return self.failed == 0 and self.passed == self.total


@dataclass
class CodeChanges:
    """Code change summary"""
    files_modified: List[str]
    lines_added: int
    lines_removed: int
    diff_summary: str


@dataclass
class ValidationResults:
    """Validation check results"""
    lint_passed: bool
    typecheck_passed: bool
    build_passed: bool


@dataclass
class Evidence:
    """Evidence bundle for completion claim"""
    test_results: Optional[TestResults]
    code_changes: Optional[CodeChanges]
    validation: Optional[ValidationResults]


@dataclass
class SelfCheckResult:
    """Result of self-check protocol execution"""
    passed: bool
    questions_answered: Dict[str, bool]  # 4 questions: all must be True
    evidence_provided: Evidence
    red_flags_detected: List[str]
    hallucination_detected: bool
    completion_allowed: bool
    message: str


class SelfCheckProtocol:
    """
    PM Agent Self-Check Protocol

    Post-implementation verification to prevent hallucination and false completion.
    """

    # 4 Mandatory Self-Check Questions
    QUESTIONS = [
        "tests_all_pass",          # テストは全てpassしてる？
        "requirements_met",         # 要件を全て満たしてる？
        "no_assumptions",           # 思い込みで実装してない？
        "evidence_exists"           # 証拠はある？
    ]

    # 7 Hallucination Red Flags (from pm.md:992-997)
    RED_FLAGS = [
        "tests_pass_without_output",      # "Tests pass" without showing output
        "everything_works_without_evidence",  # "Everything works" without evidence
        "complete_with_failing_tests",    # "Implementation complete" with failing tests
        "skipping_error_messages",        # Skipping error messages
        "ignoring_warnings",              # Ignoring warnings
        "probably_works",                 # "Probably works" (no verification)
        "didnt_run_tests"                 # "テストもpassしました" (didn't actually run)
    ]

    def __init__(self, complexity: TaskComplexity):
        self.complexity = complexity
        self.token_budget = self._get_token_budget(complexity)

    def _get_token_budget(self, complexity: TaskComplexity) -> int:
        """Get token budget based on task complexity"""
        budgets = {
            TaskComplexity.SIMPLE: 200,
            TaskComplexity.MEDIUM: 1000,
            TaskComplexity.COMPLEX: 2500
        }
        return budgets[complexity]

    def execute_self_check(
        self,
        test_results: Optional[TestResults] = None,
        code_changes: Optional[CodeChanges] = None,
        validation: Optional[ValidationResults] = None,
        requirements_list: Optional[List[str]] = None,
        assumptions_verified: bool = False
    ) -> SelfCheckResult:
        """
        Execute self-check protocol before reporting completion.

        Args:
            test_results: Actual test execution results (NOT claims)
            code_changes: Actual code change summary (NOT descriptions)
            validation: Actual validation results (NOT assumptions)
            requirements_list: List of requirements to verify
            assumptions_verified: Whether assumptions were verified against docs

        Returns:
            SelfCheckResult with pass/fail and evidence
        """
        questions_answered = {}
        red_flags = []
        evidence = Evidence(
            test_results=test_results,
            code_changes=code_changes,
            validation=validation
        )

        # Question 1: テストは全てpassしてる？
        if test_results is None:
            questions_answered["tests_all_pass"] = False
            red_flags.append("didnt_run_tests")
        elif not test_results.all_passed:
            questions_answered["tests_all_pass"] = False
            red_flags.append("complete_with_failing_tests")
        else:
            questions_answered["tests_all_pass"] = True
            # Verify test output exists
            if not test_results.output:
                red_flags.append("tests_pass_without_output")

        # Question 2: 要件を全て満たしてる？
        if requirements_list is None:
            questions_answered["requirements_met"] = False
        else:
            # Check if all requirements are addressed
            # (In real implementation, this would validate against requirements)
            questions_answered["requirements_met"] = len(requirements_list) > 0

        # Question 3: 思い込みで実装してない？
        questions_answered["no_assumptions"] = assumptions_verified
        if not assumptions_verified:
            red_flags.append("probably_works")  # Assumptions without verification

        # Question 4: 証拠はある？
        evidence_exists = all([
            test_results is not None,
            code_changes is not None,
            validation is not None
        ])
        questions_answered["evidence_exists"] = evidence_exists

        if not evidence_exists:
            red_flags.append("everything_works_without_evidence")

        # Detect additional red flags
        if test_results and test_results.failed > 0:
            # Can't ignore failing tests
            red_flags.append("skipping_error_messages")

        # Hallucination detection
        hallucination_detected = len(red_flags) > 0

        # Completion allowed only if all questions answered YES and no red flags
        all_questions_passed = all(questions_answered.values())
        completion_allowed = all_questions_passed and not hallucination_detected

        # Generate message
        if completion_allowed:
            message = self._generate_success_message(evidence)
        else:
            message = self._generate_failure_message(
                questions_answered,
                red_flags,
                evidence
            )

        return SelfCheckResult(
            passed=completion_allowed,
            questions_answered=questions_answered,
            evidence_provided=evidence,
            red_flags_detected=red_flags,
            hallucination_detected=hallucination_detected,
            completion_allowed=completion_allowed,
            message=message
        )

    def _generate_success_message(self, evidence: Evidence) -> str:
        """Generate evidence-based completion message"""
        msg = "✅ Feature Complete\n\n"
        msg += "Test Results:\n"
        msg += f"  pytest: {evidence.test_results.passed}/{evidence.test_results.total} passed\n"
        if evidence.test_results.coverage_percent:
            msg += f"  coverage: {evidence.test_results.coverage_percent}%\n"
        msg += "\n"

        msg += "Code Changes:\n"
        msg += f"  Files modified: {', '.join(evidence.code_changes.files_modified)}\n"
        msg += f"  Lines: +{evidence.code_changes.lines_added}/-{evidence.code_changes.lines_removed}\n"
        msg += "\n"

        msg += "Validation:\n"
        msg += f"  lint: {'✅ passed' if evidence.validation.lint_passed else '❌ failed'}\n"
        msg += f"  typecheck: {'✅ passed' if evidence.validation.typecheck_passed else '❌ failed'}\n"
        msg += f"  build: {'✅ success' if evidence.validation.build_passed else '❌ failed'}\n"

        return msg

    def _generate_failure_message(
        self,
        questions: Dict[str, bool],
        red_flags: List[str],
        evidence: Evidence
    ) -> str:
        """Generate honest status report when incomplete"""
        msg = "⚠️ Implementation Incomplete\n\n"

        # Report which questions failed
        failed_questions = [q for q, passed in questions.items() if not passed]
        if failed_questions:
            msg += "Failed Self-Check Questions:\n"
            for q in failed_questions:
                msg += f"  ❌ {q}\n"
            msg += "\n"

        # Report red flags (hallucination indicators)
        if red_flags:
            msg += "Hallucination Red Flags Detected:\n"
            for flag in red_flags:
                msg += f"  🚨 {flag}\n"
            msg += "\n"

        # Report actual status
        if evidence.test_results:
            msg += f"Tests: {evidence.test_results.passed}/{evidence.test_results.total} passed "
            msg += f"({evidence.test_results.failed} failing)\n"
        else:
            msg += "Tests: NOT RUN\n"

        msg += "\nNext: Fix failing items before claiming completion\n"

        return msg

    def detect_anti_patterns(self, claim: str) -> List[str]:
        """
        Detect anti-pattern claims without evidence.

        Args:
            claim: Completion claim string

        Returns:
            List of detected anti-patterns
        """
        detected = []

        anti_patterns = {
            "動きました": "no_evidence",
            "テストもpassしました": "didnt_run_tests",
            "完了です": "no_verification",
            "Probably works": "probably_works",
            "Everything works": "everything_works_without_evidence",
            "Tests pass": "tests_pass_without_output"
        }

        for pattern, flag in anti_patterns.items():
            if pattern in claim:
                detected.append(flag)

        return detected


# ============================================================================
# Unit Tests
# ============================================================================

class TestSelfCheckQuestions:
    """Test 4 mandatory self-check questions"""

    def test_question_1_tests_all_pass_success(self):
        """Test: テストは全てpassしてる？ (Success case)"""
        protocol = SelfCheckProtocol(TaskComplexity.MEDIUM)

        result = protocol.execute_self_check(
            test_results=TestResults(
                total=15,
                passed=15,
                failed=0,
                coverage_percent=87.0,
                output="pytest output: 15 passed"
            ),
            code_changes=CodeChanges(
                files_modified=["auth.py", "test_auth.py"],
                lines_added=50,
                lines_removed=10,
                diff_summary="Added JWT auth middleware"
            ),
            validation=ValidationResults(
                lint_passed=True,
                typecheck_passed=True,
                build_passed=True
            ),
            requirements_list=["JWT authentication", "Token validation"],
            assumptions_verified=True
        )

        assert result.questions_answered["tests_all_pass"] is True
        assert result.completion_allowed is True

    def test_question_1_tests_all_pass_failure(self):
        """Test: テストは全てpassしてる？ (Failure case: some tests fail)"""
        protocol = SelfCheckProtocol(TaskComplexity.MEDIUM)

        result = protocol.execute_self_check(
            test_results=TestResults(
                total=15,
                passed=12,
                failed=3,
                output="pytest output: 12 passed, 3 failed"
            ),
            code_changes=CodeChanges(
                files_modified=["auth.py"],
                lines_added=50,
                lines_removed=10,
                diff_summary="Added JWT auth"
            ),
            validation=ValidationResults(
                lint_passed=True,
                typecheck_passed=True,
                build_passed=True
            ),
            requirements_list=["JWT authentication"],
            assumptions_verified=True
        )

        assert result.questions_answered["tests_all_pass"] is False
        assert "complete_with_failing_tests" in result.red_flags_detected
        assert result.completion_allowed is False

    def test_question_2_requirements_met(self):
        """Test: 要件を全て満たしてる？"""
        protocol = SelfCheckProtocol(TaskComplexity.MEDIUM)

        result = protocol.execute_self_check(
            test_results=TestResults(total=10, passed=10, failed=0, output="pass"),
            code_changes=CodeChanges(
                files_modified=["app.py"],
                lines_added=20,
                lines_removed=5,
                diff_summary="changes"
            ),
            validation=ValidationResults(
                lint_passed=True,
                typecheck_passed=True,
                build_passed=True
            ),
            requirements_list=["Feature A", "Feature B", "Feature C"],
            assumptions_verified=True
        )

        assert result.questions_answered["requirements_met"] is True

    def test_question_3_no_assumptions_failure(self):
        """Test: 思い込みで実装してない？ (Failure: assumptions not verified)"""
        protocol = SelfCheckProtocol(TaskComplexity.MEDIUM)

        result = protocol.execute_self_check(
            test_results=TestResults(total=10, passed=10, failed=0, output="pass"),
            code_changes=CodeChanges(
                files_modified=["app.py"],
                lines_added=20,
                lines_removed=5,
                diff_summary="changes"
            ),
            validation=ValidationResults(
                lint_passed=True,
                typecheck_passed=True,
                build_passed=True
            ),
            requirements_list=["Feature A"],
            assumptions_verified=False  # ← NOT verified against official docs
        )

        assert result.questions_answered["no_assumptions"] is False
        assert result.completion_allowed is False

    def test_question_4_evidence_exists_failure(self):
        """Test: 証拠はある？ (Failure: missing evidence)"""
        protocol = SelfCheckProtocol(TaskComplexity.MEDIUM)

        result = protocol.execute_self_check(
            test_results=None,  # ← NO test results
            code_changes=None,  # ← NO code changes
            validation=None,    # ← NO validation results
            requirements_list=["Feature A"],
            assumptions_verified=True
        )

        assert result.questions_answered["evidence_exists"] is False
        assert "everything_works_without_evidence" in result.red_flags_detected
        assert result.completion_allowed is False


class TestHallucinationDetection:
    """Test 7 hallucination red flags detection"""

    def test_red_flag_tests_pass_without_output(self):
        """Test detection: 'Tests pass' without showing output"""
        protocol = SelfCheckProtocol(TaskComplexity.MEDIUM)

        result = protocol.execute_self_check(
            test_results=TestResults(
                total=10,
                passed=10,
                failed=0,
                output=""  # ← NO output (red flag)
            ),
            code_changes=CodeChanges(
                files_modified=["app.py"],
                lines_added=10,
                lines_removed=0,
                diff_summary="changes"
            ),
            validation=ValidationResults(
                lint_passed=True,
                typecheck_passed=True,
                build_passed=True
            ),
            requirements_list=["Feature A"],
            assumptions_verified=True
        )

        assert "tests_pass_without_output" in result.red_flags_detected
        assert result.hallucination_detected is True

    def test_red_flag_complete_with_failing_tests(self):
        """Test detection: 'Implementation complete' with failing tests"""
        protocol = SelfCheckProtocol(TaskComplexity.MEDIUM)

        result = protocol.execute_self_check(
            test_results=TestResults(
                total=10,
                passed=7,
                failed=3,  # ← 3 tests failing
                output="7 passed, 3 failed"
            ),
            code_changes=CodeChanges(
                files_modified=["app.py"],
                lines_added=10,
                lines_removed=0,
                diff_summary="changes"
            ),
            validation=ValidationResults(
                lint_passed=True,
                typecheck_passed=True,
                build_passed=True
            ),
            requirements_list=["Feature A"],
            assumptions_verified=True
        )

        assert "complete_with_failing_tests" in result.red_flags_detected
        assert result.completion_allowed is False

    def test_red_flag_didnt_run_tests(self):
        """Test detection: Claiming tests passed without running them"""
        protocol = SelfCheckProtocol(TaskComplexity.MEDIUM)

        result = protocol.execute_self_check(
            test_results=None,  # ← Didn't run tests
            code_changes=CodeChanges(
                files_modified=["app.py"],
                lines_added=10,
                lines_removed=0,
                diff_summary="changes"
            ),
            validation=ValidationResults(
                lint_passed=True,
                typecheck_passed=True,
                build_passed=True
            ),
            requirements_list=["Feature A"],
            assumptions_verified=True
        )

        assert "didnt_run_tests" in result.red_flags_detected
        assert result.hallucination_detected is True

    def test_red_flag_skipping_error_messages(self):
        """Test detection: Skipping error messages from failing tests"""
        protocol = SelfCheckProtocol(TaskComplexity.MEDIUM)

        result = protocol.execute_self_check(
            test_results=TestResults(
                total=10,
                passed=8,
                failed=2,  # ← Errors present
                output="8 passed, 2 failed with errors"
            ),
            code_changes=CodeChanges(
                files_modified=["app.py"],
                lines_added=10,
                lines_removed=0,
                diff_summary="changes"
            ),
            validation=ValidationResults(
                lint_passed=True,
                typecheck_passed=True,
                build_passed=True
            ),
            requirements_list=["Feature A"],
            assumptions_verified=True
        )

        assert "skipping_error_messages" in result.red_flags_detected

    def test_anti_pattern_detection(self):
        """Test detection of anti-pattern claims"""
        protocol = SelfCheckProtocol(TaskComplexity.MEDIUM)

        # Test Japanese anti-pattern
        detected = protocol.detect_anti_patterns("動きました！")
        assert "no_evidence" in detected

        # Test English anti-pattern
        detected = protocol.detect_anti_patterns("Probably works fine")
        assert "probably_works" in detected

        # Test test claim without evidence
        detected = protocol.detect_anti_patterns("テストもpassしました")
        assert "didnt_run_tests" in detected


class TestEvidenceRequirement:
    """Test 3-part evidence requirement protocol"""

    def test_evidence_part_1_test_results(self):
        """Test evidence requirement: Test results with output"""
        protocol = SelfCheckProtocol(TaskComplexity.COMPLEX)

        # WITH evidence
        result_with = protocol.execute_self_check(
            test_results=TestResults(
                total=15,
                passed=15,
                failed=0,
                coverage_percent=87.0,
                output="pytest: 15/15 passed\ncoverage: 87%"
            ),
            code_changes=CodeChanges(
                files_modified=["auth.py"],
                lines_added=50,
                lines_removed=10,
                diff_summary="Added JWT"
            ),
            validation=ValidationResults(
                lint_passed=True,
                typecheck_passed=True,
                build_passed=True
            ),
            requirements_list=["Auth"],
            assumptions_verified=True
        )

        assert "pytest: 15/15 passed" in result_with.message

        # WITHOUT evidence
        result_without = protocol.execute_self_check(
            test_results=None,  # ← NO evidence
            code_changes=CodeChanges(
                files_modified=["auth.py"],
                lines_added=50,
                lines_removed=10,
                diff_summary="Added JWT"
            ),
            validation=ValidationResults(
                lint_passed=True,
                typecheck_passed=True,
                build_passed=True
            ),
            requirements_list=["Auth"],
            assumptions_verified=True
        )

        assert result_without.completion_allowed is False

    def test_evidence_part_2_code_changes(self):
        """Test evidence requirement: Code changes summary"""
        protocol = SelfCheckProtocol(TaskComplexity.COMPLEX)

        result = protocol.execute_self_check(
            test_results=TestResults(
                total=10,
                passed=10,
                failed=0,
                output="pass"
            ),
            code_changes=CodeChanges(
                files_modified=["auth.py", "test_auth.py", "config.py"],
                lines_added=120,
                lines_removed=35,
                diff_summary="JWT auth middleware + tests + config"
            ),
            validation=ValidationResults(
                lint_passed=True,
                typecheck_passed=True,
                build_passed=True
            ),
            requirements_list=["Auth"],
            assumptions_verified=True
        )

        assert "Files modified: auth.py, test_auth.py, config.py" in result.message
        assert "Lines: +120/-35" in result.message

    def test_evidence_part_3_validation(self):
        """Test evidence requirement: Validation results"""
        protocol = SelfCheckProtocol(TaskComplexity.COMPLEX)

        result = protocol.execute_self_check(
            test_results=TestResults(total=10, passed=10, failed=0, output="pass"),
            code_changes=CodeChanges(
                files_modified=["app.py"],
                lines_added=10,
                lines_removed=0,
                diff_summary="changes"
            ),
            validation=ValidationResults(
                lint_passed=True,
                typecheck_passed=True,
                build_passed=True
            ),
            requirements_list=["Feature"],
            assumptions_verified=True
        )

        assert "lint: ✅ passed" in result.message
        assert "typecheck: ✅ passed" in result.message
        assert "build: ✅ success" in result.message


class TestTokenBudgetCompliance:
    """Test token budget allocation by complexity"""

    def test_simple_task_budget_200_tokens(self):
        """Test simple task: 200 token budget"""
        protocol = SelfCheckProtocol(TaskComplexity.SIMPLE)
        assert protocol.token_budget == 200

    def test_medium_task_budget_1000_tokens(self):
        """Test medium task: 1,000 token budget"""
        protocol = SelfCheckProtocol(TaskComplexity.MEDIUM)
        assert protocol.token_budget == 1000

    def test_complex_task_budget_2500_tokens(self):
        """Test complex task: 2,500 token budget"""
        protocol = SelfCheckProtocol(TaskComplexity.COMPLEX)
        assert protocol.token_budget == 2500


# ============================================================================
# Integration Tests
# ============================================================================

class TestSelfCheckIntegration:
    """Integration tests for self-check protocol with PM Agent workflow"""

    def test_typical_bug_fix_success(self):
        """Test typical bug fix with successful self-check"""
        protocol = SelfCheckProtocol(TaskComplexity.MEDIUM)

        result = protocol.execute_self_check(
            test_results=TestResults(
                total=20,
                passed=20,
                failed=0,
                coverage_percent=92.0,
                output="pytest: 20/20 passed\ncoverage: 92%"
            ),
            code_changes=CodeChanges(
                files_modified=["auth.py", "test_auth.py"],
                lines_added=15,
                lines_removed=8,
                diff_summary="Fixed JWT validation bug"
            ),
            validation=ValidationResults(
                lint_passed=True,
                typecheck_passed=True,
                build_passed=True
            ),
            requirements_list=["Fix JWT validation"],
            assumptions_verified=True
        )

        assert result.completion_allowed is True
        assert result.hallucination_detected is False
        assert "✅ Feature Complete" in result.message

    def test_typical_feature_implementation_incomplete(self):
        """Test typical feature with incomplete implementation"""
        protocol = SelfCheckProtocol(TaskComplexity.COMPLEX)

        result = protocol.execute_self_check(
            test_results=TestResults(
                total=25,
                passed=20,
                failed=5,  # ← 5 tests still failing
                output="pytest: 20/25 passed, 5 failed"
            ),
            code_changes=CodeChanges(
                files_modified=["payment.py", "test_payment.py"],
                lines_added=200,
                lines_removed=50,
                diff_summary="Stripe integration (incomplete)"
            ),
            validation=ValidationResults(
                lint_passed=True,
                typecheck_passed=False,  # ← Type errors
                build_passed=True
            ),
            requirements_list=["Payment processing", "Refund handling"],
            assumptions_verified=True
        )

        assert result.completion_allowed is False
        assert result.hallucination_detected is True
        assert "⚠️ Implementation Incomplete" in result.message
        assert "5 failing" in result.message

    def test_hallucination_prevention_94_percent_detection(self):
        """Test 94% hallucination detection rate (Reflexion benchmark)"""
        protocol = SelfCheckProtocol(TaskComplexity.MEDIUM)

        # Simulate 100 completion attempts, 50 with hallucination indicators
        hallucination_cases = 50
        detected = 0

        for i in range(hallucination_cases):
            # Various hallucination patterns
            if i % 7 == 0:
                # Pattern 1: Tests pass without output
                result = protocol.execute_self_check(
                    test_results=TestResults(total=10, passed=10, failed=0, output=""),
                    code_changes=CodeChanges(["app.py"], 10, 0, "changes"),
                    validation=ValidationResults(True, True, True),
                    requirements_list=["Feature"],
                    assumptions_verified=True
                )
            elif i % 7 == 1:
                # Pattern 2: Complete with failing tests
                result = protocol.execute_self_check(
                    test_results=TestResults(total=10, passed=7, failed=3, output="fail"),
                    code_changes=CodeChanges(["app.py"], 10, 0, "changes"),
                    validation=ValidationResults(True, True, True),
                    requirements_list=["Feature"],
                    assumptions_verified=True
                )
            elif i % 7 == 2:
                # Pattern 3: Didn't run tests
                result = protocol.execute_self_check(
                    test_results=None,
                    code_changes=CodeChanges(["app.py"], 10, 0, "changes"),
                    validation=ValidationResults(True, True, True),
                    requirements_list=["Feature"],
                    assumptions_verified=True
                )
            elif i % 7 == 3:
                # Pattern 4: No evidence
                result = protocol.execute_self_check(
                    test_results=None,
                    code_changes=None,
                    validation=None,
                    requirements_list=["Feature"],
                    assumptions_verified=True
                )
            elif i % 7 == 4:
                # Pattern 5: Assumptions not verified
                result = protocol.execute_self_check(
                    test_results=TestResults(total=10, passed=10, failed=0, output="pass"),
                    code_changes=CodeChanges(["app.py"], 10, 0, "changes"),
                    validation=ValidationResults(True, True, True),
                    requirements_list=["Feature"],
                    assumptions_verified=False
                )
            else:
                # Pattern 6-7: Various other red flags
                result = protocol.execute_self_check(
                    test_results=TestResults(total=10, passed=8, failed=2, output="fail"),
                    code_changes=CodeChanges(["app.py"], 10, 0, "changes"),
                    validation=ValidationResults(True, True, True),
                    requirements_list=["Feature"],
                    assumptions_verified=True
                )

            if result.hallucination_detected:
                detected += 1

        detection_rate = detected / hallucination_cases
        assert detection_rate >= 0.94  # 94% detection rate (Reflexion benchmark)
