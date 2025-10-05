"""Learning module for self-improving development metrics tracking."""

from __future__ import annotations

import json
import statistics
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class LearningInsight:
    """Structured insights with confidence scores.

    Attributes:
        category: Category of the insight (e.g., "performance", "quality")
        description: Human-readable description of the insight
        confidence: Confidence score between 0.0 and 1.0
        suggested_action: Recommended action to take
    """

    category: str
    description: str
    confidence: float
    suggested_action: str


@dataclass
class Metric:
    """Individual metric data point.

    Attributes:
        name: Name of the metric
        value: Numeric value of the metric
        timestamp: When the metric was recorded
        metadata: Additional metadata about the metric
    """

    name: str
    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


class MetricsTracker:
    """Tracks and analyzes development metrics for self-learning.

    Stores metrics in memory and optionally persists them to disk.
    Provides analysis capabilities including trend detection and insight generation.
    """

    def __init__(self, storage_path: Path | None = None) -> None:
        """Initialize the metrics tracker.

        Args:
            storage_path: Optional path to persist metrics to disk
        """
        self.storage_path = storage_path
        self._metrics: list[Metric] = []

        if storage_path and storage_path.exists():
            self._load_metrics()

    def record_metric(
        self,
        metric_name: str,
        value: float,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Record a new metric.

        Args:
            metric_name: Name of the metric to record
            value: Numeric value of the metric
            metadata: Optional additional metadata
        """
        metric = Metric(
            name=metric_name,
            value=value,
            metadata=metadata or {},
        )
        self._metrics.append(metric)

        if self.storage_path:
            self._save_metrics()

    def get_metrics(self, metric_name: str | None = None) -> list[Metric]:
        """Get recorded metrics.

        Args:
            metric_name: Optional name to filter metrics by

        Returns:
            List of metrics, optionally filtered by name
        """
        if metric_name is None:
            return self._metrics
        return [m for m in self._metrics if m.name == metric_name]

    def analyze_trends(self, metric_name: str, window_size: int = 5) -> dict[str, float]:
        """Analyze trends for a specific metric.

        Args:
            metric_name: Name of the metric to analyze
            window_size: Number of recent data points to analyze

        Returns:
            Dictionary with trend statistics including mean, median, and trend direction
        """
        metrics = self.get_metrics(metric_name)
        if not metrics:
            return {
                "mean": 0.0,
                "median": 0.0,
                "trend_direction": 0.0,
            }

        # Get recent values
        recent = metrics[-window_size:]
        values = [m.value for m in recent]

        # Calculate statistics
        mean_val = statistics.mean(values)
        median_val = statistics.median(values)

        # Simple trend: compare first half to second half
        if len(values) >= 2:
            mid = len(values) // 2
            first_half = statistics.mean(values[:mid]) if mid > 0 else values[0]
            second_half = statistics.mean(values[mid:])
            trend = second_half - first_half
        else:
            trend = 0.0

        return {
            "mean": mean_val,
            "median": median_val,
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
                        description="Code coverage is declining",
                        confidence=0.85,
                        suggested_action="Add tests for recent changes",
                    )
                )

        # Analyze build time
        build_metrics = self.get_metrics("build_time")
        if len(build_metrics) >= 5:
            trends = self.analyze_trends("build_time", window_size=5)
            if trends["mean"] > 300:  # 5 minutes
                insights.append(
                    LearningInsight(
                        category="performance",
                        description="Build time is consistently high",
                        confidence=0.7,
                        suggested_action="Consider build caching or parallelization",
                    )
                )

        return insights

    def _save_metrics(self) -> None:
        """Save metrics to disk."""
        if not self.storage_path:
            return

        data = [
            {
                "name": m.name,
                "value": m.value,
                "timestamp": m.timestamp.isoformat(),
                "metadata": m.metadata,
            }
            for m in self._metrics
        ]

        self.storage_path.write_text(json.dumps(data, indent=2))

    def _load_metrics(self) -> None:
        """Load metrics from disk."""
        if not self.storage_path or not self.storage_path.exists():
            return

        data = json.loads(self.storage_path.read_text())
        self._metrics = [
            Metric(
                name=item["name"],
                value=item["value"],
                timestamp=datetime.fromisoformat(item["timestamp"]),
                metadata=item.get("metadata", {}),
            )
            for item in data
        ]


class FeedbackLoop:
    """Implements feedback loop for continuous improvement."""

    def __init__(self, tracker: MetricsTracker) -> None:
        """Initialize the feedback loop.

        Args:
            tracker: MetricsTracker instance to use for analysis
        """
        self.tracker = tracker

    def evaluate_iteration(self, metrics: dict[str, float]) -> list[LearningInsight]:
        """Evaluate an iteration and generate insights.

        Args:
            metrics: Dictionary of metric names to values

        Returns:
            List of learning insights
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

        return suggestions
