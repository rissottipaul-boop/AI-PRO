"""Performance optimization module with caching and profiling capabilities."""

from __future__ import annotations

import functools
import math
import time
from collections import OrderedDict
from collections.abc import Callable, Sequence
from typing import Any, TypeVar

T = TypeVar("T")


class SimpleCache:
    """Manual cache management with size limits.

    Implements an LRU (Least Recently Used) cache with a maximum size.
    """

    def __init__(self, max_size: int = 100) -> None:
        """Initialize the cache.

        Args:
            max_size: Maximum number of items to store in cache
        """
        self.max_size = max_size
        self._cache: OrderedDict[str, Any] = OrderedDict()

    def get(self, key: str) -> Any | None:
        """Get a value from the cache.

        Args:
            key: Cache key to retrieve

        Returns:
            Cached value or None if not found
        """
        if key not in self._cache:
            return None

        # Move to end (most recently used)
        self._cache.move_to_end(key)
        return self._cache[key]

    def set(self, key: str, value: Any) -> None:
        """Set a value in the cache.

        Args:
            key: Cache key to set
            value: Value to cache
        """
        if key in self._cache:
            self._cache.move_to_end(key)

        self._cache[key] = value

        # Remove oldest item if cache is full
        if len(self._cache) > self.max_size:
            self._cache.popitem(last=False)

    def clear(self) -> None:
        """Clear all cached items."""
        self._cache.clear()

    def size(self) -> int:
        """Get the current size of the cache.

        Returns:
            Number of items in cache
        """
        return len(self._cache)


def cached(max_size: int = 128) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator for caching function results.

    Args:
        max_size: Maximum number of cached results

    Returns:
        Decorated function with caching
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cache = SimpleCache(max_size=max_size)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # Create cache key from arguments
            key_parts = [str(arg) for arg in args]
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = f"{func.__name__}:{'|'.join(key_parts)}"

            # Check cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result  # type: ignore[no-any-return]

            # Compute and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result)
            return result

        # Attach cache for introspection
        wrapper._cache = cache  # type: ignore[attr-defined]
        return wrapper

    return decorator


class OptimizationStrategy:
    """Provides optimization strategies for common tasks."""

    @staticmethod
    def batch_operations(items: Sequence[T], batch_size: int = 10) -> list[list[T]]:
        """Batch operations for efficient processing.

        Args:
            items: Items to batch
            batch_size: Size of each batch

        Returns:
            List of batches
        """
        batches: list[list[T]] = []
        for i in range(0, len(items), batch_size):
            batches.append(list(items[i : i + batch_size]))
        return batches

    @staticmethod
    def should_parallelize(item_count: int, threshold: int = 10) -> bool:
        """Decide if parallelization is worth it.

        Args:
            item_count: Number of items to process
            threshold: Minimum items to justify parallelization

        Returns:
            True if parallelization is recommended
        """
        return item_count >= threshold

    @staticmethod
    def estimate_complexity(n: int, complexity_type: str = "linear") -> float:
        """Estimate computational complexity.

        Args:
            n: Input size
            complexity_type: Type of complexity (linear, logarithmic, quadratic)

        Returns:
            Estimated operations count
        """
        if complexity_type == "linear":
            return float(n)
        elif complexity_type == "logarithmic":
            return math.log2(n) if n > 0 else 0.0
        elif complexity_type == "quadratic":
            return float(n * n)
        elif complexity_type == "constant":
            return 1.0
        else:
            return float(n)  # Default to linear


class PerformanceProfiler:
    """Context manager for profiling code execution.

    Example:
        with PerformanceProfiler("my_operation") as profiler:
            # do work
            pass
        print(f"Duration: {profiler.duration}")
    """

    def __init__(self, operation_name: str) -> None:
        """Initialize the profiler.

        Args:
            operation_name: Name of the operation being profiled
        """
        self.operation_name = operation_name
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        self.duration: float = 0.0

    def __enter__(self) -> PerformanceProfiler:
        """Start profiling."""
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, *args: Any) -> None:
        """Stop profiling and calculate duration."""
        self.end_time = time.perf_counter()
        self.duration = self.end_time - self.start_time

    def get_stats(self) -> dict[str, Any]:
        """Get profiling statistics.

        Returns:
            Dictionary with profiling stats
        """
        return {
            "operation": self.operation_name,
            "duration_seconds": self.duration,
            "duration_ms": self.duration * 1000,
        }
