# Self-Learning and Performance Optimization Guide

## Overview

This guide describes the self-learning and performance optimization capabilities added to the autonomous development system.

## Modules

### 1. Learning Module (`autonomous_dev/learning.py`)

The learning module provides self-improvement capabilities through metrics tracking, trend analysis, and insight generation.

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

Implements continuous improvement through feedback loops.

```python
from autonomous_dev import FeedbackLoop, MetricsTracker

tracker = MetricsTracker()
loop = FeedbackLoop(tracker)

# Evaluate an iteration
metrics = {
    "test_duration": 12.5,
    "coverage_percent": 95.0,
    "lint_errors": 0
}
insights = loop.evaluate_iteration(metrics)

# Get optimization suggestions
suggestions = loop.suggest_optimizations({
    "task_type": "refactoring",
    "complexity": "high"
})

for suggestion in suggestions:
    print(f"{suggestion['category']}: {suggestion['action']}")
    print(f"Priority: {suggestion['priority']}")
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

##### PerformanceMonitor

Monitors and tracks operation performance.

```python
from autonomous_dev import PerformanceMonitor

monitor = PerformanceMonitor()

# Record timings
monitor.record_timing("api_call", 0.5)
monitor.record_timing("api_call", 0.6)

# Get statistics
stats = monitor.get_stats("api_call")
print(f"Average: {stats['avg']}")
print(f"Count: {stats['count']}")

# Get all stats
all_stats = monitor.get_all_stats()
```

##### Decorators

###### @timed

Profile function execution time.

```python
from autonomous_dev import timed

@timed("data_processing")
def process_data(data):
    # ... processing logic
    return result

# Function execution time is automatically tracked
result = process_data(my_data)
```

###### @cached

Cache function results with LRU eviction.

```python
from autonomous_dev import cached

@cached(max_size=100)
def expensive_calculation(x, y):
    # Expensive computation
    return x * y

# First call - computes result
result1 = expensive_calculation(10, 20)  # Cache miss

# Second call - returns cached result
result2 = expensive_calculation(10, 20)  # Cache hit - much faster!
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

```python
from autonomous_dev import MetricsTracker, FeedbackLoop
from pathlib import Path

# Setup
tracker = MetricsTracker(storage_path=Path("metrics.json"))
loop = FeedbackLoop(tracker)

# In your development workflow
def run_tests():
    start = time.time()
    # Run tests
    duration = time.time() - start
    
    # Record metrics
    tracker.record_metric("test_duration", duration)
    
    # Get insights
    insights = tracker.generate_insights()
    for insight in insights:
        if insight.confidence >= 0.8:
            print(f"⚠️  {insight.description}")
            print(f"💡 {insight.suggested_action}")
```

### Pattern 2: Performance Optimization

```python
from autonomous_dev import timed, cached, PerformanceMonitor

monitor = PerformanceMonitor()

@timed("api_request")
@cached(max_size=50)
def fetch_data(endpoint):
    # Expensive API call
    response = requests.get(endpoint)
    return response.json()

# Use normally - automatically profiled and cached
data = fetch_data("/api/users")

# Check performance
stats = monitor.get_stats("api_request")
if stats['avg'] > 1.0:
    print("Warning: API calls are slow")
```

### Pattern 3: Batch Processing

```python
from autonomous_dev import OptimizationStrategy

def process_items(items):
    # Decide on strategy
    if OptimizationStrategy.should_parallelize(len(items)):
        # Process in parallel
        batches = OptimizationStrategy.batch_operations(items, batch_size=100)
        results = process_in_parallel(batches)
    else:
        # Process sequentially
        results = [process_item(item) for item in items]
    
    return results
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
- `test_duration` ✅ not `time` ❌
- `coverage_percent` ✅ not `cov` ❌
- `build_time_seconds` ✅ not `build` ❌

### 2. Metadata Usage

Include relevant context:
```python
tracker.record_metric(
    "test_duration",
    12.5,
    metadata={
        "suite": "integration",
        "branch": "feature/new-api",
        "ci": "github-actions",
        "python_version": "3.12"
    }
)
```

### 3. Cache Sizing

Size caches appropriately:
- Small datasets: 10-50 items
- Medium datasets: 100-500 items
- Large datasets: Consider external caching (Redis, Memcached)

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

```python
from autonomous_dev import SimpleCache

# L1: Small, fast cache
l1_cache = SimpleCache(max_size=10)

# L2: Larger cache
l2_cache = SimpleCache(max_size=100)

def get_data(key):
    # Try L1
    result = l1_cache.get(key)
    if result is not None:
        return result
    
    # Try L2
    result = l2_cache.get(key)
    if result is not None:
        l1_cache.set(key, result)  # Promote to L1
        return result
    
    # Compute
    result = expensive_computation(key)
    l1_cache.set(key, result)
    l2_cache.set(key, result)
    return result
```

## Future Enhancements

- ML-based predictions for metrics
- Distributed metrics collection
- Real-time dashboards
- Automated optimization application
- A/B testing framework
- Regression detection

## References

- [Architecture Documentation](ARCHITECTURE.md)
- [ADR-0002: Self-Learning System](DECISIONS/ADR-0002-self-learning-performance.md)
- [Automation Policy](automation_policy.yaml)
- [Roadmap](roadmap.yaml)

---

**Last Updated:** 2025-10-04  
**Version:** 1.0.0
