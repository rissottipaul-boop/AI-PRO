# autonomous-dev

[![CI](https://github.com/rissottipaul-boop/AI-PRO/actions/workflows/ci.yml/badge.svg)](https://github.com/rissottipaul-boop/AI-PRO/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
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
- Release workflow (build + publish на PyPI по main, OIDC без токенов)
- Makefile и PowerShell скрипт для Windows
- VSCode задачи и настройки
- ADR и архитектурная документация

### Автономная разработка 🤖
- **Copilot Instructions** (`.github/COPILOT_INSTRUCTIONS.md`) — полное руководство для AI агентов
- **Agent Task Template** — структурированные задачи для автономного выполнения
- **Conventional Commits** — стандартизированная история изменений
- **Automated Quality Gates** — многоуровневая валидация без ручного контроля

### Саамообучение и производительность 🚀
- **MetricsTracker** — сбор и анализ метрик разработки
- **FeedbackLoop** — генерация инсайтов и рекомендаций
- **PerformanceOptimizer** — кэширование, профилирование, пакетная обработка
- **Trend Analysis** — выявление паттернов в исторических данных

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
.github/COPILOT_INSTRUCTIONS.md # Инструкции для AI агента
automation_policy.yaml     # Политика автономии
ARCHITECTURE.md            # Архитектура
AUTOMATION_GUIDE.md        # Руководство по автоматизации
SELF_LEARNING_GUIDE.md     # Руководство по саамообучению
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

См. подробнее: [AUTOMATION_GUIDE.md](AUTOMATION_GUIDE.md)

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

Workflow `release.yml` собирает и публикует пакет при изменении `pyproject.toml` в ветке `main` (использует OIDC, секреты не нужны).

## Архитектура и ADR

- `ARCHITECTURE.md` — обзор слоёв
- `AUTOMATION_GUIDE.md` — руководство по инфраструктуре автоматизации
- `SELF_LEARNING_GUIDE.md` — руководство по саамообучению и оптимизации
- `DECISIONS/ADR-0001-initial-architecture.md` — начальная архитектура
- `DECISIONS/ADR-0002-self-learning-performance.md` — система саамообучения

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
# AI-PRO
