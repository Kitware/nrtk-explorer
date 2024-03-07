from typing import List
from nrtk_explorer.library import filtering

a, b, c = 0, 1, 2
test_values: List[List[int]] = [
    [],
    [a],
    [b],
    [c],
    [a, b],
    [a, c],
    [b, c],
    [a, b, c],
]


def test_concrete_and():
    filter = filtering.ConcreteIdFilter()
    result = list(map(filter.evaluate, test_values))
    assert result == [True] * 8

    filter.set_ids([], "and")
    result = list(map(filter.evaluate, test_values))
    assert result == [True] * 8

    filter.set_ids((a,), "and")
    result = list(map(filter.evaluate, test_values))
    assert result == [False, True, False, False, True, True, False, True]

    filter.set_ids((b,), "and")
    result = list(map(filter.evaluate, test_values))
    assert result == [False, False, True, False, True, False, True, True]

    filter.set_ids((c,), "and")
    result = list(map(filter.evaluate, test_values))
    assert result == [False, False, False, True, False, True, True, True]

    filter.set_ids(
        (
            a,
            b,
        ),
        "and",
    )
    result = list(map(filter.evaluate, test_values))
    assert result == [False, False, False, False, True, False, False, True]

    filter.set_ids(
        (
            a,
            c,
        ),
        "and",
    )
    result = list(map(filter.evaluate, test_values))
    assert result == [False, False, False, False, False, True, False, True]

    filter.set_ids(
        (
            b,
            c,
        ),
        "and",
    )
    result = list(map(filter.evaluate, test_values))
    assert result == [False, False, False, False, False, False, True, True]

    filter.set_ids(
        (
            a,
            b,
            c,
        ),
        "and",
    )
    result = list(map(filter.evaluate, test_values))
    assert result == [False, False, False, False, False, False, False, True]


def test_concrete_or():
    filter = filtering.ConcreteIdFilter()
    result = list(map(filter.evaluate, test_values))
    assert result == [True] * 8

    filter.set_ids([], "or")
    result = list(map(filter.evaluate, test_values))
    assert result == [True] * 8

    filter.set_ids((a,), "or")
    result = list(map(filter.evaluate, test_values))
    assert result == [False, True, False, False, True, True, False, True]

    filter.set_ids((b,), "or")
    result = list(map(filter.evaluate, test_values))
    assert result == [False, False, True, False, True, False, True, True]

    filter.set_ids((c,), "or")
    result = list(map(filter.evaluate, test_values))
    assert result == [False, False, False, True, False, True, True, True]

    filter.set_ids(
        (
            a,
            b,
        ),
        "or",
    )
    result = list(map(filter.evaluate, test_values))
    assert result == [False, True, True, False, True, True, True, True]

    filter.set_ids(
        (
            a,
            c,
        ),
        "or",
    )
    result = list(map(filter.evaluate, test_values))
    assert result == [False, True, False, True, True, True, True, True]

    filter.set_ids(
        (
            b,
            c,
        ),
        "or",
    )
    result = list(map(filter.evaluate, test_values))
    assert result == [False, False, True, True, True, True, True, True]

    filter.set_ids(
        (
            a,
            b,
            c,
        ),
        "or",
    )
    result = list(map(filter.evaluate, test_values))
    assert result == [False, True, True, True, True, True, True, True]


def test_concrete_not():
    filter = filtering.ConcreteIdFilter()
    filter.set_ids((a,), "and")
    not_filter = filtering.NotFilter(filter)
    result = list(map(not_filter.evaluate, test_values))
    assert result == [True, False, True, True, False, False, True, False]


def test_composite_and():
    filter_a = filtering.ConcreteIdFilter()
    filter_a.set_ids((a,), "and")

    filter_b = filtering.ConcreteIdFilter()
    filter_b.set_ids((b,), "and")

    filter_not_a = filtering.NotFilter(filter_a)
    filter_not_b = filtering.NotFilter(filter_b)

    filter = filtering.ComposableFilter()
    not_filter = filtering.NotFilter(filter)

    filter.compose(filter_a, filter_b, "and")
    result = list(map(filter.evaluate, test_values))
    assert result == [False, False, False, False, True, False, False, True]
    result = list(map(not_filter.evaluate, test_values))
    assert result == [True, True, True, True, False, True, True, False]

    filter.compose(filter_a, filter_not_b, "and")
    result = list(map(filter.evaluate, test_values))
    assert result == [False, True, False, False, False, True, False, False]

    filter.compose(filter_not_a, filter_not_b, "and")
    result = list(map(filter.evaluate, test_values))
    assert result == [True, False, False, True, False, False, False, False]


def test_composite_or():
    filter_a = filtering.ConcreteIdFilter()
    filter_a.set_ids((a,), "and")

    filter_b = filtering.ConcreteIdFilter()
    filter_b.set_ids((b,), "and")

    filter_not_a = filtering.NotFilter(filter_a)
    filter_not_b = filtering.NotFilter(filter_b)

    filter = filtering.ComposableFilter()

    filter.compose(filter_a, filter_b, "or")
    result = list(map(filter.evaluate, test_values))
    assert result == [False, True, True, False, True, True, True, True]

    filter.compose(filter_a, filter_not_b, "or")
    result = list(map(filter.evaluate, test_values))
    assert result == [True, True, False, True, True, True, False, True]

    filter.compose(filter_not_a, filter_not_b, "or")
    result = list(map(filter.evaluate, test_values))
    assert result == [True, True, True, True, False, True, True, False]
