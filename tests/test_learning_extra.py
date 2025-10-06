"""Additional tests to improve coverage for learning module edge branches."""

from __future__ import annotations

from autonomous_dev.learning import FeedbackLoop, MetricsTracker


def test_generate_insights_lint_errors_positive_mean() -> None:
    tracker = MetricsTracker()
    # Record lint errors (non-zero) to trigger mean > 0 branch
    for v in (3.0, 2.0, 1.0):
        tracker.record_metric("lint_errors", v)
    insights = tracker.generate_insights()
    assert any(
        i.category == "quality" and "Linting errors detected" in i.description for i in insights
    )


def test_generate_insights_test_failures_mean_positive() -> None:
    tracker = MetricsTracker()
    for v in (1.0, 2.0, 1.0):
        tracker.record_metric("test_failures", v)
    insights = tracker.generate_insights()
    assert any(
        i.category == "reliability" and "Test failures detected" in i.description for i in insights
    )


def test_generate_insights_build_errors_mean_positive() -> None:
    tracker = MetricsTracker()
    for v in (2.0, 1.0, 1.0):
        tracker.record_metric("build_errors", v)
    insights = tracker.generate_insights()
    assert any(
        i.category == "reliability" and "Build errors detected" in i.description for i in insights
    )


def test_feedback_loop_suggest_optimizations_debugging_complexity_and_lint() -> None:
    tracker = MetricsTracker()
    loop = FeedbackLoop(tracker)
    # Add lint errors to trigger recent linting errors suggestion (>=3 recent sum > 0)
    for v in (1.0, 0.0, 2.0):
        tracker.record_metric("lint_errors", v)
    suggestions = loop.suggest_optimizations({"task_type": "debugging", "complexity": "high"})
    categories = {s["category"] for s in suggestions}
    assert "error_handling" in categories  # from debugging/high complexity context
    # Ensure lint errors suggestion present
    assert any("lint" in str(s.get("description", "")).lower() for s in suggestions)
