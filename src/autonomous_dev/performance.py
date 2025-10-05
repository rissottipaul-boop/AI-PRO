"""Performance optimization utilities for autonomous development.

Provides profiling, caching, and optimization strategies.
"""

from __future__ import annotations

import functools
import time
from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


class PerformanceMonitor:
    """Monitors and tracks performance of operations."""

    def __init__(self) -> None:
        """Initialize performance monitor."""
        self._timings: dict[str, list[float]] = {}

    def record_timing(self, operation: str, duration: float) -> None:
        """Record timing for an operation.

        Args:
            operation: Name of the operation
            duration: Duration in seconds
        """
        if operation not in self._timings:
            self._timings[operation] = []
        self._timings[operation].append(duration)

    def get_stats(self, operation: str) -> dict[str, float]:
        """Get statistics for an operation.

        Args:
            operation: Name of the operation

        Returns:
            Dictionary with min, max, avg, total timings
        """
        if operation not in self._timings:
            return {"min": 0.0, "max": 0.0, "avg": 0.0, "total": 0.0, "count": 0.0}

        timings = self._timings[operation]
        return {
            "min": min(timings),
            "max": max(timings),
            "avg": sum(timings) / len(timings),
            "total": sum(timings),
            "count": float(len(timings)),
        }

    def get_all_stats(self) -> dict[str, dict[str, float]]:
        """Get statistics for all operations.

        Returns:
            Dictionary mapping operation names to their statistics
        """
        return {op: self.get_stats(op) for op in self._timings}


def timed(operation_name: str | None = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to time function execution.

    Args:
        operation_name: Name for the operation. If None, uses function name.

    Returns:
        Decorated function
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start

            op_name = operation_name if operation_name else func.__name__
            # Store timing information in function attribute
            if not hasattr(wrapper, "_timings"):
                wrapper._timings = []  # type: ignore[attr-defined]
            wrapper._timings.append((op_name, duration))  # type: ignore[attr-defined]

            return result

        return wrapper

    return decorator


class SimpleCache:
    """Simple in-memory cache for expensive operations."""

    def __init__(self, max_size: int = 100) -> None:
        """Initialize cache.

        Args:
            max_size: Maximum number of items to cache
        """
        self.max_size = max_size
        self._cache: dict[str, Any] = {}
        self._access_order: list[str] = []

    def get(self, key: str) -> Any | None:
        """Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        if key in self._cache:
            # Update access order
            self._access_order.remove(key)
            self._access_order.append(key)
            return self._cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        """Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        if key in self._cache:
            # Update existing
            self._access_order.remove(key)
        elif len(self._cache) >= self.max_size:
            # Evict least recently used
            lru_key = self._access_order.pop(0)
            del self._cache[lru_key]

        self._cache[key] = value
        self._access_order.append(key)

    def clear(self) -> None:
        """Clear the cache."""
        self._cache.clear()
        self._access_order.clear()

    def size(self) -> int:
        """Get current cache size.

        Returns:
            Number of items in cache
        """
        return len(self._cache)


def cached(
    max_size: int = 100,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to cache function results.

    Args:
        max_size: Maximum cache size

    Returns:
        Decorated function
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cache = SimpleCache(max_size=max_size)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # Create cache key from arguments
            key = str((args, tuple(sorted(kwargs.items()))))

            # Try to get from cache
            cached_result = cache.get(key)
            if cached_result is not None:
                # Cache stores Any, but we know it's type T from previous calls
                return cached_result  # type: ignore[no-any-return]

            # Compute and cache result
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result

        # Expose cache for testing
        wrapper._cache = cache  # type: ignore[attr-defined]
        return wrapper

    return decorator


class OptimizationStrategy:
    """Provides optimization strategies for common tasks."""

    @staticmethod
    def batch_operations(items: list[T], batch_size: int = 100) -> list[list[T]]:
        """Batch items for efficient processing.

        Args:
            items: Items to batch
            batch_size: Size of each batch

        Returns:
            List of batches
        """
        return [items[i : i + batch_size] for i in range(0, len(items), batch_size)]

    @staticmethod
    def should_parallelize(item_count: int, threshold: int = 10) -> bool:
        """Determine if operation should be parallelized.

        Args:
            item_count: Number of items to process
            threshold: Minimum items for parallelization

        Returns:
            True if parallelization is recommended
        """
        return item_count >= threshold

    @staticmethod
    def estimate_complexity(n: int, complexity_type: str = "linear") -> float:
        """Estimate computational complexity.

        Args:
            n: Input size
            complexity_type: Type of complexity (linear, quadratic, logarithmic)

        Returns:
            Estimated relative cost
        """
        if complexity_type == "linear":
            return float(n)
        elif complexity_type == "quadratic":
            return float(n * n)
        elif complexity_type == "logarithmic":
            import math

            return math.log(n) if n > 0 else 0.0
        else:
            return float(n)


__all__ = [
    "PerformanceMonitor",
    "SimpleCache",
    "OptimizationStrategy",
    "timed",
    "cached",
]
