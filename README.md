# autonomous-dev

![CI](https://github.com/rissottipaul-boop/AI-PRO/actions/workflows/ci.yml/badge.svg)
![Nightly](https://github.com/rissottipaul-boop/AI-PRO/actions/workflows/nightly.yml/badge.svg)
![Changelog](https://github.com/rissottipaul-boop/AI-PRO/actions/workflows/changelog.yml/badge.svg)
![Coverage](https://codecov.io/gh/rissottipaul-boop/AI-PRO/branch/main/graph/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python Versions](https://img.shields.io/badge/python-3.11%20|%203.12%20|%203.13-3776AB.svg)
![SBOM](https://img.shields.io/badge/SBOM-CycloneDX-success.svg)

Автономная заготовка репозитория для быстрой AI-ассистируемой разработки.

## Возможности

### Базовые

- Строгий Python 3.11+ (типизация, mypy strict)
- Линтинг и автоформат (ruff + black)
- Pre-commit хуки (ruff, black, mypy)
- Тестирование (pytest + coverage, порог 85%)
- CI (GitHub Actions) — matrix (3.11, 3.12, 3.13) + отдельный security job
- Security сканы: bandit, pip-audit (HIGH), deptry
- Automation Policy (`automation_policy.yaml`)
- Dependabot (pip + actions)
- Release workflow (build + publish на PyPI по main через OIDC, без пароля)
- Makefile и PowerShell скрипт для Windows
- VSCode задачи и настройки
- ADR и архитектурная документация

### Автономный AI-агент 🤖

- **Copilot Instructions** (`.github/copilot-instructions.md`) — полный контракт для агента
- **Structured Tasks** (`.github/ISSUE_TEMPLATE/agent_task.yml`) — шаблон задач для агента
- **Automation Guide** (`AUTOMATION_GUIDE.md`) — комплексная документация автоматизации
- Conventional Commits стандарт
- Чёткие границы разрешённых изменений

## Быстрый старт

```bash
# (опционально) создать виртуальное окружение (Linux/macOS)
python -m venv .venv
source .venv/bin/activate
```

PowerShell (Windows):

```powershell
python -m venv .venv
./.venv/Scripts/Activate.ps1
```

CMD (Windows):

```bat
python -m venv .venv
.\.venv\Scripts\activate.bat
```

Далее общие шаги:

```bash
# Установка dev зависимостей
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
src/autonomous_dev/                      # исходный код
tests/                                   # тесты
.github/
  ├── copilot-instructions.md            # Инструкции для AI-агента
  ├── ISSUE_TEMPLATE/agent_task.yml      # Шаблон задач для агента
  └── workflows/
      ├── ci.yml                         # CI pipeline
      └── release.yml                    # Release pipeline
automation_policy.yaml                   # Политика автономии
AUTOMATION_GUIDE.md                      # Гид по автоматизации
ARCHITECTURE.md                          # Архитектура
DECISIONS/                               # ADR решения
roadmap.yaml                             # Дорожная карта
.devcontainer/                           # Dev Container конфигурация
```

## Автономный рабочий цикл AI

См. полную документацию в `.github/copilot-instructions.md` и `AUTOMATION_GUIDE.md`.

**Краткий цикл:**

1. **Plan** — анализ задач из roadmap/issues
2. **Implement** — минимальные, атомарные изменения
3. **Validate** — локальные проверки (lint + test)
4. **Commit** — следуя Conventional Commits
5. **CI Validation** — GitHub Actions проверяет всё
6. **Review** — человек только для high-impact
7. **Merge** — авто или manual (см. `automation_policy.yaml`)
8. **Release** — автоматический при bump версии

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

Workflow `release.yml` собирает и публикует пакет при изменении `pyproject.toml` в ветке `main` (OIDC Trusted Publishing — `PYPI_TOKEN` не требуется). Убедись, что версия повышена по семантике (semver) перед merge.

## Архитектура и ADR

- `ARCHITECTURE.md` — обзор слоёв
- `DECISIONS/ADR-0001-initial-architecture.md` — фиксация ключевых решений

## Дорожная карта

`roadmap.yaml` хранит инициативы для планирования последующих автоматизаций.

## Документация для AI-агентов

- **[Copilot Instructions](.github/copilot-instructions.md)** — полный контракт и гайдлайны
- **[Automation Guide](AUTOMATION_GUIDE.md)** — инфраструктура автоматизации
- **[Agent Task Template](.github/ISSUE_TEMPLATE/agent_task.yml)** — структурированные задачи
- **[Automation Policy](automation_policy.yaml)** — правила и пороги
- **[Architecture](ARCHITECTURE.md)** — архитектура системы
- **[Roadmap](roadmap.yaml)** — дорожная карта

## Расширения (потенциал)

- ✅ Devcontainer + Dockerfile
- ✅ Conventional commits (реализовано)
- Автогенерация changelog (git-cliff / github-changelog-generator)
- SBOM + лицензии
- ChatOps команды (slash /qa /security)
- Performance benchmarks

## Dev Container

Среда разработки в контейнере обеспечивает воспроизводимость и унификацию инструментов.

### Запуск

1. Установить расширение VS Code: Dev Containers
2. Открыть папку репозитория в VS Code
3. Нажать: F1 → Dev Containers: Reopen in Container
4. Дождаться установки зависимостей и pre-commit хуков

### Что внутри контейнера

- Python 3.11 (venv в `/workspace/.venv`)
- Установлены dev зависимости (`.[dev]`)
- pre-commit хуки уже установлены
- Расширения VS Code (Python, Pylance, Ruff, Docker, GitHub Actions)
- docker-in-docker (опционально) для будущих интеграций

### Частые операции внутри контейнера

```bash
pytest -q
ruff check .
mypy src/autonomous_dev
pre-commit run --all-files
```

### Обновление зависимостей

При изменении `pyproject.toml` пересоберите контейнер: F1 → Dev Containers: Rebuild Container

## MCP Конфигурация

В репозитории доступен файл `mcp.json`, описывающий запуск GitHub MCP сервера через Docker.

```jsonc
{
  "mcp": {
    "inputs": [
      {
        "type": "promptString",
        "id": "github_token",
        "description": "GitHub Personal Access Token",
        "password": true
      }
    ],
    "servers": {
      "github": {
        "command": "docker",
        "args": [
          "run",
          "-i",
          "--rm",
            "-e",
          "GITHUB_PERSONAL_ACCESS_TOKEN",
          "ghcr.io/github/github-mcp-server"
        ],
        "env": {
          "GITHUB_PERSONAL_ACCESS_TOKEN": "${input:github_token}"
        }
      }
    }
  }
}
```

### Использование

1. Получить GitHub Personal Access Token (минимально: `repo`, при необходимости `actions`, `security_events`)
2. При инициализации MCP клиент запросит ввод `github_token`
3. Сервер запустится в контейнере `ghcr.io/github/github-mcp-server`

### Безопасность (MCP)

- Не коммитить реальные токены
- Использовать fine-grained токен с минимальным scope
- Регулярно ревокать неиспользуемые ключи

---

## Лицензия

MIT
