import pytest

from autonomous_dev.example import add, sum_all


def test_add():
    assert add(2, 3) == 5


def test_sum_all():
    assert sum_all([1, 2, 3]) == 6


def test_sum_all_type_error():
    with pytest.raises(ValueError):
        sum_all([1, "x", 3])  # type: ignore[list-item]
