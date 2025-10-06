"""Tests for the learning module."""

from __future__ import annotations

import tempfile
from pathlib import Path

from autonomous_dev.learning import FeedbackLoop, LearningInsight, MetricEntry, MetricsTracker


def test_metric_entry_creation() -> None:
    """Test creating a metric entry."""
    entry = MetricEntry(
        timestamp="2025-01-01T00:00:00",
        metric_name="test_metric",
        value=42.0,
        metadata={"source": "test"},
    )
    assert entry.metric_name == "test_metric"
    assert entry.value == 42.0
    assert entry.metadata["source"] == "test"


def test_metric_entry_to_dict() -> None:
    """Test converting metric entry to dictionary."""
    entry = MetricEntry(
        timestamp="2025-01-01T00:00:00",
        metric_name="test_metric",
        value=42.0,
        metadata={},
    )
    entry_dict = entry.to_dict()
    assert entry_dict["metric_name"] == "test_metric"
    assert entry_dict["value"] == 42.0


def test_learning_insight_creation() -> None:
    """Test creating a learning insight."""
    insight = LearningInsight(
        category="performance",
        description="Test insight",
        confidence=0.9,
        suggested_action="Do something",
    )
    assert insight.category == "performance"
    assert insight.confidence == 0.9


def test_metrics_tracker_initialization() -> None:
    """Test metrics tracker initialization."""
    tracker = MetricsTracker()
    assert tracker.get_metrics() == []


def test_metrics_tracker_record_metric() -> None:
    """Test recording a metric."""
    tracker = MetricsTracker()
    tracker.record_metric("coverage", 95.5, {"branch": "main"})

    metrics = tracker.get_metrics()
    assert len(metrics) == 1
    assert metrics[0].metric_name == "coverage"
    assert metrics[0].value == 95.5
    assert metrics[0].metadata["branch"] == "main"


def test_metrics_tracker_get_filtered_metrics() -> None:
    """Test filtering metrics by name."""
    tracker = MetricsTracker()
    tracker.record_metric("coverage", 95.0)
    tracker.record_metric("test_duration", 10.5)
    tracker.record_metric("coverage", 96.0)

    coverage_metrics = tracker.get_metrics("coverage")
    assert len(coverage_metrics) == 2
    assert all(m.metric_name == "coverage" for m in coverage_metrics)


def test_metrics_tracker_analyze_trends() -> None:
    """Test trend analysis."""
    tracker = MetricsTracker()
    # Record increasing values
    for i in range(10):
        tracker.record_metric("test_duration", float(i))

    trends = tracker.analyze_trends("test_duration", window_size=10)
    assert trends["mean"] == 4.5
    assert trends["min"] == 0.0
    assert trends["max"] == 9.0
    assert trends["trend_direction"] > 0  # Increasing trend


def test_metrics_tracker_analyze_trends_empty() -> None:
    """Test trend analysis with no data."""
    tracker = MetricsTracker()
    trends = tracker.analyze_trends("nonexistent")
    assert trends["mean"] == 0.0
    assert trends["min"] == 0.0
    assert trends["max"] == 0.0


def test_metrics_tracker_generate_insights_performance() -> None:
    """Test generating performance insights."""
    tracker = MetricsTracker()
    # Record increasing test durations
    for i in range(6):
        tracker.record_metric("test_duration", float(10 + i))

    insights = tracker.generate_insights()
    # Should detect increasing test duration
    performance_insights = [i for i in insights if i.category == "performance"]
    assert len(performance_insights) > 0
    assert "increasing" in performance_insights[0].description.lower()


def test_metrics_tracker_generate_insights_quality() -> None:
    """Test generating quality insights."""
    tracker = MetricsTracker()
    # Record decreasing coverage
    for i in range(6):
        tracker.record_metric("coverage_percent", float(95 - i * 2))

    insights = tracker.generate_insights()
    # Should detect decreasing coverage
    quality_insights = [i for i in insights if i.category == "quality"]
    assert len(quality_insights) > 0
    assert "coverage" in quality_insights[0].description.lower()


def test_metrics_tracker_persistence() -> None:
    """Test saving and loading metrics."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "metrics.json"

        # Create and save metrics
        tracker1 = MetricsTracker(storage_path=storage_path)
        tracker1.record_metric("coverage", 95.0)
        tracker1.record_metric("test_duration", 10.5)

        # Load metrics in new tracker
        tracker2 = MetricsTracker(storage_path=storage_path)
        metrics = tracker2.get_metrics()
        assert len(metrics) == 2
        assert metrics[0].metric_name == "coverage"
        assert metrics[1].metric_name == "test_duration"


def test_feedback_loop_initialization() -> None:
    """Test feedback loop initialization."""
    tracker = MetricsTracker()
    loop = FeedbackLoop(tracker)
    assert loop.tracker is tracker


def test_feedback_loop_evaluate_iteration() -> None:
    """Test evaluating an iteration."""
    tracker = MetricsTracker()
    loop = FeedbackLoop(tracker)

    metrics = {"coverage": 95.0, "test_duration": 10.5}
    insights = loop.evaluate_iteration(metrics)

    # Metrics should be recorded
    assert len(tracker.get_metrics()) == 2
    # Insights may be empty if not enough data
    assert isinstance(insights, list)


def test_feedback_loop_suggest_optimizations() -> None:
    """Test suggesting optimizations."""
    tracker = MetricsTracker()
    loop = FeedbackLoop(tracker)

    # Generate some data for insights
    for i in range(6):
        tracker.record_metric("test_duration", float(10 + i))

    suggestions = loop.suggest_optimizations({"task_type": "testing"})
    assert isinstance(suggestions, list)


def test_feedback_loop_suggest_optimizations_refactoring() -> None:
    """Test suggesting optimizations for refactoring."""
    tracker = MetricsTracker()
    loop = FeedbackLoop(tracker)

    suggestions = loop.suggest_optimizations({"task_type": "refactoring"})
    assert len(suggestions) > 0
    # Should include refactoring-specific suggestion
    assert any("refactoring" in str(s["description"]).lower() for s in suggestions)


def test_feedback_loop_high_confidence_suggestions() -> None:
    """Test that only high-confidence suggestions are included."""
    tracker = MetricsTracker()
    loop = FeedbackLoop(tracker)

    # Generate data that will create insights
    for i in range(6):
        tracker.record_metric("test_duration", float(10 + i))

    suggestions = loop.suggest_optimizations({})
    # All suggestions should have high confidence
    for suggestion in suggestions:
        priority = suggestion.get("priority", 0)
        assert isinstance(priority, (int, float)) and priority >= 0.5
