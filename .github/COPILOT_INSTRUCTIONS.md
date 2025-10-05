# Copilot Coding Agent Instructions

## Mission

Автоматизировать развитие проекта (качество, безопасность, функциональность) без снижения строгих стандартов качества и с минимальными изменениями.

## Core Principles

1. **Predictability** — результат должен быть предсказуемым и воспроизводимым
2. **Test-first** — тесты добавляются/обновляются вместе с изменениями логики
3. **Minimal surface change** — минимальные изменения в каждом PR
4. **Reproducibility** — не ломать локальные dev-потоки
5. **Safety** — несколько слоев валидации для предотвращения поломок

## Repository Context

- **Language:** Python 3.11–3.13
- **Packaging:** `pyproject.toml` (единая точка правды для зависимостей и конфигурации)
- **Quality Tools:** pre-commit (ruff, ruff-format, black, mypy), pytest + coverage (>=85%)
- **Security:** bandit, pip-audit (fail on HIGH), deptry
- **CI:** GitHub Actions (matrix Python 3.11-3.13 + отдельный security job)
- **Releases:** Автоматические через GitHub Actions + OIDC → PyPI (при изменении версии в `pyproject.toml`)

## Tooling Contract

### Перед каждым коммитом выполни локально

```bash
# 1. Pre-commit hooks
pre-commit run --all-files

# 2. Tests with coverage
pytest --cov=src/autonomous_dev --cov-fail-under=85
```

### Не разрешается без явного обоснования

- Снижать строгость mypy (strict mode обязателен)
- Удалять тесты
- Снижать порог покрытия (<85%)
- Ослаблять настройки линтера
- Отключать security инструменты

## Allowed Changes

### ✅ Разрешено (с тестами)

- Добавление новых функций с тестами
- Рефакторинг с сохранением поведения (должны быть указаны инварианты)
- Обновление зависимостей (со ссылкой на changelog)
- Исправления безопасности (ссылка на CVE или advisory)
- Улучшение документации
- Оптимизация производительности (с бенчмарками/доказательствами)

### ⛔ Запрещено без явного одобрения

- Удаление/ослабление security инструментов
- Массовый рефакторинг (>100 файлов)
- Изменение public API без ADR
- Vendoring внешнего кода
- Добавление новых зависимостей без обоснования альтернатив
- Изменения в `.github/agents/` (это инструкции для других агентов)

## Commit Conventions

Используем **Conventional Commits** для структурирования истории:

### Типы коммитов

- `feat:` — новая функциональность
- `fix:` — исправление бага
- `refactor:` — изменение кода без изменения поведения
- `test:` — только изменения тестов
- `chore:` — инфраструктура/мета (CI, зависимости, конфиги)
- `docs:` — только документация
- `perf:` — улучшение производительности
- `build:` или `ci:` — изменения сборки/CI пайплайна
- `style:` — форматирование (без изменения логики)

### Примеры

feat: add metrics tracking for performance analysis
fix: handle edge case in learning insight generation
refactor: extract common optimization logic
test: add coverage for batch processing scenarios
chore: update ruff to 0.13.0
docs: clarify self-learning module usage
perf: optimize cache lookup with binary search
ci: add Python 3.14 to test matrix

## Branch Naming

- `feat/<краткое-описание>` — новая функциональность
- `fix/<краткое-описание>` — исправление
- `chore/<краткое-описание>` — инфраструктура
- `refactor/<краткое-описание>` — рефакторинг
- `auto/dep-update-<дата>` — автоматическое обновление зависимостей

## Workflow: Автономный цикл разработки

### 1. Подготовка (Planning)

- Прочитать `.github/COPILOT_INSTRUCTIONS.md` (этот файл)
- Изучить `automation_policy.yaml` — правила автоматизации
- Просмотреть `roadmap.yaml` — дорожная карта проекта
- Проверить открытые issues и PR

### 2. Анализ задачи

- Определить scope: что ВКЛЮЧЕНО и что ИСКЛЮЧЕНО
- Составить TODO (внутренний список шагов)
- Оценить риски и edge cases
- Определить acceptance criteria (как измерить успех)

### 3. Реализация

- Создать ветку по конвенции
- Внести изменения (минимальные, атомарные)
- Обновить/создать тесты при любом изменении логики
- Прогнать локальные проверки:

  ```bash
  pre-commit run --all-files
  pytest --cov=src/autonomous_dev --cov-fail-under=85
  ```

### 4. Документация

- Обновить docstrings (если изменился public API)
- Обновить README/ARCHITECTURE/ADR (если релевантно)
- Добавить примеры использования (если новая функция)

### 5. Pull Request

Создать PR с чеклистом (см. раздел "PR Checklist" ниже)

### 6. CI Validation

- GitHub Actions проверяет все автоматически
- Если CI падает — исправить итеративно

### 7. Review & Merge

- Human review только для high-impact изменений (см. `automation_policy.yaml`)
- Auto-merge или manual merge в зависимости от policy

### 8. Release (автоматический)

- Если изменена версия в `pyproject.toml` — автоматический релиз на PyPI

## PR Checklist

Каждый PR должен включать:

```markdown
- [ ] Изменения логически атомарны (один логический блок работы)
- [ ] Обновлены/добавлены тесты
- [ ] Локально: pre-commit OK
- [ ] Локально: pytest OK (покрытие ≥85%)
- [ ] Нет снижения покрытия
- [ ] Нет ослабления статического анализа (mypy strict)
- [ ] Документация обновлена (если нужно)
- [ ] Нет временных/мусорных файлов
- [ ] Коммиты следуют Conventional Commits
```

## Edge Cases & Special Situations

### Если нужно ослабить правило

- Создать отдельный PR с детальным обоснованием
- Добавить ADR в `DECISIONS/` с объяснением решения
- Использовать узкие ignore (per-line) вместо глобальных изменений конфигурации

### Если инструмент в CI нестабилен

- Зафиксировать версию инструмента
- Описать проблему в PR
- Добавить workaround с TODO для будущего исправления

### Если нужна новая зависимость

Обязательно указать:

- Причина добавления
- Рассмотренные альтернативы
- Активная поддержка (дата последнего релиза)
- Лицензия (совместима с MIT)
- Размер/влияние на сборку

## Quality Standards

### Coverage

- **Минимум:** 85% (настроено в `pyproject.toml`)
- **Текущий:** 100%
- **Reporting:** Codecov integration

### Lint & Format

- **Ruff:** 0 ошибок обязательно
- **Black:** Единый стиль форматирования
- **Line length:** 100 символов

### Type Safety

- **mypy:** Strict mode включен
- **Python:** 3.11+ обязательно
- Все публичные функции должны иметь type hints

### Security

- **bandit:** 0 критичных/высоких проблем
- **pip-audit:** Fail on HIGH severity
- **deptry:** Нет неиспользуемых зависимостей

## Automation Policy Reference

См. `automation_policy.yaml` для полной политики. Основные моменты:

### Auto-mergeable (при зелёном CI)

- Dev dependency patch updates
- Форматирование кода
- Изменения только тестов (без изменения логики)
- Обновления документации (non-ADR)

### Requires Human Review

- Public API changes
- Major version bumps
- ADR modifications
- Security policy changes
- Изменения в release workflow

## Key Files & Directories

.github/
  ├── COPILOT_INSTRUCTIONS.md    ← этот файл
  ├── ISSUE_TEMPLATE/
  │   ├── agent_task.yml         ← шаблон для задач агента
  │   ├── bug_report.yml
  │   └── feature_request.yml
  ├── workflows/
  │   ├── ci.yml                 ← основной CI пайплайн
  │   └── release.yml            ← автоматический релиз
  └── CODEOWNERS                 ← ownership для ревью

automation_policy.yaml           ← политика автоматизации
roadmap.yaml                     ← дорожная карта
ARCHITECTURE.md                  ← архитектура системы
DECISIONS/                       ← ADR (Architecture Decision Records)
src/autonomous_dev/              ← исходный код
tests/                           ← тесты

## References

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [pytest Documentation](https://docs.pytest.org/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)

## Status

✅ **Инфраструктура готова и оперативна**  
📅 **Last Updated:** 2025-10-04  
🔒 **Security:** bandit + pip-audit + deptry активны  
🧪 **Tests:** 100% coverage  
🚀 **Release:** Автоматический через OIDC

---

**Примечание:** Этот файл — единый источник правды для автономной работы агента. При возникновении противоречий с другими документами — этот файл имеет приоритет для автоматизированной работы.

## MCP Integration

Для взаимодействия с GitHub через Model Context Protocol предоставлен файл `mcp.json` в корне репозитория.

### Назначение

Конфиг описывает запуск GitHub MCP сервера в Docker контейнере (образ: `ghcr.io/github/github-mcp-server`). Клиент MCP запрашивает ввод персонального токена и передаёт его контейнеру через переменную окружения `GITHUB_PERSONAL_ACCESS_TOKEN`.

### Файл `mcp.json` (фрагмент)

```jsonc
{
  "mcp": {
    "inputs": [
      { "type": "promptString", "id": "github_token", "description": "GitHub Personal Access Token", "password": true }
    ],
    "servers": {
      "github": {
        "command": "docker",
        "args": [
          "run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"
        ],
        "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${input:github_token}" }
      }
    }
  }
}
```

### Политика безопасности MCP

- Не хранить токены в файлах / git истории
- Использовать fine-grained PAT с минимальными правами (`repo`, опционально `actions`, `security_events`)
- Регулярно ревокать неиспользуемые токены
- Не инжектировать токен в логи CI

### Поведение агента

Если требуется доступ к GitHub API через MCP:

1. Проверить наличие файла `mcp.json`
2. Убедиться, что токен запрошен интерактивно клиентом
3. Не предлагать пользователю вводить токен в открытом виде в PR/issue
