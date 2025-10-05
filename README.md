# autonomous-dev



Автономная заготовка репозитория для быстрой AI-ассистируемой разработки.

## Возможности

### Базовые

- Тестирование (pytest + coverage, порог 85%)
- CI (GitHub Actions) — matrix (3.11, 3.12, 3.13) + отдельный security job

- Automation Policy (`automation_policy.yaml`)
- Dependabot (pip + actions)
- Release workflow (build + publish на PyPI по main через OIDC, без пароля)
- Makefile и PowerShell скрипт для Windows
- VSCode задачи и настройки
- ADR и архитектурная документация
- Политика безопасности (SECURITY.md)

### Саамообучение и производительность 🚀
- **Система метрик**: отслеживание и анализ показателей разработки
- **Анализ трендов**: автоматическое выявление паттернов и проблем
- **Генерация инсайтов**: предложения по улучшению на основе данных
- **Циклы обратной связи**: непрерывное улучшение процессов
- **Профилирование**: мониторинг производительности операций
- **Кэширование**: оптимизация дорогих вычислений
- **Батчинг и параллелизация**: эффективная обработка данных

### Автономный AI-агент 🤖

- **Copilot Instructions** (`.github/COPILOT_INSTRUCTIONS.md`) — полный контракт для агента
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
  ├── COPILOT_INSTRUCTIONS.md            # Инструкции для AI-агента
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



## Политика автоматизации

Файл `automation_policy.yaml` задаёт:

- Порог покрытия: 85%
- Жёсткий линт (0 ошибок)
- Что разрешено авто-мерджить (dev deps patch, форматирование)
- Что требует ревью (public API, major bump, ADR изменения)

## Безопасность


- `deptry` — неиспользуемые/скрытые зависимости
- ✅ SBOM (CycloneDX) — генерируется в CI для каждого билда
- Планируемое: расширенный SAST

См. [SECURITY.md](SECURITY.md) для подробной информации о мерах безопасности.

## Обновления зависимостей

- Dependabot конфиг: еженедельные PR для pip и GitHub Actions
- Возможна интеграция Renovate (будущее)

## Релизы

Workflow `release.yml` собирает и публикует пакет при изменении `pyproject.toml` в ветке `main` (OIDC Trusted Publishing — `PYPI_TOKEN` не требуется). Убедись, что версия повышена по семантике (semver) перед merge.

## Архитектура и ADR

- `ARCHITECTURE.md` — обзор слоёв
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
- ✅ Автогенерация changelog (git-cliff реализован)
- ✅ SBOM (CycloneDX в CI)
- ✅ Nightly workflow (расширенные проверки)
- ✅ Version checking (семантическая валидация)
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
