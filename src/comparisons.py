"""Module to be used for comparisons using a string operator.

>>> assert lt(2, 3)
>>> assert lt(3.3333334, 3.3333334004)
>>> assert not lt(3, 3)
>>> assert not lt(3, 2)
>>> assert not lt(2.00006, 2.00005)

>>> assert lte(2, 2)
>>> assert lte(2, 3)
>>> assert not lte(3, 2)
>>> assert not lte(2.11, 2.100001)

>>> assert gt(3, 2)
>>> assert not gt(3, 3)
>>> assert not gt(2, 3)
>>> assert not gt(2.11, 2.12)

>>> assert gte(2, 2)
>>> assert gte(3, 2)
>>> assert not gte(2, 3)
>>> assert not gte(2.1, 2.11)
"""


def equal(item_1, item_2):
    """
    >>> assert equal(2, 2)
    >>> assert not equal(2, 3)
    >>> assert equal(2, 2.)
    >>> assert equal(2, 2.0000000000)
    >>> assert not equal(2, 2.00000000001)
    
    Watch out for precision!
    >>> assert equal(2, 2.00000000000000001)
    """
    return item_1 == item_2


def less_than(item_1, item_2):
    """
    >>> assert less_than(2, 3)
    >>> assert less_than(3.3333334, 3.3333334004)
    >>> assert not less_than(3, 3)
    >>> assert not less_than(3, 2)
    >>> assert not less_than(2.00006, 2.00005)
    """
    return item_1 < item_2


def less_than_or_equal(item_1, item_2):
    """
    >>> assert less_than_or_equal(2, 2)
    >>> assert less_than_or_equal(2, 3)
    >>> assert not less_than_or_equal(3, 2)
    >>> assert not less_than_or_equal(2.11, 2.100001)
    """
    return item_1 <= item_2


def greater_than(item_1, item_2):
    """
    >>> assert greater_than(3, 2)
    >>> assert not greater_than(3, 3)
    >>> assert not greater_than(2, 3)
    >>> assert not greater_than(2.11, 2.12)
    """
    return item_1 > item_2


def greater_than_or_equal(item_1, item_2):
    """
    >>> assert greater_than_or_equal(2, 2)
    >>> assert greater_than_or_equal(3, 2)
    >>> assert not greater_than_or_equal(2, 3)
    >>> assert not greater_than_or_equal(2.1, 2.11)
    """
    return item_1 >= item_2


lt = less_than
lte = less_than_or_equal
gt = greater_than
gte = greater_than_or_equal


def normalize_operator(operator):
    # NOT THE BEST NAME EVER!
    return operator.strip().replace(' ', '_').lower()


def get_possible_string_operators():
    """
    >>> operators = get_possible_string_operators()
    >>> operators[:2]
    ('equal', 'less_than')
    >>> operators[-2:]
    ('greater than or equal', 'gte')
    >>> assert 'gt' in operators
    >>> assert 'less than' in operators
    >>> assert 'greater than_or equal' not in operators
    """
    return ('equal',
            'less_than', 'less than', 'lt',
            'less_than_or_equal', 'less than or equal', 'lte',
            'greater_than', 'greater than', 'gt',
            'greater_than_or_equal', 'greater than or equal', 'gte',
            )
