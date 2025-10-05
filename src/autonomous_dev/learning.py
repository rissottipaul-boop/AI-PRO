"""Self-learning module for autonomous development system.

Tracks metrics, analyzes patterns, and provides feedback for continuous improvement.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class MetricEntry:
    """Single metric entry with timestamp."""

    timestamp: str
    metric_name: str
    value: float
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class LearningInsight:
    """Insight derived from metrics analysis."""

    category: str
    description: str
    confidence: float
    suggested_action: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class MetricsTracker:
    """Tracks and analyzes development metrics for self-learning."""

    def __init__(self, storage_path: Path | None = None) -> None:
        """Initialize metrics tracker.

        Args:
            storage_path: Path to store metrics data. If None, uses in-memory storage.
        """
        self.storage_path = storage_path
        self._metrics: list[MetricEntry] = []
        if storage_path and storage_path.exists():
            self._load_metrics()

    def record_metric(
        self, metric_name: str, value: float, metadata: dict[str, Any] | None = None
    ) -> None:
        """Record a new metric.

        Args:
            metric_name: Name of the metric (e.g., 'test_duration', 'coverage_percent')
            value: Numeric value of the metric
            metadata: Optional metadata about the metric
        """
        entry = MetricEntry(
            timestamp=datetime.now().isoformat(),
            metric_name=metric_name,
            value=value,
            metadata=metadata or {},
        )
        self._metrics.append(entry)
        if self.storage_path:
            self._save_metrics()

    def get_metrics(self, metric_name: str | None = None) -> list[MetricEntry]:
        """Get recorded metrics.

        Args:
            metric_name: If provided, filter by this metric name

        Returns:
            List of metric entries
        """
        if metric_name is None:
            return self._metrics.copy()
        return [m for m in self._metrics if m.metric_name == metric_name]

    def analyze_trends(self, metric_name: str, window_size: int = 10) -> dict[str, float]:
        """Analyze trends for a specific metric.

        Args:
            metric_name: Name of the metric to analyze
            window_size: Number of recent entries to analyze

        Returns:
            Dictionary with trend analysis (mean, min, max, trend_direction)
        """
        metrics = self.get_metrics(metric_name)[-window_size:]
        if not metrics:
            return {"mean": 0.0, "min": 0.0, "max": 0.0, "trend_direction": 0.0}

        values = [m.value for m in metrics]
        mean_val = sum(values) / len(values)
        min_val = min(values)
        max_val = max(values)

        # Calculate trend direction (positive = improving, negative = degrading)
        trend = 0.0
        if len(values) >= 2:
            mid_point = len(values) // 2
            first_half_avg = sum(values[:mid_point]) / mid_point
            second_half_avg = sum(values[mid_point:]) / (len(values) - mid_point)
            trend = second_half_avg - first_half_avg

        return {
            "mean": mean_val,
            "min": min_val,
            "max": max_val,
            "trend_direction": trend,
        }

    def generate_insights(self) -> list[LearningInsight]:
        """Generate actionable insights from metrics.

        Returns:
            List of learning insights
        """
        insights: list[LearningInsight] = []

        # Analyze test performance
        test_metrics = self.get_metrics("test_duration")
        if len(test_metrics) >= 5:
            trends = self.analyze_trends("test_duration", window_size=5)
            if trends["trend_direction"] > 0.5:
                insights.append(
                    LearningInsight(
                        category="performance",
                        description="Test execution time is increasing",
                        confidence=0.8,
                        suggested_action="Review test efficiency and consider optimization",
                    )
                )

        # Analyze coverage trends
        coverage_metrics = self.get_metrics("coverage_percent")
        if len(coverage_metrics) >= 5:
            trends = self.analyze_trends("coverage_percent", window_size=5)
            if trends["trend_direction"] < -2.0:
                insights.append(
                    LearningInsight(
                        category="quality",
                        description="Code coverage is decreasing",
                        confidence=0.9,
                        suggested_action="Add tests for recent changes to maintain quality",
                    )
                )

        # Analyze error trends
        error_metrics = self.get_metrics("lint_errors")
        if len(error_metrics) >= 3:
            trends = self.analyze_trends("lint_errors", window_size=3)
            if trends["mean"] > 0:
                insights.append(
                    LearningInsight(
                        category="quality",
                        description="Linting errors detected",
                        confidence=0.95,
                        suggested_action="Fix linting errors to maintain code quality standards",
                    )
                )
            elif trends["trend_direction"] > 0.5:
                insights.append(
                    LearningInsight(
                        category="quality",
                        description="Linting errors are increasing",
                        confidence=0.85,
                        suggested_action="Review recent changes and address code quality issues",
                    )
                )

        # Analyze test failure trends
        test_failure_metrics = self.get_metrics("test_failures")
        if len(test_failure_metrics) >= 3:
            trends = self.analyze_trends("test_failures", window_size=3)
            if trends["mean"] > 0:
                insights.append(
                    LearningInsight(
                        category="reliability",
                        description="Test failures detected",
                        confidence=0.95,
                        suggested_action="Investigate and fix failing tests immediately",
                    )
                )
            elif trends["trend_direction"] > 0.5:
                insights.append(
                    LearningInsight(
                        category="reliability",
                        description="Test failure rate is increasing",
                        confidence=0.85,
                        suggested_action="Review test stability and fix flaky tests",
                    )
                )

        # Analyze build error trends
        build_error_metrics = self.get_metrics("build_errors")
        if len(build_error_metrics) >= 3:
            trends = self.analyze_trends("build_errors", window_size=3)
            if trends["mean"] > 0:
                insights.append(
                    LearningInsight(
                        category="reliability",
                        description="Build errors detected",
                        confidence=0.95,
                        suggested_action="Fix build errors to restore system stability",
                    )
                )

        return insights

    def _save_metrics(self) -> None:
        """Save metrics to storage."""
        if not self.storage_path:
            return
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with self.storage_path.open("w") as f:
            json.dump([m.to_dict() for m in self._metrics], f, indent=2)

    def _load_metrics(self) -> None:
        """Load metrics from storage."""
        if not self.storage_path or not self.storage_path.exists():
            return
        with self.storage_path.open("r") as f:
            data = json.load(f)
            self._metrics = [
                MetricEntry(
                    timestamp=m["timestamp"],
                    metric_name=m["metric_name"],
                    value=m["value"],
                    metadata=m["metadata"],
                )
                for m in data
            ]


class FeedbackLoop:
    """Implements feedback loop for continuous improvement."""

    def __init__(self, tracker: MetricsTracker) -> None:
        """Initialize feedback loop.

        Args:
            tracker: Metrics tracker to use for analysis
        """
        self.tracker = tracker

    def evaluate_iteration(self, metrics: dict[str, float]) -> list[LearningInsight]:
        """Evaluate a development iteration.

        Args:
            metrics: Dictionary of metric names to values

        Returns:
            List of insights for improvement
        """
        # Record all metrics
        for name, value in metrics.items():
            self.tracker.record_metric(name, value)

        # Generate insights
        return self.tracker.generate_insights()

    def suggest_optimizations(self, context: dict[str, Any]) -> Sequence[dict[str, str | float]]:
        """Suggest optimizations based on context.

        Args:
            context: Context information (e.g., task type, complexity)

        Returns:
            List of optimization suggestions
        """
        suggestions: list[dict[str, str | float]] = []
        insights = self.tracker.generate_insights()

        for insight in insights:
            if insight.confidence >= 0.7:
                suggestions.append(
                    {
                        "category": insight.category,
                        "description": insight.description,
                        "action": insight.suggested_action,
                        "priority": insight.confidence,
                    }
                )

        # Add context-specific suggestions
        if context.get("task_type") == "refactoring":
            suggestions.append(
                {
                    "category": "best_practice",
                    "description": "Refactoring task detected",
                    "action": "Ensure test coverage remains high after changes",
                    "priority": 0.9,
                }
            )

        # Add error-handling suggestions for debugging tasks
        if context.get("task_type") == "debugging":
            suggestions.append(
                {
                    "category": "error_handling",
                    "description": "Debugging task detected",
                    "action": "Add comprehensive error logging and track error metrics",
                    "priority": 0.85,
                }
            )

        # Add error prevention suggestions for high complexity tasks
        if context.get("complexity") == "high":
            suggestions.append(
                {
                    "category": "error_handling",
                    "description": "High complexity task detected",
                    "action": "Implement robust error handling and validation",
                    "priority": 0.8,
                }
            )

        # Add suggestions based on error history
        error_metrics = self.tracker.get_metrics("lint_errors")
        if error_metrics and len(error_metrics) >= 3:
            recent_errors = sum(m.value for m in error_metrics[-3:])
            if recent_errors > 0:
                suggestions.append(
                    {
                        "category": "error_handling",
                        "description": "Recent linting errors detected",
                        "action": "Run automated linting and fix issues before commit",
                        "priority": 0.9,
                    }
                )

        return suggestions


__all__ = ["MetricsTracker", "FeedbackLoop", "MetricEntry", "LearningInsight"]
