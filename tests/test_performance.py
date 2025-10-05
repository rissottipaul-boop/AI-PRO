"""Tests for the performance module."""

import time

from autonomous_dev.performance import (
    OptimizationStrategy,
    PerformanceProfiler,
    SimpleCache,
    cached,
)


def test_simple_cache_initialization():
    """Test SimpleCache initialization."""
    cache = SimpleCache(max_size=10)
    assert cache.size() == 0


def test_simple_cache_set_and_get():
    """Test setting and getting cache values."""
    cache = SimpleCache(max_size=10)

    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"


def test_simple_cache_get_missing():
    """Test getting a missing key."""
    cache = SimpleCache(max_size=10)
    assert cache.get("missing") is None


def test_simple_cache_max_size():
    """Test that cache respects max_size."""
    cache = SimpleCache(max_size=3)

    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")
    cache.set("key4", "value4")  # Should evict key1

    assert cache.size() == 3
    assert cache.get("key1") is None  # Evicted
    assert cache.get("key2") == "value2"
    assert cache.get("key3") == "value3"
    assert cache.get("key4") == "value4"


def test_simple_cache_lru():
    """Test LRU eviction behavior."""
    cache = SimpleCache(max_size=2)

    cache.set("key1", "value1")
    cache.set("key2", "value2")

    # Access key1 to make it recently used
    cache.get("key1")

    # Add key3, should evict key2 (least recently used)
    cache.set("key3", "value3")

    assert cache.get("key1") == "value1"
    assert cache.get("key2") is None  # Evicted
    assert cache.get("key3") == "value3"


def test_simple_cache_update_existing():
    """Test updating an existing key."""
    cache = SimpleCache(max_size=2)

    cache.set("key1", "value1")
    cache.set("key1", "value2")  # Update

    assert cache.size() == 1
    assert cache.get("key1") == "value2"


def test_simple_cache_clear():
    """Test clearing the cache."""
    cache = SimpleCache(max_size=10)

    cache.set("key1", "value1")
    cache.set("key2", "value2")

    cache.clear()

    assert cache.size() == 0
    assert cache.get("key1") is None


def test_cached_decorator():
    """Test cached decorator basic functionality."""
    call_count = 0

    @cached(max_size=10)
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    # First call computes
    result1 = expensive_func(5)
    assert result1 == 10
    assert call_count == 1

    # Second call uses cache
    result2 = expensive_func(5)
    assert result2 == 10
    assert call_count == 1  # Not called again

    # Different argument computes
    result3 = expensive_func(10)
    assert result3 == 20
    assert call_count == 2


def test_cached_decorator_with_kwargs():
    """Test cached decorator with keyword arguments."""
    call_count = 0

    @cached(max_size=10)
    def func_with_kwargs(x: int, y: int = 1) -> int:
        nonlocal call_count
        call_count += 1
        return x + y

    result1 = func_with_kwargs(5, y=2)
    assert result1 == 7
    assert call_count == 1

    result2 = func_with_kwargs(5, y=2)
    assert result2 == 7
    assert call_count == 1  # Cached


def test_cached_decorator_cache_introspection():
    """Test that cache is accessible for introspection."""

    @cached(max_size=10)
    def func(x: int) -> int:
        return x * 2

    func(5)
    func(10)

    assert hasattr(func, "_cache")
    assert func._cache.size() == 2


def test_optimization_strategy_batch_operations():
    """Test batching operations."""
    items = list(range(25))
    batches = OptimizationStrategy.batch_operations(items, batch_size=10)

    assert len(batches) == 3
    assert len(batches[0]) == 10
    assert len(batches[1]) == 10
    assert len(batches[2]) == 5


def test_optimization_strategy_batch_operations_exact():
    """Test batching with exact division."""
    items = list(range(30))
    batches = OptimizationStrategy.batch_operations(items, batch_size=10)

    assert len(batches) == 3
    assert all(len(batch) == 10 for batch in batches)


def test_optimization_strategy_batch_operations_empty():
    """Test batching empty list."""
    items: list[int] = []
    batches = OptimizationStrategy.batch_operations(items, batch_size=10)

    assert len(batches) == 0


def test_optimization_strategy_should_parallelize():
    """Test parallelization decision."""
    assert OptimizationStrategy.should_parallelize(100, threshold=10) is True
    assert OptimizationStrategy.should_parallelize(5, threshold=10) is False
    assert OptimizationStrategy.should_parallelize(10, threshold=10) is True


def test_optimization_strategy_estimate_complexity_linear():
    """Test linear complexity estimation."""
    complexity = OptimizationStrategy.estimate_complexity(100, "linear")
    assert complexity == 100.0


def test_optimization_strategy_estimate_complexity_logarithmic():
    """Test logarithmic complexity estimation."""
    complexity = OptimizationStrategy.estimate_complexity(1024, "logarithmic")
    assert complexity == 10.0  # log2(1024) = 10


def test_optimization_strategy_estimate_complexity_quadratic():
    """Test quadratic complexity estimation."""
    complexity = OptimizationStrategy.estimate_complexity(10, "quadratic")
    assert complexity == 100.0


def test_optimization_strategy_estimate_complexity_constant():
    """Test constant complexity estimation."""
    complexity = OptimizationStrategy.estimate_complexity(1000, "constant")
    assert complexity == 1.0


def test_optimization_strategy_estimate_complexity_unknown():
    """Test unknown complexity type defaults to linear."""
    complexity = OptimizationStrategy.estimate_complexity(50, "unknown")
    assert complexity == 50.0


def test_performance_profiler_context_manager():
    """Test PerformanceProfiler as context manager."""
    with PerformanceProfiler("test_operation") as profiler:
        time.sleep(0.01)  # Small delay

    assert profiler.duration > 0.01
    assert profiler.operation_name == "test_operation"


def test_performance_profiler_get_stats():
    """Test getting profiler statistics."""
    with PerformanceProfiler("test_op") as profiler:
        time.sleep(0.01)

    stats = profiler.get_stats()

    assert stats["operation"] == "test_op"
    assert "duration_seconds" in stats
    assert "duration_ms" in stats
    assert stats["duration_seconds"] > 0
    assert stats["duration_ms"] > 0


def test_performance_profiler_multiple_operations():
    """Test profiling multiple operations."""
    durations = []

    for i in range(3):
        with PerformanceProfiler(f"operation_{i}") as profiler:
            time.sleep(0.01)
        durations.append(profiler.duration)

    assert len(durations) == 3
    assert all(d > 0 for d in durations)


def test_cached_decorator_preserves_function_name():
    """Test that cached decorator preserves function metadata."""

    @cached(max_size=10)
    def my_function(x: int) -> int:
        """This is my function."""
        return x

    assert my_function.__name__ == "my_function"
    assert "This is my function" in my_function.__doc__


def test_simple_cache_size_tracking():
    """Test that cache size is tracked correctly."""
    cache = SimpleCache(max_size=5)

    for i in range(5):
        cache.set(f"key{i}", f"value{i}")
        assert cache.size() == i + 1

    # Add one more, should stay at 5
    cache.set("key5", "value5")
    assert cache.size() == 5
