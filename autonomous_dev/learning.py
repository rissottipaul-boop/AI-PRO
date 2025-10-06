from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass
class MetricEntry:
    timestamp: str
    metric_name: str
    value: float
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class LearningInsight:
    category: str
    description: str
    confidence: float
    suggested_action: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class MetricsTracker:
    def __init__(self, storage_path: Path | None = None) -> None:
        self._metrics: list[MetricEntry] = []
        self._storage_path = storage_path
        if storage_path and storage_path.exists():
            try:
                data = json.loads(storage_path.read_text(encoding="utf-8"))
                for raw in data:
                    self._metrics.append(
                        MetricEntry(
                            timestamp=raw.get("timestamp", ""),
                            metric_name=raw.get("metric_name", ""),
                            value=float(raw.get("value", 0.0)),
                            metadata=raw.get("metadata", {}) or {},
                        )
                    )
            except Exception:
                # Игнорируем поврежденный файл
                pass

    def record_metric(
        self, metric_name: str, value: float, metadata: dict[str, Any] | None = None
    ) -> MetricEntry:
        # Используем timezone-aware UTC
        entry = MetricEntry(
            timestamp=datetime.now(UTC).isoformat(timespec="seconds"),
            metric_name=metric_name,
            value=float(value),
            metadata=metadata or {},
        )
        self._metrics.append(entry)
        self._save()
        return entry

    def _save(self) -> None:
        if not self._storage_path:
            return
        try:
            serialized = [m.to_dict() for m in self._metrics]
            self._storage_path.write_text(
                json.dumps(serialized, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except Exception:
            pass  # Безопасное игнорирование

    def get_metrics(self, metric_name: str | None = None) -> list[MetricEntry]:
        if metric_name is None:
            return list(self._metrics)
        return [m for m in self._metrics if m.metric_name == metric_name]

    def analyze_trends(self, metric_name: str, window_size: int = 10) -> dict[str, float]:
        data = [m.value for m in self.get_metrics(metric_name)][-window_size:]
        if not data:
            return {"mean": 0.0, "min": 0.0, "max": 0.0, "trend_direction": 0.0}
        mean_v = sum(data) / len(data)
        min_v = min(data)
        max_v = max(data)
        trend = (data[-1] - data[0]) / (len(data) - 1) if len(data) > 1 else 0.0
        return {
            "mean": mean_v,
            "min": min_v,
            "max": max_v,
            "trend_direction": trend,
        }

    def _generate_performance_insight(self) -> LearningInsight | None:
        stats = self.analyze_trends("test_duration", window_size=10)
        trend = stats["trend_direction"]
        if trend > 0.1 and len(self.get_metrics("test_duration")) >= 5:
            confidence = min(
                1.0,
                0.7 + min(0.3, abs(trend) / (stats["mean"] + 1e-6)),
            )
            description = (
                "Обнаружено увеличивающееся время выполнения тестов "
                f"(среднее {stats['mean']:.2f}, тренд растущий)."
            )
            action = "Оптимизировать узкие места тестов или параллелизовать выполнение."
            return LearningInsight(
                category="performance",
                description=description,
                confidence=confidence,
                suggested_action=action,
            )
        return None

    def _generate_quality_insight(self) -> LearningInsight | None:
        stats = self.analyze_trends("coverage_percent", window_size=10)
        trend = stats["trend_direction"]
        if trend < -0.1 and len(self.get_metrics("coverage_percent")) >= 5:
            confidence = min(
                1.0,
                0.75 + min(0.25, abs(trend) / (abs(stats["mean"]) + 1e-6)),
            )
            description = f"Понижающееся покрытие (coverage) тестами (среднее {stats['mean']:.2f})."
            action = "Добавить тесты для новых или измененных областей кода."
            return LearningInsight(
                category="quality",
                description=description,
                confidence=confidence,
                suggested_action=action,
            )
        return None

    def generate_insights(self) -> list[LearningInsight]:
        insights: list[LearningInsight] = []
        perf = self._generate_performance_insight()
        if perf:
            insights.append(perf)
        qual = self._generate_quality_insight()
        if qual:
            insights.append(qual)
        return insights


class FeedbackLoop:
    def __init__(self, tracker: MetricsTracker) -> None:
        self.tracker = tracker

    def evaluate_iteration(self, metrics: dict[str, float]) -> list[LearningInsight]:
        for name, value in metrics.items():
            self.tracker.record_metric(name, value)
        return self.tracker.generate_insights()

    def suggest_optimizations(self, context: dict[str, Any]) -> list[dict[str, Any]]:
        insights = self.tracker.generate_insights()
        suggestions: list[dict[str, Any]] = []
        for ins in insights:
            if ins.confidence >= 0.7:
                suggestions.append(
                    {
                        "description": ins.description,
                        "action": ins.suggested_action or "Исследовать причину метрики.",
                        "priority": round(ins.confidence, 2),
                        "category": ins.category,
                    }
                )
        task_type = str(context.get("task_type", "")).lower()
        if task_type == "refactoring":
            suggestions.append(
                {
                    "description": (
                        "Рекомендация для refactoring: провести модульный анализ сложных функций."
                    ),
                    "action": "Выделить высокоцикломатические участки и упростить.",
                    "priority": 0.85,
                    "category": "refactoring",
                }
            )
        # Гарантируем только high-confidence
        return [s for s in suggestions if float(s.get("priority", 0)) >= 0.7]
