import pytest
import sys
import checkit

from checkit.comparisons import (equal,
                                 less_than, lt,
                                 less_than_or_equal, lte,
                                 greater_than, gt,
                                 greater_than_or_equal, gte,
                                 get_possible_operators,
                                 )


def test_equal():
    assert equal(2, 2.)
    assert equal(2, 2.0000000000)
    assert not equal(2, 2.00000000001)
    assert equal('a', 'a')
    assert not equal('a', 'A')


def test_less_than():
    assert less_than(2, 3)
    assert less_than(3.3333334, 3.3333334004)
    assert less_than('a', 'b')
    assert less_than([1, 1], [1, 2])
    assert not less_than('a', 'A')
    assert not less_than(3, 3)
    assert not less_than(3, 2)
    assert not less_than(2.00006, 2.00005)


def test_less_than_or_equal():
    assert less_than_or_equal(2, 2)
    assert less_than_or_equal(2, 3)
    assert less_than_or_equal([1, 2], [2, 1])
    assert less_than_or_equal([1, 3, 3, 4], [1, 3, 3, 4])
    assert not less_than_or_equal(3, 2)
    assert not less_than_or_equal(2.11, 2.100001)


def test_greater_than():
    assert greater_than(3, 2)
    assert greater_than([1, 2], [1, 1])
    assert greater_than([1, 2], [1, 1, 1, 1])
    assert not greater_than([1, 2], [1, 2, 1, 1])
    assert not greater_than([1, 2], [1, 2])
    assert not greater_than(3, 3)
    assert not greater_than(2, 3)
    assert not greater_than(2.11, 2.12)


def test_greater_than_or_equal():
    assert greater_than_or_equal(3, 2)
    assert greater_than_or_equal(3, 3)
    assert greater_than_or_equal([1, 2], [1, 1])
    assert greater_than_or_equal([1, 2], [1, 1, 1, 1])
    assert greater_than_or_equal([1, 2], [1, 2])
    assert not greater_than_or_equal([1, 2], [1, 2, 1, 1])
    assert greater_than_or_equal('b', 'A')
    assert not greater_than_or_equal(2.11, 2.12)


def test_get_possible_operators():
    operators = get_possible_operators()
    assert len(operators) == 9
    assert all(callable(operator) for operator in operators)
    possible_operators = (equal,
                          less_than, lt,
                          less_than_or_equal, lte,
                          greater_than, gt,
                          greater_than_or_equal, gte,
                          )
    assert all(operator in possible_operators for operator in operators)


def test_short_versions_of_operators():
    assert lt(2, 3)
    assert lt(3.3333334, 3.3333334004)
    assert not lt(3, 3)
    assert not lt(3, 2)
    assert not lt(2.00006, 2.00005)

    assert lte(2, 2)
    assert lte(2, 3)
    assert not lte(3, 2)
    assert not lte(2.11, 2.100001)

    assert gt(3, 2)
    assert not gt(3, 3)
    assert not gt(2, 3)
    assert not gt(2.11, 2.12)

    assert gte(2, 2)
    assert gte(3, 2)
    assert not gte(2, 3)
    assert not gte(2.1, 2.11)


def test_get_possible_operators():
    operators = get_possible_operators()
    assert all(callable(operator) for operator in operators)
    assert len(operators) == 9
