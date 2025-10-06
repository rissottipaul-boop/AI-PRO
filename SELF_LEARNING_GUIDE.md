# Self-Learning and Performance Optimization Guide

## Overview

This guide explains the self-learning and performance optimization features built into the autonomous development system. These features enable the system to learn from past iterations and continuously improve its efficiency.

## 🧠 Core Components

### 1. MetricsTracker

Tracks and analyzes development metrics over time to identify patterns and trends.

#### Features
- **Metric Recording**: Store arbitrary metrics with metadata
- **Persistent Storage**: Optional JSON-based history (file or in-memory)
- **Trend Analysis**: Identify patterns in metric changes
- **Statistical Summary**: Generate insights from historical data

#### Usage Example

```python
from autonomous_dev.learning import MetricsTracker

# Initialize tracker
tracker = MetricsTracker()

# Record metrics
tracker.record_metric("test_duration", 12.5, {"suite": "unit"})
tracker.record_metric("coverage", 95.8, {"branch": "main"})

# Get all metrics
metrics = tracker.get_metrics()

# Get specific metric
test_metrics = tracker.get_metrics(metric_name="test_duration")

# Analyze trends
trends = tracker.analyze_trends("test_duration")
# Returns: {"average": 12.5, "min": 10.2, "max": 15.3, "trend": "stable"}
```

#### Persistent Storage

```python
# Save to file
tracker = MetricsTracker(storage_path="/path/to/metrics.json")
tracker.record_metric("coverage", 96.0)
# Automatically persisted

# Load existing metrics
tracker2 = MetricsTracker(storage_path="/path/to/metrics.json")
# Loads previous metrics
```

### 2. FeedbackLoop

Evaluates iterations and generates actionable insights based on collected metrics.

#### Features
- **Iteration Evaluation**: Analyze each development iteration
- **Insight Generation**: Create actionable recommendations
- **Confidence Scoring**: Each insight has a confidence level (0.0-1.0)
- **Context-Aware**: Adapts suggestions to task type
- **Priority Ranking**: Insights sorted by importance

#### Usage Example

```python
from autonomous_dev.learning import FeedbackLoop, MetricsTracker

tracker = MetricsTracker()
loop = FeedbackLoop(tracker)

# Evaluate an iteration
metrics = {
    "test_duration": 15.2,
    "coverage": 94.5,
    "lint_errors": 0
}
insights = loop.evaluate_iteration(metrics)

# Get optimization suggestions
context = {"task_type": "testing"}
suggestions = loop.suggest_optimizations(context)

for suggestion in suggestions:
    print(f"Priority: {suggestion['priority']}")
    print(f"Action: {suggestion['description']}")
    print(f"Expected: {suggestion['expected_impact']}")
```

#### Insight Types

The system generates insights in several categories:

- **performance**: Speed and efficiency improvements
- **quality**: Code quality and maintainability
- **testing**: Test coverage and effectiveness
- **security**: Security-related recommendations
- **maintenance**: Technical debt and refactoring

### 3. PerformanceOptimizer

Applies optimization strategies to improve execution speed and resource usage.

#### Features
- **Caching**: LRU cache for expensive operations
- **Profiling**: Built-in performance monitoring
- **Batching**: Group operations for efficiency
- **Resource Management**: Optimal resource allocation

#### Usage Example

```python
from autonomous_dev.learning import PerformanceOptimizer

optimizer = PerformanceOptimizer()

# Cache expensive function results
@optimizer.cache(maxsize=128)
def expensive_operation(param):
    # Complex computation
    return result

# Profile function execution
@optimizer.profile
def monitored_function():
    # Your code
    pass

# Batch operations
items = [1, 2, 3, 4, 5]
results = optimizer.batch_process(process_func, items, batch_size=2)
```

## 📊 Metrics Categories

### Development Metrics

Track key development indicators:

```python
# Build time
tracker.record_metric("build_time", 45.2, {"target": "production"})

# Test execution
tracker.record_metric("test_duration", 12.5, {"suite": "unit"})

# Code quality
tracker.record_metric("coverage", 95.8, {"branch": "main"})
tracker.record_metric("lint_errors", 0, {"tool": "ruff"})
tracker.record_metric("type_errors", 0, {"tool": "mypy"})
```

### Performance Metrics

Monitor system performance:

```python
# Execution time
tracker.record_metric("execution_time", 0.025, {"function": "calculate_metrics"})

# Memory usage
tracker.record_metric("memory_peak_mb", 125.4, {"operation": "data_processing"})

# Cache hit rate
tracker.record_metric("cache_hit_rate", 0.85, {"cache": "lru"})
```

### Quality Metrics

Track code quality indicators:

```python
# Complexity
tracker.record_metric("cyclomatic_complexity", 5, {"module": "core"})

# Technical debt
tracker.record_metric("tech_debt_hours", 8.5, {"component": "api"})

# Documentation coverage
tracker.record_metric("doc_coverage", 92.0, {"package": "autonomous_dev"})
```

## 🎯 Learning Strategies

### 1. Pattern Recognition

The system identifies recurring patterns:

```python
# After collecting enough data (typically 5+ samples)
trends = tracker.analyze_trends("test_duration")

if trends["trend"] == "increasing":
    # Tests are getting slower
    insights = loop.suggest_optimizations({"task_type": "performance"})
```

### 2. Adaptive Thresholds

Quality gates adapt based on historical performance:

```python
# System learns optimal coverage target
coverage_history = tracker.get_metrics(metric_name="coverage")
if all(m.value >= 95.0 for m in coverage_history[-10:]):
    # Can safely raise threshold
    recommended_threshold = 95.0
```

### 3. Context-Aware Suggestions

Recommendations adapt to the current context:

```python
# Different suggestions for different task types
refactoring_suggestions = loop.suggest_optimizations({"task_type": "refactoring"})
# Focus on: code structure, duplication, maintainability

testing_suggestions = loop.suggest_optimizations({"task_type": "testing"})
# Focus on: coverage, test speed, flakiness
```

## 🚀 Performance Optimization Strategies

### 1. Caching Strategy

**When to use:**
- Expensive computations with deterministic results
- Frequently accessed data
- API calls with stable responses

**Example:**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def calculate_complexity(code_string: str) -> float:
    # Expensive analysis
    return complexity_score
```

**Best practices:**
- Use appropriate `maxsize` based on expected unique inputs
- Clear cache when underlying data changes
- Monitor cache hit rate

### 2. Batch Processing

**When to use:**
- Processing multiple similar items
- I/O operations that can be grouped
- API calls with batch endpoints

**Example:**
```python
def process_files_batch(files: list[str], batch_size: int = 10) -> list[Result]:
    results = []
    for i in range(0, len(files), batch_size):
        batch = files[i:i + batch_size]
        results.extend(process_batch(batch))
    return results
```

### 3. Profiling and Monitoring

**Always profile before optimizing:**

```python
import cProfile
import pstats

def profile_code():
    profiler = cProfile.Profile()
    profiler.enable()

    # Your code here

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 slowest functions
```

## 📈 Metrics Collection Best Practices

### 1. Consistent Naming

Use clear, consistent metric names:

```python
# Good
tracker.record_metric("test_duration_seconds", 12.5)
tracker.record_metric("coverage_percent", 95.8)

# Avoid
tracker.record_metric("time", 12.5)  # Too vague
tracker.record_metric("cov", 95.8)   # Unclear abbreviation
```

### 2. Rich Metadata

Include context in metadata:

```python
tracker.record_metric(
    "build_time",
    45.2,
    {
        "target": "production",
        "python_version": "3.12",
        "os": "linux",
        "ci": True
    }
)
```

### 3. Regular Collection

Collect metrics consistently:

```python
# In CI workflow
def collect_ci_metrics():
    start = time.time()
    run_tests()
    duration = time.time() - start

    tracker.record_metric("test_duration", duration, {"ci": True})
    tracker.record_metric("coverage", get_coverage(), {"ci": True})
```

## 🔍 Insight Interpretation

### Confidence Levels

- **0.9-1.0**: High confidence - act immediately
- **0.7-0.8**: Medium confidence - consider action
- **0.5-0.6**: Low confidence - investigate further
- **<0.5**: Very uncertain - need more data

### Priority Scoring

Insights are prioritized based on:
- Impact on quality/performance
- Ease of implementation
- Risk level
- Historical success rate

### Example Insight

```python
{
    "category": "performance",
    "description": "Test suite duration increasing steadily",
    "confidence": 0.85,
    "suggested_action": "Profile slow tests and optimize or parallelize",
    "priority": 0.9,
    "expected_impact": "30-50% reduction in test time",
    "supporting_data": {
        "trend": "increasing",
        "average": 15.2,
        "recent_samples": [14.1, 15.3, 16.2, 15.9, 16.5]
    }
}
```

## 🔧 Integration with CI/CD

### Collect Metrics in CI

```yaml
# .github/workflows/ci.yml
- name: Run tests with metrics
  run: |
    python -c "
    from autonomous_dev.learning import MetricsTracker
    import time

    tracker = MetricsTracker(storage_path='metrics.json')

    start = time.time()
    # Run tests
    duration = time.time() - start

    tracker.record_metric('test_duration', duration, {'ci': True})
    "
```

### Generate Reports

```yaml
- name: Generate insights
  run: |
    python scripts/generate_insights.py

- name: Upload metrics artifact
  uses: actions/upload-artifact@v4
  with:
    name: metrics
    path: metrics.json
```

## 📋 Implementation Checklist

Setting up self-learning in your workflow:

- [x] MetricsTracker implemented
- [x] FeedbackLoop configured
- [x] PerformanceOptimizer available
- [ ] Metrics collection in CI
- [ ] Persistent storage configured
- [ ] Insight reporting automated
- [ ] Performance baselines established
- [ ] Optimization strategies applied

## 🎓 Advanced Topics

### Custom Metrics

Define domain-specific metrics:

```python
class CustomMetricsTracker(MetricsTracker):
    def record_deployment_metric(self, success: bool, duration: float):
        self.record_metric(
            "deployment_success_rate",
            1.0 if success else 0.0,
            {"duration": duration}
        )
```

### Machine Learning Integration

Future enhancement: Use ML for predictions:

```python
# Potential future feature
predictor = MLPredictor(tracker)
predicted_duration = predictor.predict_test_duration(
    changes={"files_modified": 5, "lines_changed": 150}
)
```

## 📚 References

- **Implementation**: `src/autonomous_dev/learning.py`
- **Tests**: `tests/test_learning.py`
- **ADR**: `DECISIONS/ADR-0002-self-learning-performance.md`

---

**Status:** ✅ Implemented and tested
**Coverage:** 100%
**Last Updated:** 2025-10-04
