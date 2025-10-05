"""Tests for the learning module."""

import json
from pathlib import Path

from autonomous_dev.learning import FeedbackLoop, LearningInsight, MetricsTracker


def test_learning_insight_creation():
    """Test creating a LearningInsight."""
    insight = LearningInsight(
        category="performance",
        description="Test execution time is increasing",
        confidence=0.8,
        suggested_action="Review test efficiency",
    )
    assert insight.category == "performance"
    assert insight.confidence == 0.8


def test_metrics_tracker_initialization():
    """Test MetricsTracker initialization."""
    tracker = MetricsTracker()
    assert tracker.get_metrics() == []


def test_metrics_tracker_record_metric():
    """Test recording metrics."""
    tracker = MetricsTracker()
    tracker.record_metric("test_duration", 10.5)

    metrics = tracker.get_metrics("test_duration")
    assert len(metrics) == 1
    assert metrics[0].name == "test_duration"
    assert metrics[0].value == 10.5


def test_metrics_tracker_record_metric_with_metadata():
    """Test recording metrics with metadata."""
    tracker = MetricsTracker()
    tracker.record_metric(
        "test_duration",
        12.5,
        metadata={"suite": "integration", "branch": "main"},
    )

    metrics = tracker.get_metrics("test_duration")
    assert metrics[0].metadata["suite"] == "integration"
    assert metrics[0].metadata["branch"] == "main"


def test_metrics_tracker_get_metrics_filtered():
    """Test filtering metrics by name."""
    tracker = MetricsTracker()
    tracker.record_metric("test_duration", 10.0)
    tracker.record_metric("coverage_percent", 85.0)
    tracker.record_metric("test_duration", 11.0)

    test_metrics = tracker.get_metrics("test_duration")
    assert len(test_metrics) == 2

    coverage_metrics = tracker.get_metrics("coverage_percent")
    assert len(coverage_metrics) == 1


def test_metrics_tracker_analyze_trends():
    """Test trend analysis."""
    tracker = MetricsTracker()

    # Record increasing values
    for i in range(10):
        tracker.record_metric("test_duration", float(10 + i))

    trends = tracker.analyze_trends("test_duration", window_size=10)
    assert trends["mean"] > 10
    assert trends["trend_direction"] > 0  # Increasing trend


def test_metrics_tracker_analyze_trends_empty():
    """Test trend analysis with no data."""
    tracker = MetricsTracker()
    trends = tracker.analyze_trends("missing_metric")

    assert trends["mean"] == 0.0
    assert trends["median"] == 0.0
    assert trends["trend_direction"] == 0.0


def test_metrics_tracker_generate_insights_test_duration():
    """Test generating insights for test duration."""
    tracker = MetricsTracker()

    # Record metrics showing increasing test duration
    for i in range(6):
        tracker.record_metric("test_duration", float(10 + i))

    insights = tracker.generate_insights()

    # Should generate insight about increasing test duration
    performance_insights = [i for i in insights if i.category == "performance"]
    assert len(performance_insights) > 0
    assert "test execution time" in performance_insights[0].description.lower()


def test_metrics_tracker_generate_insights_coverage():
    """Test generating insights for coverage."""
    tracker = MetricsTracker()

    # Record metrics showing declining coverage
    for i in range(6):
        tracker.record_metric("coverage_percent", float(90 - i * 2))

    insights = tracker.generate_insights()

    # Should generate insight about declining coverage
    quality_insights = [i for i in insights if i.category == "quality"]
    assert len(quality_insights) > 0


def test_metrics_tracker_generate_insights_build_time():
    """Test generating insights for build time."""
    tracker = MetricsTracker()

    # Record high build times
    for i in range(6):
        tracker.record_metric("build_time", 400.0 + i)

    insights = tracker.generate_insights()

    # Should generate insight about high build time
    performance_insights = [i for i in insights if i.category == "performance"]
    assert any("build time" in i.description.lower() for i in performance_insights)


def test_metrics_tracker_persistence(tmp_path: Path):
    """Test persisting metrics to disk."""
    storage_path = tmp_path / "metrics.json"

    # Create tracker and record metrics
    tracker = MetricsTracker(storage_path=storage_path)
    tracker.record_metric("test_duration", 10.0)
    tracker.record_metric("coverage_percent", 85.0)

    # Verify file was created
    assert storage_path.exists()

    # Load metrics in new tracker
    tracker2 = MetricsTracker(storage_path=storage_path)
    metrics = tracker2.get_metrics()

    assert len(metrics) == 2
    assert metrics[0].name == "test_duration"
    assert metrics[1].name == "coverage_percent"


def test_metrics_tracker_load_nonexistent(tmp_path: Path):
    """Test loading from nonexistent file."""
    storage_path = tmp_path / "nonexistent.json"
    tracker = MetricsTracker(storage_path=storage_path)

    assert tracker.get_metrics() == []


def test_feedback_loop_initialization():
    """Test FeedbackLoop initialization."""
    tracker = MetricsTracker()
    loop = FeedbackLoop(tracker)

    assert loop.tracker is tracker


def test_feedback_loop_evaluate_iteration():
    """Test evaluating an iteration."""
    tracker = MetricsTracker()
    loop = FeedbackLoop(tracker)

    insights = loop.evaluate_iteration(
        {
            "test_duration": 15.0,
            "coverage_percent": 85.0,
            "lint_errors": 0.0,
        }
    )

    # Metrics should be recorded
    assert len(tracker.get_metrics()) == 3

    # Insights should be a list
    assert isinstance(insights, list)


def test_feedback_loop_suggest_optimizations():
    """Test suggesting optimizations."""
    tracker = MetricsTracker()
    loop = FeedbackLoop(tracker)

    # Record metrics to generate insights
    for i in range(6):
        tracker.record_metric("test_duration", float(10 + i))

    suggestions = loop.suggest_optimizations(context={})

    # Should get suggestions from insights
    assert isinstance(suggestions, list)


def test_feedback_loop_suggest_optimizations_refactoring():
    """Test suggesting optimizations for refactoring context."""
    tracker = MetricsTracker()
    loop = FeedbackLoop(tracker)

    suggestions = loop.suggest_optimizations(context={"task_type": "refactoring"})

    # Should include refactoring-specific suggestion
    refactoring_suggestions = [s for s in suggestions if s["category"] == "best_practice"]
    assert len(refactoring_suggestions) > 0
    assert refactoring_suggestions[0]["priority"] == 0.9


def test_feedback_loop_high_confidence_filter():
    """Test that only high-confidence insights become suggestions."""
    tracker = MetricsTracker()
    loop = FeedbackLoop(tracker)

    # Record enough metrics to trigger insights
    for i in range(6):
        tracker.record_metric("test_duration", float(10 + i))

    suggestions = loop.suggest_optimizations(context={})

    # All suggestions should have priority >= 0.7
    for suggestion in suggestions:
        assert suggestion["priority"] >= 0.7


def test_metrics_tracker_analyze_trends_single_value():
    """Test trend analysis with single value."""
    tracker = MetricsTracker()
    tracker.record_metric("test_duration", 10.0)

    trends = tracker.analyze_trends("test_duration", window_size=5)
    assert trends["mean"] == 10.0
    assert trends["trend_direction"] == 0.0


def test_metrics_tracker_save_without_storage():
    """Test that save is no-op without storage_path."""
    tracker = MetricsTracker(storage_path=None)
    tracker.record_metric("test_duration", 10.0)
    # Should not raise an error


def test_metrics_tracker_json_serialization(tmp_path: Path):
    """Test that metrics are properly serialized to JSON."""
    storage_path = tmp_path / "metrics.json"
    tracker = MetricsTracker(storage_path=storage_path)

    tracker.record_metric("test_duration", 10.5, metadata={"branch": "main"})

    # Read and verify JSON
    data = json.loads(storage_path.read_text())
    assert len(data) == 1
    assert data[0]["name"] == "test_duration"
    assert data[0]["value"] == 10.5
    assert data[0]["metadata"]["branch"] == "main"
