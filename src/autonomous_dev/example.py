"""Пример модуля с простой функцией и заделом под расширение."""

from __future__ import annotations

from collections.abc import Iterable


def add(a: int, b: int) -> int:
    """Сложить два целых числа.

    Args:
        a: Первое число.
        b: Второе число.
    Returns:
        Сумма a и b.
    """
    return a + b


def sum_all(values: Iterable[int]) -> int:
    """Просуммировать все значения.

    Все значения предполагаются int согласно аннотации типов.
    """
    total = 0
    for v in values:  # итерация для валидации каждого элемента
        # Проверяем строго тип int (исключая например bool, если нужно можно ужесточить)
        if type(v) is not int:  # noqa: E721 - преднамеренно используем type(...) is
            raise ValueError(f"Expected int, got {type(v).__name__}")
        total += v
    return total


__all__ = ["add", "sum_all"]
