# Self-Learning and Performance Optimization Guide

This guide explains how to use the autonomous_dev self-learning and performance optimization features.

## Overview

The autonomous_dev package provides two main modules for continuous improvement:

1. **Learning Module** (`autonomous_dev.learning`) - Tracks metrics and generates insights
2. **Performance Module** (`autonomous_dev.performance`) - Profiling and optimization tools

## Modules

### 1. Learning Module (`autonomous_dev/learning.py`)

The learning module provides metrics tracking and analysis for continuous improvement.

#### Components

##### MetricsTracker

Tracks and analyzes development metrics over time.

```python
from autonomous_dev import MetricsTracker

# Initialize tracker (in-memory)
tracker = MetricsTracker()

# Or with persistent storage
from pathlib import Path
tracker = MetricsTracker(storage_path=Path("metrics.json"))

# Record metrics
tracker.record_metric(
    metric_name="test_duration",
    value=12.5,
    metadata={"suite": "integration", "branch": "main"}
)

# Get metrics
all_metrics = tracker.get_metrics()
test_metrics = tracker.get_metrics("test_duration")

# Analyze trends
trends = tracker.analyze_trends("test_duration", window_size=10)
print(f"Mean: {trends['mean']}")
print(f"Trend: {trends['trend_direction']}")  # Positive = increasing
```

##### FeedbackLoop

Implements continuous improvement cycle.

```python
from autonomous_dev import FeedbackLoop, MetricsTracker

tracker = MetricsTracker()
loop = FeedbackLoop(tracker)

# Evaluate an iteration
insights = loop.evaluate_iteration({
    "test_duration": 15.2,
    "coverage_percent": 92.5,
    "lint_errors": 0
})

# Get optimization suggestions
suggestions = loop.suggest_optimizations(
    context={"task_type": "refactoring"}
)

for suggestion in suggestions:
    print(f"{suggestion['category']}: {suggestion['action']}")
```

##### LearningInsight

Structured insights with confidence scores.

```python
from autonomous_dev import LearningInsight

insight = LearningInsight(
    category="performance",
    description="Test execution time is increasing",
    confidence=0.8,
    suggested_action="Review test efficiency"
)
```

#### Tracked Metrics

Common metrics to track:

- `test_duration` - Test execution time
- `coverage_percent` - Code coverage percentage
- `lint_errors` - Number of linting errors
- `build_time` - Build duration
- `ci_duration` - CI pipeline duration
- `memory_usage` - Memory consumption
- Custom metrics as needed

### 2. Performance Module (`autonomous_dev/performance.py`)

The performance module provides profiling, caching, and optimization strategies.

#### Components

##### PerformanceProfiler

Context manager for timing operations.

```python
from autonomous_dev import PerformanceProfiler

with PerformanceProfiler("data_processing") as profiler:
    # Do expensive work
    process_data()

print(f"Took {profiler.duration:.2f} seconds")
stats = profiler.get_stats()
# {'operation': 'data_processing', 'duration_seconds': 1.23, 'duration_ms': 1230}
```

##### SimpleCache

Manual cache management.

```python
from autonomous_dev import SimpleCache

cache = SimpleCache(max_size=100)

# Set values
cache.set("key1", "value1")

# Get values
value = cache.get("key1")  # Returns "value1"
value = cache.get("missing")  # Returns None

# Clear cache
cache.clear()
```

##### cached decorator

Automatic function result caching.

```python
from autonomous_dev import cached

@cached(max_size=100)
def expensive_computation(n: int) -> int:
    return n ** 2

# First call computes
result = expensive_computation(10)  # Computed

# Second call uses cache
result = expensive_computation(10)  # Cached

# Check cache size
print(expensive_computation._cache.size())
```

##### OptimizationStrategy

Provides optimization strategies for common tasks.

```python
from autonomous_dev import OptimizationStrategy

# Batch operations
items = list(range(100))
batches = OptimizationStrategy.batch_operations(items, batch_size=10)
# Returns: [[0-9], [10-19], ..., [90-99]]

# Decide if parallelization is worth it
should_parallelize = OptimizationStrategy.should_parallelize(
    item_count=100,
    threshold=10
)  # Returns: True

# Estimate computational complexity
complexity = OptimizationStrategy.estimate_complexity(
    n=1000,
    complexity_type="logarithmic"
)  # Returns: ~6.9
```

## Usage Patterns

### Pattern 1: Continuous Monitoring

Track metrics over time and generate insights:

```python
from pathlib import Path
from autonomous_dev import MetricsTracker

tracker = MetricsTracker(storage_path=Path(".metrics.json"))

# During each CI run
tracker.record_metric("test_duration", 45.2)
tracker.record_metric("coverage_percent", 87.5)

# Periodically check for insights
insights = tracker.generate_insights()
for insight in insights:
    if insight.confidence >= 0.8:
        print(f"⚠️  {insight.description}")
        print(f"   Action: {insight.suggested_action}")
```

### Pattern 2: Performance Optimization

Profile and optimize expensive operations:

```python
from autonomous_dev import PerformanceProfiler, cached, OptimizationStrategy

# Profile current performance
with PerformanceProfiler("batch_process") as profiler:
    for item in large_list:
        process(item)

if profiler.duration > 60:  # More than 1 minute
    # Optimize with batching
    batches = OptimizationStrategy.batch_operations(large_list, batch_size=100)
    
    for batch in batches:
        process_batch(batch)

# Cache expensive computations
@cached(max_size=500)
def compute_hash(data: str) -> str:
    # Expensive operation
    return hashlib.sha256(data.encode()).hexdigest()
```

### Pattern 3: Batch Processing

Optimize batch operations:

```python
from autonomous_dev import OptimizationStrategy

items = fetch_work_items()  # 1000 items

if OptimizationStrategy.should_parallelize(len(items), threshold=50):
    # Use parallel processing
    batches = OptimizationStrategy.batch_operations(items, batch_size=100)
    
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        results = executor.map(process_batch, batches)
else:
    # Process sequentially
    results = [process_item(item) for item in items]
```

## Integration with CI/CD

### In GitHub Actions

```yaml
- name: Track CI Metrics
  run: |
    python -c "
    from autonomous_dev import MetricsTracker
    tracker = MetricsTracker(storage_path='ci_metrics.json')
    tracker.record_metric('ci_duration', ${{ steps.test.outputs.duration }})
    tracker.record_metric('coverage', ${{ steps.coverage.outputs.percent }})
    "
```

### Pre-commit Hook

```python
# .git/hooks/pre-commit
from autonomous_dev import MetricsTracker

tracker = MetricsTracker(storage_path=".metrics.json")
# Record pre-commit metrics
tracker.record_metric("commits_per_day", 1)
```

## Best Practices

### 1. Metric Naming

Use consistent, descriptive names:

- ✅ `test_duration`, `coverage_percent`, `build_time`
- ❌ `t1`, `c`, `bt`

### 2. Metadata Usage

Include context with metrics:

```python
tracker.record_metric(
    "test_duration",
    45.2,
    metadata={
        "suite": "integration",
        "branch": "main",
        "commit": "abc123"
    }
)
```

### 3. Cache Sizing

Choose appropriate cache sizes:

```python
# Small, frequently used data
@cached(max_size=50)
def get_config(key: str) -> str:
    pass

# Large dataset, infrequent access
@cached(max_size=1000)
def expensive_query(params: dict) -> list:
    pass
```

### 4. Performance Thresholds

Define clear thresholds in automation policy:

```yaml
performance:
  test_duration_max: 60  # seconds
  build_time_max: 300    # seconds
  cache_size: 100        # items
```

### 5. Insight Confidence

Act on high-confidence insights:

```python
insights = tracker.generate_insights()
for insight in insights:
    if insight.confidence >= 0.8:  # 80%+ confidence
        # Take action
        apply_optimization(insight.suggested_action)
```

## Advanced Topics

### Custom Insight Rules

Extend `MetricsTracker.generate_insights()`:

```python
class CustomMetricsTracker(MetricsTracker):
    def generate_insights(self):
        insights = super().generate_insights()
        
        # Add custom rule
        memory_metrics = self.get_metrics("memory_usage")
        if len(memory_metrics) >= 5:
            trends = self.analyze_trends("memory_usage")
            if trends["mean"] > 1000:  # MB
                insights.append(
                    LearningInsight(
                        category="resource",
                        description="High memory usage detected",
                        confidence=0.85,
                        suggested_action="Profile memory usage"
                    )
                )
        
        return insights
```

### Multi-Level Caching

Combine in-memory and persistent caching:

```python
from autonomous_dev import SimpleCache
import pickle

class PersistentCache(SimpleCache):
    def __init__(self, max_size: int, cache_file: Path):
        super().__init__(max_size)
        self.cache_file = cache_file
        self._load()
    
    def _load(self):
        if self.cache_file.exists():
            self._cache = pickle.loads(self.cache_file.read_bytes())
    
    def set(self, key: str, value: Any) -> None:
        super().set(key, value)
        self.cache_file.write_bytes(pickle.dumps(self._cache))
```

## Troubleshooting

### Issue: Metrics not persisting

**Solution:** Ensure storage path is writable

```python
tracker = MetricsTracker(storage_path=Path("metrics.json"))
# Check: metrics.json file should be created
```

### Issue: Cache not improving performance

**Solution:** Check cache hit rate

```python
@cached(max_size=100)
def my_function(x):
    return x * 2

# Verify cache is working
cache = my_function._cache
print(f"Cache size: {cache.size()}")
```

### Issue: No insights generated

**Solution:** Need more data

```python
# Insights require minimum data points
for i in range(10):  # Generate at least 5-10 data points
    tracker.record_metric("test_duration", float(10 + i))

insights = tracker.generate_insights()
```

## Examples

### Complete Workflow Example

```python
from pathlib import Path
from autonomous_dev import (
    MetricsTracker,
    FeedbackLoop,
    PerformanceProfiler,
    cached
)

# Initialize
tracker = MetricsTracker(storage_path=Path("metrics.json"))
loop = FeedbackLoop(tracker)

# Profile operation
with PerformanceProfiler("test_suite") as profiler:
    run_tests()

# Record metrics
metrics = {
    "test_duration": profiler.duration,
    "coverage_percent": get_coverage(),
    "lint_errors": count_lint_errors()
}

# Get insights and suggestions
insights = loop.evaluate_iteration(metrics)
suggestions = loop.suggest_optimizations({"task_type": "testing"})

# Apply optimizations
for suggestion in suggestions:
    if suggestion["priority"] > 0.8:
        print(f"High priority: {suggestion['action']}")
```

## References

- [Project Architecture](ARCHITECTURE.md)
- [Automation Guide](AUTOMATION_GUIDE.md)
- [Automation Policy](automation_policy.yaml)

---

**Last Updated:** 2025-10-04
