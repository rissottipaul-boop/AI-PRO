"""Tests for the performance module."""

from __future__ import annotations

import time

from autonomous_dev.performance import (
    OptimizationStrategy,
    PerformanceMonitor,
    SimpleCache,
    cached,
    timed,
)


def test_performance_monitor_initialization() -> None:
    """Test performance monitor initialization."""
    monitor = PerformanceMonitor()
    assert monitor.get_all_stats() == {}


def test_performance_monitor_record_timing() -> None:
    """Test recording timing."""
    monitor = PerformanceMonitor()
    monitor.record_timing("test_op", 1.5)
    monitor.record_timing("test_op", 2.0)

    stats = monitor.get_stats("test_op")
    assert stats["count"] == 2.0
    assert stats["min"] == 1.5
    assert stats["max"] == 2.0
    assert stats["avg"] == 1.75
    assert stats["total"] == 3.5


def test_performance_monitor_get_stats_empty() -> None:
    """Test getting stats for non-existent operation."""
    monitor = PerformanceMonitor()
    stats = monitor.get_stats("nonexistent")
    assert stats["count"] == 0.0
    assert stats["min"] == 0.0


def test_performance_monitor_get_all_stats() -> None:
    """Test getting all statistics."""
    monitor = PerformanceMonitor()
    monitor.record_timing("op1", 1.0)
    monitor.record_timing("op2", 2.0)

    all_stats = monitor.get_all_stats()
    assert "op1" in all_stats
    assert "op2" in all_stats
    assert all_stats["op1"]["avg"] == 1.0
    assert all_stats["op2"]["avg"] == 2.0


def test_timed_decorator() -> None:
    """Test timed decorator."""

    @timed("test_function")
    def slow_function() -> int:
        time.sleep(0.01)
        return 42

    result = slow_function()
    assert result == 42
    assert hasattr(slow_function, "_timings")
    assert len(slow_function._timings) == 1  # type: ignore[attr-defined]
    assert slow_function._timings[0][0] == "test_function"  # type: ignore[attr-defined]
    assert slow_function._timings[0][1] > 0  # type: ignore[attr-defined]


def test_timed_decorator_default_name() -> None:
    """Test timed decorator with default name."""

    @timed()
    def my_function() -> str:
        return "result"

    result = my_function()
    assert result == "result"
    assert hasattr(my_function, "_timings")
    assert my_function._timings[0][0] == "my_function"  # type: ignore[attr-defined]


def test_simple_cache_initialization() -> None:
    """Test cache initialization."""
    cache = SimpleCache(max_size=10)
    assert cache.size() == 0


def test_simple_cache_get_set() -> None:
    """Test cache get and set."""
    cache = SimpleCache()
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"
    assert cache.size() == 1


def test_simple_cache_get_missing() -> None:
    """Test getting missing key."""
    cache = SimpleCache()
    assert cache.get("missing") is None


def test_simple_cache_eviction() -> None:
    """Test LRU eviction."""
    cache = SimpleCache(max_size=2)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")  # Should evict key1

    assert cache.get("key1") is None
    assert cache.get("key2") == "value2"
    assert cache.get("key3") == "value3"
    assert cache.size() == 2


def test_simple_cache_update_access_order() -> None:
    """Test that access updates order."""
    cache = SimpleCache(max_size=2)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    # Access key1 to make it recently used
    _ = cache.get("key1")
    # Add key3, should evict key2 (least recently used)
    cache.set("key3", "value3")

    assert cache.get("key1") == "value1"
    assert cache.get("key2") is None
    assert cache.get("key3") == "value3"


def test_simple_cache_update_existing() -> None:
    """Test updating existing key."""
    cache = SimpleCache()
    cache.set("key1", "value1")
    cache.set("key1", "value2")

    assert cache.get("key1") == "value2"
    assert cache.size() == 1


def test_simple_cache_clear() -> None:
    """Test clearing cache."""
    cache = SimpleCache()
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.clear()

    assert cache.size() == 0
    assert cache.get("key1") is None


def test_cached_decorator() -> None:
    """Test cached decorator."""
    call_count = 0

    @cached(max_size=10)
    def expensive_function(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    # First call
    result1 = expensive_function(5)
    assert result1 == 10
    assert call_count == 1

    # Second call with same argument (should use cache)
    result2 = expensive_function(5)
    assert result2 == 10
    assert call_count == 1  # Not called again

    # Different argument
    result3 = expensive_function(10)
    assert result3 == 20
    assert call_count == 2


def test_cached_decorator_with_kwargs() -> None:
    """Test cached decorator with keyword arguments."""
    call_count = 0

    @cached()
    def function_with_kwargs(x: int, y: int = 1) -> int:
        nonlocal call_count
        call_count += 1
        return x + y

    result1 = function_with_kwargs(5, y=2)
    result2 = function_with_kwargs(5, y=2)
    assert result1 == result2
    assert call_count == 1


def test_optimization_strategy_batch_operations() -> None:
    """Test batching operations."""
    items = list(range(25))
    batches = OptimizationStrategy.batch_operations(items, batch_size=10)

    assert len(batches) == 3
    assert len(batches[0]) == 10
    assert len(batches[1]) == 10
    assert len(batches[2]) == 5


def test_optimization_strategy_batch_operations_exact() -> None:
    """Test batching with exact divisor."""
    items = list(range(20))
    batches = OptimizationStrategy.batch_operations(items, batch_size=10)

    assert len(batches) == 2
    assert len(batches[0]) == 10
    assert len(batches[1]) == 10


def test_optimization_strategy_should_parallelize() -> None:
    """Test parallelization decision."""
    assert OptimizationStrategy.should_parallelize(5, threshold=10) is False
    assert OptimizationStrategy.should_parallelize(10, threshold=10) is True
    assert OptimizationStrategy.should_parallelize(15, threshold=10) is True


def test_optimization_strategy_estimate_complexity_linear() -> None:
    """Test linear complexity estimation."""
    complexity = OptimizationStrategy.estimate_complexity(100, "linear")
    assert complexity == 100.0


def test_optimization_strategy_estimate_complexity_quadratic() -> None:
    """Test quadratic complexity estimation."""
    complexity = OptimizationStrategy.estimate_complexity(10, "quadratic")
    assert complexity == 100.0


def test_optimization_strategy_estimate_complexity_logarithmic() -> None:
    """Test logarithmic complexity estimation."""
    complexity = OptimizationStrategy.estimate_complexity(100, "logarithmic")
    assert complexity > 0.0
    assert complexity < 10.0  # log(100) ≈ 4.6


def test_optimization_strategy_estimate_complexity_unknown() -> None:
    """Test unknown complexity type defaults to linear."""
    complexity = OptimizationStrategy.estimate_complexity(50, "unknown")
    assert complexity == 50.0
