# autonomous-dev



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

- Makefile и PowerShell скрипт для Windows
- VSCode задачи и настройки
- ADR и архитектурная документация


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

```

## Автономный рабочий цикл AI



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



## Архитектура и ADR

- `ARCHITECTURE.md` — обзор слоёв
- `AUTOMATION_GUIDE.md` — руководство по инфраструктуре автоматизации
- `SELF_LEARNING_GUIDE.md` — руководство по саамообучению и оптимизации
- `DECISIONS/ADR-0001-initial-architecture.md` — начальная архитектура
- `DECISIONS/ADR-0002-self-learning-performance.md` — система саамообучения

## Дорожная карта

`roadmap.yaml` хранит инициативы для планирования последующих автоматизаций.

## Документация для AI-агентов

- **[Copilot Instructions](.github/COPILOT_INSTRUCTIONS.md)** — полный контракт и гайдлайны
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
