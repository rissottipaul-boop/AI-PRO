# autonomous-dev

[![CI](https://github.com/rissottipaul-boop/AI-PRO/actions/workflows/ci.yml/badge.svg)](https://github.com/rissottipaul-boop/AI-PRO/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/rissottipaul-boop/AI-PRO/branch/main/graph/badge.svg)](https://codecov.io/gh/rissottipaul-boop/AI-PRO)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Автономная заготовка репозитория для быстрой AI-ассистируемой разработки.

## Возможности

### Базовые
- Строгий Python 3.11+ (типизация, mypy strict)
- Линтинг и автоформат (ruff + black)
- Pre-commit хуки (ruff, black, mypy, pytest)
- Тестирование (pytest + coverage, порог 85%)
- CI (GitHub Actions) — matrix (3.11, 3.12, 3.13) + отдельный security job
- Security сканы: bandit, pip-audit (HIGH), deptry
- Automation Policy (`automation_policy.yaml`)
- Dependabot (pip + actions)
- Release workflow (build + publish на PyPI по main, требует секрет `PYPI_TOKEN`)
- Makefile и PowerShell скрипт для Windows
- VSCode задачи и настройки
- ADR и архитектурная документация

### Саамообучение и производительность 🚀
- **Система метрик**: отслеживание и анализ показателей разработки
- **Анализ трендов**: автоматическое выявление паттернов и проблем
- **Генерация инсайтов**: предложения по улучшению на основе данных
- **Циклы обратной связи**: непрерывное улучшение процессов
- **Профилирование**: мониторинг производительности операций
- **Кэширование**: оптимизация дорогих вычислений
- **Батчинг и параллелизация**: эффективная обработка данных

## Быстрый старт

```bash
# (опционально) создать и активировать виртуальное окружение
python -m venv .venv
source .venv/Scripts/activate  # Windows PowerShell: ./.venv/Scripts/Activate.ps1

# Установка зависимостей (dev)
pip install .[dev]

# Запуск тестов
pytest -q

# Линт + типы
ruff check . && mypy src/autonomous_dev
```

PowerShell скрипт:

```powershell
pwsh -File scripts/dev.ps1 -All
```

Makefile (Linux/macOS):

```bash
make install
make all
```

## Pre-commit

```bash
pre-commit install
pre-commit run --all-files
```

## Структура

```text
src/autonomous_dev/        # исходный код
tests/                     # тесты
.github/workflows/ci.yml   # CI pipeline
.github/workflows/release.yml # Release pipeline
automation_policy.yaml     # Политика автономии
ARCHITECTURE.md            # Архитектура
DECISIONS/                 # ADR решения
roadmap.yaml               # Дорожная карта
.github/ISSUE_TEMPLATE/    # Шаблоны задач
```

## Автономный рабочий цикл AI

1. Анализ задач (todo) — явная фиксация шагов
2. Мелкие атомарные изменения
3. Немедленная валидация (линт/типы/тесты) локально или через задачи
4. CI (matrix + security) подтверждает корректность
5. Метрики (coverage + security) → артефакты
6. **Обратная связь**: анализ метрик, генерация инсайтов
7. **Оптимизация**: применение стратегий улучшения производительности
8. (Дальше) Автовыпуск и changelog

## Использование модулей саамообучения

```python
from autonomous_dev import MetricsTracker, FeedbackLoop, PerformanceMonitor

# Отслеживание метрик
tracker = MetricsTracker()
tracker.record_metric("test_duration", 12.5, {"suite": "integration"})

# Анализ трендов
trends = tracker.analyze_trends("test_duration")
print(f"Среднее время: {trends['mean']:.2f}s")

# Генерация инсайтов
insights = tracker.generate_insights()
for insight in insights:
    print(f"{insight.category}: {insight.description}")

# Циклы обратной связи
loop = FeedbackLoop(tracker)
suggestions = loop.suggest_optimizations({"task_type": "refactoring"})

# Мониторинг производительности
monitor = PerformanceMonitor()
monitor.record_timing("api_call", 0.5)
stats = monitor.get_stats("api_call")
```

## Политика автоматизации

Файл `automation_policy.yaml` задаёт:

- Порог покрытия: 85%
- Жёсткий линт (0 ошибок)
- Что разрешено авто-мерджить (dev deps patch, форматирование)
- Что требует ревью (public API, major bump, ADR изменения)

## Безопасность

- `bandit` — статический анализ
- `pip-audit --fail-on HIGH` — уязвимости зависимостей
- `deptry` — неиспользуемые/скрытые зависимости
- Планируемое: SBOM (cyclonedx), SAST расширение

## Обновления зависимостей

- Dependabot конфиг: еженедельные PR для pip и GitHub Actions
- Возможна интеграция Renovate (будущее)

## Релизы

Workflow `release.yml` собирает и публикует пакет при изменении `pyproject.toml` в ветке `main` (нужен секрет `PYPI_TOKEN`).

## Архитектура и ADR

- `ARCHITECTURE.md` — обзор слоёв
- `DECISIONS/ADR-0001-initial-architecture.md` — фиксация ключевых решений

## Дорожная карта

`roadmap.yaml` хранит инициативы для планирования последующих автоматизаций.

## Расширения (потенциал)

- Devcontainer + Dockerfile
- Semantic / conventional commits + автогенерация changelog
- SBOM + лицензии
- ChatOps команды (slash /qa /security)
- Performance benchmarks

## Лицензия

MIT
