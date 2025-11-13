# PM Agent Reflection Systems Test Suite

Comprehensive test suite for the PM Agent autonomous reflection system that prevents hallucination and optimizes token usage.

## Test Coverage

### 1. test_confidence_check.py (628 lines)
**Tests**: 3-tier confidence scoring system

**Coverage**:
- ✅ High Confidence (90-100%): Proceed with implementation
- ✅ Medium Confidence (70-89%): Present alternatives
- ✅ Low Confidence (<70%): Ask user questions
- ✅ Boundary conditions (70%, 90%)
- ✅ Anti-pattern detection (proceeding without check)
- ✅ Token budget compliance (100-200 tokens)
- ✅ ROI calculation (25-250x return)

**Key Metrics**:
- Token Budget: 100-200 tokens per check
- Expected ROI: 25-250x (prevent 5-50K token waste)

### 2. test_self_check_protocol.py (740 lines)
**Tests**: Post-implementation self-verification system

**Coverage**:
- ✅ 4 Mandatory Self-Check Questions
  - "テストは全てpassしてる？"
  - "要件を全て満たしてる？"
  - "思い込みで実装してない？"
  - "証拠はある？"
- ✅ 7 Hallucination Red Flags detection
- ✅ Evidence Requirement Protocol (3-part validation)
- ✅ Token budget allocation (200/1K/2.5K by complexity)
- ✅ 94% hallucination detection rate (Reflexion benchmark)

**Key Metrics**:
- Hallucination Detection: 94% success rate
- Token Budget: 200-2,500 tokens (complexity-dependent)
- Evidence Types: Test results, code changes, validation

### 3. test_token_budget.py (590 lines)
**Tests**: Token-budget-aware reflection system

**Coverage**:
- ✅ Budget allocation by complexity
  - Simple: 200 tokens
  - Medium: 1,000 tokens
  - Complex: 2,500 tokens
- ✅ Budget compliance validation
- ✅ Savings vs unlimited reflection (80-95%)
- ✅ Monthly cost projection
- ✅ ROI calculation (40x+ return)
- ✅ Efficiency metrics

**Key Metrics**:
- Token Savings: 80-95% vs unlimited baseline
- Simple Task: 80% savings (200 vs 1,000)
- Medium Task: 80% savings (1,000 vs 5,000)
- Complex Task: 75% savings (2,500 vs 10,000)

### 4. test_reflexion_pattern.py (650 lines)
**Tests**: Self-reflection loop with memory-based error learning

**Coverage**:
- ✅ Smart error lookup (mindbase OR grep fallback)
- ✅ Past solution application (0 tokens if cached)
- ✅ Root cause investigation (WebSearch, WebFetch, Grep)
- ✅ Hypothesis formation
- ✅ Learning capture (dual storage: local + mindbase)
- ✅ Error recurrence rate (<10% target)
- ✅ Performance optimization

**Key Metrics**:
- Error Recurrence: <10% (vs 30-50% baseline)
- Token Savings: >70% with cached solutions
- Cached Lookup: 0 additional tokens (500-700 total)
- New Error Investigation: ~1,500 tokens

## Running Tests

### All Tests
```bash
pytest tests/pm_agent/ -v
```

### By Test File
```bash
pytest tests/pm_agent/test_confidence_check.py -v
pytest tests/pm_agent/test_self_check_protocol.py -v
pytest tests/pm_agent/test_token_budget.py -v
pytest tests/pm_agent/test_reflexion_pattern.py -v
```

### By Marker
```bash
pytest tests/pm_agent/ -m unit           # Unit tests only
pytest tests/pm_agent/ -m integration    # Integration tests only
pytest tests/pm_agent/ -m performance    # Performance tests only
pytest tests/pm_agent/ -m hallucination  # Hallucination detection tests only
```

### Coverage Report
```bash
pytest tests/pm_agent/ --cov=. --cov-report=html
```

## Expected Results

### Quality Metrics
```yaml
Hallucination Detection:
  Target: 94%
  Actual: [Will be validated by test suite]

Token Efficiency:
  Average Reduction: 60%
  Simple Tasks: 63% reduction
  Medium Tasks: 47% reduction
  Complex Tasks: 40% reduction

Error Recurrence:
  Target: <10%
  Baseline (without reflexion): 30-50%
  Improvement: 80% reduction

Confidence Accuracy:
  Target: >85%
  High Confidence: Proceed correctly
  Medium Confidence: Present alternatives
  Low Confidence: Ask user questions
```

### Performance Benchmarks
```yaml
Response Time:
  Confidence Check: <100ms
  Self-Check Protocol: <200ms
  Token Budget Check: <10ms
  Error Lookup (cached): <50ms
  Error Lookup (new): ~1-2 seconds (WebSearch/WebFetch)

Token Usage:
  Confidence Check: 100-200 tokens
  Self-Check Simple: 200 tokens
  Self-Check Medium: 1,000 tokens
  Self-Check Complex: 2,500 tokens
  Reflexion (cached): 500-700 tokens
  Reflexion (new): 1,500-2,000 tokens
```

## Test Architecture

```
tests/pm_agent/
├── __init__.py              # Test suite metadata
├── conftest.py              # Pytest configuration and fixtures
├── README.md                # This file
├── test_confidence_check.py # Confidence scoring (628 lines)
├── test_self_check_protocol.py # Self-verification (740 lines)
├── test_token_budget.py     # Budget management (590 lines)
└── test_reflexion_pattern.py # Error learning (650 lines)

Total: ~2,600 lines of test code
Coverage: 5 core reflection systems
```

## Integration with PM Agent

These tests validate the implementation specified in:
- `plugins/airis-agent/commands/pm.md` (Line 870-1016)
- `docs/research/reflexion-integration-2025.md`
- `docs/reference/pm-agent-autonomous-reflection.md`

## Next Steps

After test suite validation:
1. ✅ Activate metrics collection (`docs/memory/workflow_metrics.jsonl`)
2. ✅ Implement A/B testing framework (80% best, 20% experimental)
3. ✅ Performance tuning based on real-world usage data
4. ✅ Continuous optimization cycle

## Maintenance

**Test Updates Required When**:
- PM Agent specification changes (pm.md)
- New reflection systems added
- Token budget thresholds adjusted
- Hallucination detection patterns expanded

**Quality Gates**:
- All tests must pass before deployment
- Coverage >90% for reflection systems
- Performance benchmarks within spec
- Hallucination detection ≥94%
