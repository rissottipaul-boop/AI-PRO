# Automation Infrastructure Guide

## Overview

This repository is set up with a complete automation infrastructure for AI-assisted autonomous development. All quality gates, security checks, and deployment processes are automated.

## ✅ Current Status

All automation infrastructure is **complete and operational**:

- ✅ Tests passing (100% coverage)
- ✅ Linting clean (Ruff + Black)
- ✅ Type checking strict (mypy)
- ✅ CI/CD workflows configured
- ✅ Security scanning enabled
- ✅ Coverage reporting (Codecov)
- ✅ Release automation ready
- ✅ **Self-learning system** (metrics, feedback loops)
- ✅ **Performance optimization** (caching, profiling, batching)
- ✅ **Copilot agent instructions** (`.github/COPILOT_INSTRUCTIONS.md`)

## 🔄 Automated Workflows

### 1. Continuous Integration (`.github/workflows/ci.yml`)

**Triggers:** Every push and pull request to `main`

**Matrix Testing:** Python 3.11, 3.12, 3.13

**Steps:**

- Pre-commit hooks validation
- Linting (Ruff)
- Code formatting (Ruff format, Black)
- Type checking (mypy)
- Unit tests with coverage (pytest)
- Coverage upload to Codecov

### 2. Security Scanning (in CI workflow)

**Automated Checks:**

- `bandit` - Static security analysis
- `pip-audit` - Dependency vulnerability scanning (fails on HIGH)
- `deptry` - Unused/missing dependency detection

### 3. Release Workflow (`.github/workflows/release.yml`)

**Triggers:**

- Manual dispatch
- Push to `main` when `pyproject.toml` changes

**Actions:**

- Build Python package
- Upload artifacts
- Publish to PyPI (uses OIDC, no token needed)

## 🛠️ Local Development Tools

### Quick Commands

```bash
# Install dependencies
make install

# Run all checks
make all

# Individual checks
make lint      # Ruff + mypy
make test      # pytest with coverage
make format    # Auto-format code
```

### PowerShell (Windows)

```powershell
# Install
pwsh -File scripts/dev.ps1 -Install

# Lint
pwsh -File scripts/dev.ps1 -Lint

# Test
pwsh -File scripts/dev.ps1 -Test

# All checks
pwsh -File scripts/dev.ps1 -All
```

### Pre-commit Hooks

```bash
# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## 📊 Quality Gates

### Coverage Requirements

- **Target:** 85% minimum (configured in `pyproject.toml`)
- **Current:** 100%
- **Reporting:** Codecov integration enabled

### Lint & Format

- **Ruff:** 0 errors required
- **Black:** Consistent formatting enforced
- **Line length:** 100 characters

### Type Safety

- **mypy:** Strict mode enabled
- **Python:** 3.11+ required

## 🔐 Security Policy

### Dependency Management

- **Dependabot:** Weekly automated PR for pip and GitHub Actions
- **pip-audit:** Fails CI on HIGH severity vulnerabilities
- **bandit:** Scans for common security issues

### Safe Auto-merge Policy

Defined in `automation_policy.yaml`:

**Auto-mergeable:**

- Dev dependency patch updates
- Formatting/lint fixes
- Test-only changes

**Requires Review:**
- Public API changes
- Major version bumps
- ADR modifications
- Security policy changes

## 🎯 How AI Agent Uses This

### Autonomous Development Cycle

1. **Plan:** Analyze tasks from roadmap/issues
2. **Implement:** Make minimal, focused changes
3. **Validate:** Run local checks (lint + test)
4. **Commit:** Push changes to PR (following Conventional Commits)
5. **CI Validation:** GitHub Actions verify all checks
6. **Review:** Human review only for high-impact changes
7. **Merge:** Auto or manual merge based on policy
8. **Release:** Automatic if `pyproject.toml` version bumped

### Key Principles

- **Minimal Changes:** Only modify what's necessary
- **Iterative:** Frequent small commits with validation
- **Observable:** Coverage + CI badges show health
- **Safe:** Multiple validation layers prevent breakage
- **Self-Learning:** Track metrics and learn from patterns
- **Optimized:** Cache results and optimize operations automatically

## 📈 Metrics & Monitoring

### Status Badges

All visible in README:
- CI Status
- Code Coverage (Codecov)
- Python Version
- Code Style (Black)
- Linter (Ruff)

### Coverage Reporting

- **Local:** Coverage report in terminal after `pytest`
- **CI:** Coverage uploaded to Codecov on every build
- **Trend:** Codecov tracks coverage over time

## 🧠 Self-Learning Features

### Metrics Tracking

The system includes a `MetricsTracker` that records:

- Operation execution times
- Success/failure rates
- Performance trends over time

```python
from autonomous_dev.learning import MetricsTracker

tracker = MetricsTracker()
tracker.record_metric("cache_hit", 0.95)
tracker.record_metric("response_time", 0.023)
```

### Feedback Loops

The `FeedbackLoop` component enables:

- Analysis of performance data
- Generation of actionable insights
- Automatic strategy adjustments

```python
from autonomous_dev.learning import FeedbackLoop

loop = FeedbackLoop(tracker)
insights = loop.analyze_and_generate_insights()
# Returns LearningInsight objects with recommendations
```

### Performance Optimization

Built-in optimization strategies:

- **Caching:** Results caching with configurable TTL
- **Profiling:** Performance profiling with context managers
- **Batching:** Batch processing for bulk operations

```python
from autonomous_dev.performance import CacheManager, BatchProcessor

# Caching
cache = CacheManager()
result = cache.get_or_compute("key", lambda: expensive_operation())

# Batch processing
batch = BatchProcessor()
results = batch.process_items(items, process_function)
- **MetricsTracker**: Records and analyzes development metrics
- **Persistent storage**: Optional JSON-based metric history
- **Trend analysis**: Identifies patterns over time

### Feedback Loops
- **FeedbackLoop**: Evaluates iterations and suggests improvements
- **Confidence scores**: Each insight has a confidence level
- **Context-aware**: Adapts suggestions to task type

### Performance Optimization
- **Profiling**: `@timed` decorator tracks execution time
- **Caching**: `@cached` decorator with LRU eviction
- **Batching**: Automatic batching for large datasets
- **Parallelization**: Smart detection of when to parallelize

Example usage:
```python
from autonomous_dev import MetricsTracker, FeedbackLoop
from autonomous_dev import timed, cached

# Track metrics
tracker = MetricsTracker()
tracker.record_metric("test_duration", 12.5)

# Get insights
loop = FeedbackLoop(tracker)
suggestions = loop.suggest_optimizations({"task_type": "testing"})

# Optimize with decorators
@timed("heavy_computation")
@cached(max_size=100)
def expensive_function(x):
    return x ** 2
```

## 🚀 Next Steps (Optional Enhancements)

These are documented in `roadmap.yaml` but can be implemented:

1. **Changelog Generation**
   - Tool: `git-cliff` or `github-changelog-generator`
   - Trigger: On version bump in `pyproject.toml`

2. **Semantic Version Enforcement**
   - Script to validate version bumps match change type
   - Conventional commit → SemVer mapping

3. **Nightly/Weekly Workflows**
   - Extended security scans
   - Dependency update checks
   - Performance regression tests

4. **Enhanced Badges**
   - PyPI version badge
   - License badge
   - Download statistics

5. **Dependabot Grouping**
   - Group minor/patch updates
   - Separate major updates for review

## 📚 Documentation

- **Architecture:** `ARCHITECTURE.md` - System design and principles
- **Agent Instructions:** `.github/COPILOT_INSTRUCTIONS.md` - Complete agent contract
- **Decisions:** `DECISIONS/` - ADR (Architecture Decision Records)
- **Roadmap:** `roadmap.yaml` - Planned features and initiatives
- **Policy:** `automation_policy.yaml` - Automation rules and thresholds

## 🆘 Troubleshooting

### Common Issues

**Pre-commit fails:**

```bash
pre-commit clean
pre-commit run --all-files
```

**Tests fail:**
```bash
pytest -v  # Verbose output
pytest --lf  # Run last failed
```

**Lint errors:**
```bash
ruff check . --fix  # Auto-fix where possible
ruff format .       # Format code
```

**Type errors:**
```bash
mypy src/autonomous_dev --show-error-codes
```

### CI Failures

1. Check the specific job that failed
2. Review the error message
3. Reproduce locally with same Python version
4. Fix and push again

### Coverage Drops

If coverage falls below 85%:

1. Identify uncovered lines: `pytest --cov --cov-report=html`
2. Add tests for new code
3. Consider if certain code should be excluded (e.g., `# pragma: no cover`)

## 🎓 References

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [pytest Documentation](https://docs.pytest.org/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Codecov](https://docs.codecov.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)

---

**Status:** ✅ Infrastructure complete and operational  
**Last Updated:** 2025-10-04  
**Agent Ready:** Yes - See `.github/COPILOT_INSTRUCTIONS.md`
