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
    return sum(values)


__all__ = ["add", "sum_all"]
