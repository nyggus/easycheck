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


def test_equal_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        equal()
    with pytest.raises(TypeError, match='required positional argument'):
        equal(1)
    with pytest.raises(TypeError, match='required positional argument'):
        equal(True)
    with pytest.raises(TypeError, match='unexpected keyword'):
        equal(item1=0, item_2=2)
    with pytest.raises(TypeError, match='unexpected keyword'):
        equal(item_1=0, item2=2)


def test_equal():
    assert equal(2, 2.)
    assert equal(2, 2.0000000000)
    assert not equal(2, 2.00000000001)
    assert equal('a', 'a')
    assert not equal('a', 'A')


def test_less_than_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        less_than()
    with pytest.raises(TypeError, match='required positional argument'):
        less_than(1)
    with pytest.raises(TypeError, match='required positional argument'):
        less_than(True)
    with pytest.raises(TypeError, match='unexpected keyword'):
        less_than(item1=0, item_2=2)
    with pytest.raises(TypeError, match='unexpected keyword'):
        less_than(item_1=0, item2=2)


def test_less_than():
    assert less_than(2, 3)
    assert less_than(3.3333334, 3.3333334004)
    assert less_than('a', 'b')
    assert less_than([1, 1], [1, 2])
    assert not less_than('a', 'A')
    assert not less_than(3, 3)
    assert not less_than(3, 2)
    assert not less_than(2.00006, 2.00005)


def test_less_than_or_equal_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        less_than_or_equal()
    with pytest.raises(TypeError, match='required positional argument'):
        less_than_or_equal(1)
    with pytest.raises(TypeError, match='required positional argument'):
        less_than_or_equal(True)
    with pytest.raises(TypeError, match='unexpected keyword'):
        less_than_or_equal(item1=0, item_2=2)
    with pytest.raises(TypeError, match='unexpected keyword'):
        less_than_or_equal(item_1=0, item2=2)


def test_less_than_or_equal():
    assert less_than_or_equal(2, 2)
    assert less_than_or_equal(2, 3)
    assert less_than_or_equal([1, 2], [2, 1])
    assert less_than_or_equal([1, 3, 3, 4], [1, 3, 3, 4])
    assert not less_than_or_equal(3, 2)
    assert not less_than_or_equal(2.11, 2.100001)


def test_greater_than_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        greater_than()
    with pytest.raises(TypeError, match='required positional argument'):
        greater_than(1)
    with pytest.raises(TypeError, match='required positional argument'):
        greater_than(True)
    with pytest.raises(TypeError, match='unexpected keyword'):
        greater_than(item1=0, item_2=2)
    with pytest.raises(TypeError, match='unexpected keyword'):
        greater_than(item_1=0, item2=2)


def test_greater_than():
    assert greater_than(3, 2)
    assert greater_than([1, 2], [1, 1])
    assert greater_than([1, 2], [1, 1, 1, 1])
    assert not greater_than([1, 2], [1, 2, 1, 1])
    assert not greater_than([1, 2], [1, 2])
    assert not greater_than(3, 3)
    assert not greater_than(2, 3)
    assert not greater_than(2.11, 2.12)


def test_greater_than_or_equal_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        greater_than_or_equal()
    with pytest.raises(TypeError, match='required positional argument'):
        greater_than_or_equal(1)
    with pytest.raises(TypeError, match='required positional argument'):
        greater_than_or_equal(True)
    with pytest.raises(TypeError, match='unexpected keyword'):
        greater_than_or_equal(item1=0, item_2=2)
    with pytest.raises(TypeError, match='unexpected keyword'):
        greater_than_or_equal(item_1=0, item2=2)


def test_greater_than_or_equal():
    assert greater_than_or_equal(3, 2)
    assert greater_than_or_equal(3, 3)
    assert greater_than_or_equal([1, 2], [1, 1])
    assert greater_than_or_equal([1, 2], [1, 1, 1, 1])
    assert greater_than_or_equal([1, 2], [1, 2])
    assert not greater_than_or_equal([1, 2], [1, 2, 1, 1])
    assert greater_than_or_equal('b', 'A')
    assert not greater_than_or_equal(2.11, 2.12)


def test_get_possible_operators_edge_cases():
    with pytest.raises(TypeError, match='takes 0 positional arguments'):
        get_possible_operators(20)
    with pytest.raises(TypeError, match='takes 0 positional arguments'):
        get_possible_operators(None)


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


def test_short_versions_of_operators_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        lt()
    with pytest.raises(TypeError, match='required positional argument'):
        lt(1)
    with pytest.raises(TypeError, match='required positional argument'):
        lte()
    with pytest.raises(TypeError, match='required positional argument'):
        lte(1)
    with pytest.raises(TypeError, match='required positional argument'):
        gt()
    with pytest.raises(TypeError, match='required positional argument'):
        gt(1)
    with pytest.raises(TypeError, match='required positional argument'):
        gte()
    with pytest.raises(TypeError, match='required positional argument'):
        gte(1)
    with pytest.raises(TypeError, match='unexpected keyword'):
        lt(item1=1, item_2=1)
    with pytest.raises(TypeError, match='unexpected keyword'):
        lt(item_1=1, item2=1)
    with pytest.raises(TypeError, match='unexpected keyword'):
        lte(item1=1, item_2=1)
    with pytest.raises(TypeError, match='unexpected keyword'):
        lte(item_1=1, item2=1)
    with pytest.raises(TypeError, match='unexpected keyword'):
        gt(item1=1, item_2=1)
    with pytest.raises(TypeError, match='unexpected keyword'):
        gt(item_1=1, item2=1)
    with pytest.raises(TypeError, match='unexpected keyword'):
        gte(item1=1, item_2=1)
    with pytest.raises(TypeError, match='unexpected keyword'):
        gte(item_1=1, item2=1)


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
