# Copilot Coding Agent Instructions

## Mission
Автоматизировать развитие проекта (качество, безопасность, функциональность) без снижения строгих стандартов.

## Core Principles
- **Predictability**: Изменения должны быть предсказуемыми и воспроизводимыми
- **Test-first**: Тесты создаются или обновляются вместе с изменениями логики
- **Minimal surface change per PR**: Один PR — одна логическая единица работы
- **Reproducibility**: Не ломать локальные dev-потоки

## Tooling Contract

### Обязательные проверки перед коммитом
```bash
# 1. Запустить pre-commit хуки
pre-commit run --all-files

# 2. Запустить тесты с проверкой покрытия
pytest --cov=src/autonomous_dev --cov-fail-under=85
```

### Запрещено без явного обоснования
- Ослаблять строгость mypy (strict mode)
- Удалять существующие тесты
- Снижать порог покрытия (текущий: 85%)
- Добавлять игнорирования линтера на уровне файла/модуля

## Allowed Changes

### Разрешено
- ✅ Добавление новой функциональности с тестами
- ✅ Рефакторинг с сохранением поведения (должны быть указаны инварианты)
- ✅ Обновление зависимостей (со ссылкой на changelog)
- ✅ Исправления безопасности (со ссылкой на CVE или advisory)
- ✅ Улучшение документации
- ✅ Оптимизация производительности (с бенчмарками)

### Требуется обоснование
- ⚠️ Изменения в публичном API
- ⚠️ Изменения в архитектуре (требуется ADR)
- ⚠️ Major version bump зависимостей
- ⚠️ Изменения в политике автоматизации

## Disallowed Without Approval

- ❌ Удаление или понижение инструментов безопасности
- ❌ Массовый рефакторинг (>100 файлов)
- ❌ Вендоринг внешнего кода без лицензионных проверок
- ❌ Отключение CI проверок

## Commit Convention (Conventional Commits)

```
<type>: <краткое описание>

[опциональное развёрнутое описание]

[опциональный footer с breaking changes, ссылки на issues]
```

### Типы коммитов
- `feat:` — новая функциональность
- `fix:` — исправление бага
- `refactor:` — рефакторинг без изменения поведения
- `test:` — только изменения в тестах
- `chore:` — инфраструктура, мета-задачи
- `docs:` — документация
- `perf:` — оптимизация производительности
- `build:` или `ci:` — сборка, пайплайн

### Примеры
```
feat: add metrics tracking for test duration

Implements MetricsTracker class with persistent storage.

Closes #123
```

```
fix: correct validation logic in FeedbackLoop

The previous implementation didn't handle edge case when
metrics list was empty.
```

## Branch Naming

```
feat/<краткое-описание>
fix/<краткое-описание>
chore/<краткое-описание>
refactor/<краткое-описание>
auto/dep-update-<date>
```

## Development Flow

### 1. Подготовка
- Прочитать `.github/COPILOT_INSTRUCTIONS.md`, `roadmap.yaml`, `automation_policy.yaml`
- Сформировать внутренний TODO список шагов
- Проверить существующие issue/ADR для контекста

### 2. Реализация
- Создать ветку с правильным именованием
- Внести минимальные изменения для решения задачи
- Обновить/создать тесты при любом изменении логики
- Запустить локальные проверки: `make all` или `pre-commit run --all-files && pytest`

### 3. Документирование
- Обновить docstrings для изменённых функций/классов
- При необходимости обновить README.md, ARCHITECTURE.md
- Для архитектурных решений создать ADR в `DECISIONS/`

### 4. Pull Request
- Открыть PR с чеклистом (см. ниже)
- Краткое резюме мотивации (зачем)
- Список изменений (что)
- Потенциальные риски и план отката

### 5. После ревью
- Обработать feedback
- Дождаться зелёного CI
- Merge после approval

## PR Checklist

Каждый PR должен включать:

```markdown
## Checklist
- [ ] Изменения логически атомарны (один PR = одна задача)
- [ ] Обновлены/добавлены тесты
- [ ] Локально: pre-commit OK
- [ ] Локально: pytest OK
- [ ] Нет снижения покрытия
- [ ] Нет ослабления статического анализа
- [ ] Документация обновлена (если нужно)
- [ ] Отсутствуют «лишние» файлы (временные, сгенерированные)
- [ ] Commit message следует Conventional Commits

## Changes
- Описание изменений

## Testing
- Как протестировано

## Risks
- Потенциальные риски и план отката
```

## Quality Gates

### Покрытие тестами
- **Минимум**: 85% (настроено в `pyproject.toml`)
- **Цель**: >90%
- **Отчёт**: Codecov integration (опционально)

### Линтинг
- **Ruff**: 0 ошибок обязательно
- **Black**: Единообразное форматирование
- **Line length**: 100 символов

### Типизация
- **mypy**: strict mode
- **Python**: 3.11+

### Безопасность
- **bandit**: статический анализ безопасности
- **pip-audit**: уязвимости в зависимостях (fail on HIGH)
- **deptry**: неиспользуемые/недостающие зависимости

## Edge Cases Handling

### Если нужно ослабить правило
- Создать отдельный PR с подробным обоснованием
- Использовать минимально возможный scope (per-line, per-function)
- Документировать причину в коде (комментарий)
- Упомянуть в PR description

### Если инструмент нестабилен
- Зафиксировать версию инструмента
- Описать проблему в PR
- Добавить TODO для будущего исследования

### Если нужен новый пакет
- **Обязательно указать**:
  - Причину (почему существующие не подходят)
  - Альтернативы (что рассматривалось)
  - Поддержка экосистемы (активность, лицензия)
- Добавить в `pyproject.toml` с закреплённой минорной версией
- Проверить лицензионную совместимость

## Automation Policy Reference

Детали политики автоматизации в `automation_policy.yaml`:

### Автоматический merge разрешён
- Dev dependency patch updates
- Форматирование кода
- Регенерация TOC в README
- Security audit reports (информационные)

### Требуется ревью
- Изменения в публичном API
- Major version bump
- Изменения в ADR
- Изменения в политике безопасности

## Self-Learning & Performance

Система включает метрики и оптимизацию:

- **MetricsTracker**: Запись метрик разработки
- **FeedbackLoop**: Анализ итераций и генерация инсайтов
- **Performance**: Кэширование, профилирование, пакетная обработка

Подробнее в `SELF_LEARNING_GUIDE.md`.

## CI/CD Pipeline

### Continuous Integration
- Matrix testing: Python 3.11, 3.12, 3.13
- Pre-commit hooks validation
- Linting (Ruff), formatting (Black), type checking (mypy)
- Unit tests с покрытием
- Security scanning (bandit, pip-audit, deptry)

### Release Workflow
- Триггер: изменение `pyproject.toml` в `main`
- Build + publish на PyPI (OIDC, без токенов)
- Artifacts сохраняются

## Troubleshooting

### Pre-commit fails
```bash
pre-commit clean
pre-commit install
pre-commit run --all-files
```

### Tests fail
```bash
pytest -v  # Подробный вывод
pytest --lf  # Только провалившиеся
pytest -k test_name  # Конкретный тест
```

### Lint errors
```bash
ruff check . --fix  # Автофикс где возможно
ruff format .       # Форматирование
```

### Type errors
```bash
mypy src/autonomous_dev --show-error-codes
```

## Communication

### При блокирующей проблеме
1. Описать проблему чётко и кратко
2. Указать что уже пробовали
3. Приложить релевантные логи/трассировки
4. Предложить возможные решения (если есть)

### При неуверенности
- Лучше спросить, чем делать неправильно
- Использовать draft PR для раннего feedback
- Помечать TODO в коде для будущего улучшения

## References

- **Architecture**: `ARCHITECTURE.md`
- **Self-Learning**: `SELF_LEARNING_GUIDE.md`
- **Automation**: `AUTOMATION_GUIDE.md`
- **Decisions**: `DECISIONS/ADR-*.md`
- **Roadmap**: `roadmap.yaml`
- **Policy**: `automation_policy.yaml`

---

**Status**: ✅ Active  
**Last Updated**: 2025-10-04  
**Version**: 1.0
