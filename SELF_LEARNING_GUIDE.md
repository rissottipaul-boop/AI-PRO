# Self-Learning and Performance Optimization Guide

## Overview

This guide describes the self-learning and performance optimization capabilities added to the autonomous development system.

**Status:** 🚧 Framework documented (implementation planned)

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

- **test_duration** — Test execution time
- **coverage_percent** — Code coverage percentage
- **lint_errors** — Number of linting errors
- **build_time** — Build duration
- **memory_usage** — Memory consumption
- **api_latency** — API response time

### 2. Performance Module (`autonomous_dev/performance.py`)

The performance module provides profiling, caching, and optimization strategies.

#### Components

##### PerformanceMonitor

Global performance monitoring singleton.

```python
from autonomous_dev import PerformanceMonitor

monitor = PerformanceMonitor()

# Record operation timing
monitor.record_operation("database_query", duration=0.45)

# Get statistics
stats = monitor.get_stats("database_query")
print(f"Average: {stats['avg']}s")
print(f"Count: {stats['count']}")
print(f"Total: {stats['total']}s")
```

##### Decorators

`@timed` - Profile function execution time.

```python
from autonomous_dev import timed

@timed("my_function")
def my_function():
    # Function code
    pass

# Automatically recorded in PerformanceMonitor
```

`@cached` - LRU caching decorator.

```python
from autonomous_dev import cached

@cached(max_size=100)
def expensive_function(x, y):
    # Expensive computation
    return x + y

# First call: computed
result = expensive_function(1, 2)

# Second call: cached
result = expensive_function(1, 2)
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

### Pattern 1: Track Development Metrics

```python
from autonomous_dev import MetricsTracker

tracker = MetricsTracker(storage_path=Path("dev_metrics.json"))

# After test run
tracker.record_metric("test_duration", 15.2)

# After build
tracker.record_metric("build_time", 120.5)

# Generate insights periodically
insights = tracker.generate_insights()
for insight in insights:
    print(f"[{insight.category}] {insight.description}")
    print(f"Action: {insight.suggested_action}")
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

### Pattern 4: Feedback Loop Integration

```python
from autonomous_dev import FeedbackLoop, MetricsTracker

tracker = MetricsTracker()
loop = FeedbackLoop(tracker)

# Development iteration
def run_iteration():
    # Run tests
    test_result = run_tests()
    
    # Evaluate
    metrics = {
        "test_duration": test_result.duration,
        "coverage_percent": test_result.coverage
    }
    
    insights = loop.evaluate_iteration(metrics)
    
    # Apply suggestions
    for insight in insights:
        if insight.confidence >= 0.8:
            print(f"High-confidence action: {insight.suggested_action}")
```

## Best Practices

### 1. Metric Naming

Use consistent, descriptive names:
```python
# Good
tracker.record_metric("test_duration", 12.5)
tracker.record_metric("api_latency_users", 0.45)

# Bad
tracker.record_metric("time", 12.5)
tracker.record_metric("lat", 0.45)
```

### 2. Metadata Usage

Include relevant context:
```python
tracker.record_metric(
    "test_duration",
    12.5,
    metadata={
        "suite": "integration",
        "branch": "main",
        "python_version": "3.11"
    }
)
```

### 3. Cache Sizing

Choose appropriate cache sizes:
```python
# Small, frequently accessed data
@cached(max_size=100)
def get_user(user_id): ...

# Large, infrequently accessed data
@cached(max_size=10)
def get_report(report_id): ...
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

## Integration with CI/CD

### Recording Metrics in CI

```yaml
# .github/workflows/ci.yml
- name: Run tests
  run: |
    pytest --cov=src --junitxml=junit.xml
    python scripts/record_metrics.py --test-duration $TEST_DURATION
```

### Automated Insights

```python
# scripts/analyze_trends.py
from autonomous_dev import MetricsTracker

tracker = MetricsTracker(storage_path=Path("ci_metrics.json"))
insights = tracker.generate_insights()

for insight in insights:
    if insight.confidence >= 0.85:
        # Create GitHub issue
        create_issue(
            title=f"[Auto] {insight.category}: {insight.description}",
            body=f"Suggested action: {insight.suggested_action}"
        )
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

# L1: In-memory cache
l1_cache = SimpleCache(max_size=100)

# L2: Persistent cache (e.g., Redis)
l2_cache = RedisCache()

def get_data(key):
    # Try L1
    value = l1_cache.get(key)
    if value is not None:
        return value
    
    # Try L2
    value = l2_cache.get(key)
    if value is not None:
        l1_cache.set(key, value)
        return value
    
    # Fetch and cache
    value = fetch_from_source(key)
    l1_cache.set(key, value)
    l2_cache.set(key, value)
    return value
```

### Performance Budget

```python
from autonomous_dev import PerformanceMonitor

monitor = PerformanceMonitor()

# Set budgets
BUDGETS = {
    "api_request": 1.0,  # seconds
    "database_query": 0.5,
    "cache_lookup": 0.01
}

# Check budget
for operation, budget in BUDGETS.items():
    stats = monitor.get_stats(operation)
    if stats['avg'] > budget:
        print(f"⚠️ {operation} exceeded budget: {stats['avg']:.2f}s > {budget}s")
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

### Issue: High memory usage

**Solution:** Clear caches periodically
```python
# Clear specific cache
my_function._cache.clear()

# Or set smaller max_size
@cached(max_size=50)  # Reduced from 100
def my_function(x):
    ...
```

## Future Enhancements

- [ ] Machine learning-based trend prediction
- [ ] Distributed metrics collection
- [ ] Real-time dashboard
- [ ] Anomaly detection
- [ ] Automatic optimization application
- [ ] A/B testing framework
- [ ] Performance regression detection

## References

- [ARCHITECTURE.md](ARCHITECTURE.md) — System architecture
- [AUTOMATION_GUIDE.md](AUTOMATION_GUIDE.md) — Automation infrastructure
- [automation_policy.yaml](automation_policy.yaml) — Automation policy

---

**Status:** 📝 Documentation complete (awaiting module implementation)  
**Last Updated:** 2025-10-04  
**Next Steps:** Implement `learning.py` and `performance.py` modules
