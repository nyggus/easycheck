"""Module to be used for comparisons using a string operator.

The operators is used by the check_it.checks functions. The module is
covered by both pytests doctests.
"""


def equal(item_1, item_2):
    """
    >>> assert equal(2, 2)
    >>> assert not equal(2, 3)
    
    Watch out for precision!
    >>> assert equal(2, 2.00000000000000001)
    """
    return item_1 == item_2


def less_than(item_1, item_2):
    """
    >>> less_than(2, 4)
    True
    >>> less_than('a', 'b')
    True
    >>> less_than(3, 2)
    False
    """
    return item_1 < item_2


def less_than_or_equal(item_1, item_2):
    """
    >>> less_than_or_equal(2, 4)
    True
    >>> less_than_or_equal('A', 'A')
    True
    >>> less_than_or_equal(3, 2)
    False
    """
    return item_1 <= item_2


def greater_than(item_1, item_2):
    """
    >>> greater_than(3, 2)
    True
    >>> greater_than('A', 'a')
    False
    >>> greater_than([1, 2], [1, 1])
    True
    """
    return item_1 > item_2


def greater_than_or_equal(item_1, item_2):
    """
    >>> greater_than_or_equal(3, 2)
    True
    >>> greater_than_or_equal('A', 'a')
    False
    >>> greater_than_or_equal([1, 2], [1, 1])
    True
    """
    return item_1 >= item_2


lt = less_than
lte = less_than_or_equal
gt = greater_than
gte = greater_than_or_equal


def get_possible_operators():
    """
    >>> operators = get_possible_operators()
    >>> type(operators[0])
    <class 'function'>
    >>> len(operators)
    9
    """
    return (equal,
            less_than, lt,
            less_than_or_equal, lte,
            greater_than, gt,
            greater_than_or_equal, gte,
            )
