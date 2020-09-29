"""A module for simple asserts to be used outside of testing.

The module offers very simple asserting functions. They do not offer
much new functionality over raising exceptions when a particular condition
is violated. Rather, they offer simple and easy to understand wrappers
for assering conditions and raising the corresponding exceptions.

The main function is assert_that, which could be enough for all
asserts. The other functions are actually its wrappers, used to
test particular conditions.

The assert_that function is general and checks condition; if it
is not met, raises error (which is one of the Exception classes,
either a built-in or self-created), optionally using message:
>>> assert_that(2 > 1)
>>> assert_that(2 > 1, error=ValueError, message='Two is bigger than one')

assert_not is a simple wrapper to check negative conditions:
>>> txt = 'quasi-framework'
>>> txt_2 = txt.replace('-', '_')
>>> assert_not(txt == txt_2)

The other functions use this function to check a particular condition,
like length:
>>> assert_length([1, 2, 3], 3)
>>> assert_length('the SimpleAssert module', 23)

or instance:
>>> assert_instance(['string'], list)
>>> assert_instance('string', str, message='This is not a string')

or two-item comparison (for the moment working only for numbers):
>>> a, b, c = 2, 4, 2
>>> assert_comparison(a, 'less than or equal', b)
>>> assert_comparison(b, 'greater than or equal', a)
>>> assert_comparison(a, 'equal', c)

Some comments:
We thought of adding functions like assert_equal(item_1, item_2, message=None),
but we think that assert_equal(item_1, item_2) is less readable than
assert_that(item_1 == item_2) or assert_that(item_1 is item_2) (depending on
what is being asserted). The same way we did not write functions assert_unequal,
assert_greater_than and the like. The generic function assert_that(condition)
is in our opinion more readable.

The list of functions of certainly open, but such a new function must follow
all of the following conditions:
* it must be readable (easy to understand in a one-liner), and it must be more
  readable than any other function from the module  (see the above comparison of
  assert_that(item_1 == item_2) and assert_equal(item_1, item_2)
* its name must clearly convey what is being asserted
* it uses a new Exception class only if this is justified
* it returns nothing when the checked condition is passed, and it raises
  an exception otherwise
* it covers all possible situations that the assert can meet
* if atypical situations are handled, this is done in a reasonable way
  (consider how the assert_length function handles the length of numbers)
* its behavior is fully covered by tests (both doctests and pytests)

TODO: pytests need to be implemented
"""

from typing import Generator, Iterator
from comparisons import (equal,
                         less_than, lt,
                         less_than_or_equal, lte,
                         greater_than, gt,
                         greater_than_or_equal, gte,
                         get_possible_string_operators,
                         normalize_operator
                         )
from itertools import zip_longest


class LengthError(Exception):
    pass


class MultipleConditionError(Exception):
    pass


class IncorrectOperatorError(Exception):
    pass


def assert_that(condition, error=AssertionError, message=None):
    """Assert that a condition is true.

    If yes, returns nothing. If not, throws an error with optional message.
    >>> assert_that(2 > 1)
    >>> assert_that(2 < 1)
    Traceback (most recent call last):
        ...
    AssertionError
    >>> assert_that(2 < 1, error=ValueError)
    Traceback (most recent call last):
        ...
    ValueError
    >>> assert_that(2 < 1, error=ValueError, message='2 is not smaller than 1')
    Traceback (most recent call last):
        ...
    ValueError: 2 is not smaller than 1
    """
    if not condition:
        if message:
            raise error(message)
        else:
            raise error
    else:
        pass


def assert_not(condition, error=AssertionError, message=None):
    """Assert that a condition is not true.

    If yes, returns nothing. If not, throws an error with optional message.

    >>> assert_not(2 == 1)
    >>> assert_not(2 > 1)
    Traceback (most recent call last):
        ...
    AssertionError
    >>> assert_not(2 > 1, error=ValueError)
    Traceback (most recent call last):
        ...
    ValueError
    >>> assert_not(2 > 1, error=ValueError, message='2 is not smaller than 1')
    Traceback (most recent call last):
        ...
    ValueError: 2 is not smaller than 1
    """
    assert_that(not condition, error=error, message=message)


def assert_in_iterable(item, iterable, error=ValueError, message=None):
    """Assert that item is in iterable.
    
    But maybe assert_that(2 in [2, 3, 4]) is better/clearer?
    
    >>> assert_in_iterable(2, [2, 3, 4])
    """
    assert_that(item in iterable, error=error, message=message)


def assert_length(item, expected_length, condition='equal', message=None):
    """Assert that item has length of expected_length.

    If yes, returns nothing. If not, throws LengthError with optional message.
    In the case of numbers (integers, floats, complex) or a bool, it takes their length as 1.

    >>> assert_length(['string'], 1)
    >>> assert_length('string', 6)
    >>> assert_length([1, 2], 2)
    >>> assert_length(range(0, 3), 3)
    >>> assert_length(len(i for i in range(3)))
    Traceback (most recent call last):
        ...
    TypeError: object of type 'generator' has no len()
    """
    assert_that(
        condition in get_possible_string_operators(),
        error=ValueError,
        message=f'Unknown '
    )
    if isinstance(item, (int, float, complex, bool)):
        item = [item]

    condition_to_assert = compare(len(item), condition, expected_length)
    assert_that(condition_to_assert, error=LengthError, message=message)


def assert_instance(item, expected_instance, error=TypeError, message=None):
    """Assert that item has type of expected_instance.

    expected_instance can be a tuple of instances.
    If the assert is true, returns nothing. If not, throws LengthError with
    optional message.
    >>> assert_instance(['string'], list)
    >>> assert_instance('string', str)
    >>> assert_instance((1, 2), tuple)
    >>> assert_instance((1, 2), (tuple, list), message='Neither tuple nor list')
    >>> assert_instance([1, 2], (tuple, list), message='Neither tuple nor list')
    >>> assert_instance('souvenir',
    ...    (tuple, list),
    ...    message='Neither tuple nor list')
    Traceback (most recent call last):
        ...
    TypeError: Neither tuple nor list
    >>> assert_instance((i for i in range(3)), tuple)
    Traceback (most recent call last):
        ...
    TypeError
    >>> assert_instance((i for i in range(3)), tuple, message='This is not tuple.')
    Traceback (most recent call last):
        ...
    TypeError: This is not tuple.
    >>> assert_instance((i for i in range(3)), Generator)
    
    (We are doing so even though we're discouraged to use typing.Generator
    with isinstance)
    """
    assert_that(isinstance(item, expected_instance),
                error=error,
                message=message)

# This name is not clear!


def assert_multiple_that(conditions, errors=[AssertionError], messages=[None]):
    """Assert that each of at least two conditions is true.
    
    Be aware that if you provide only one error, all remaining ones will
    be AssertionError. 
    
    Throws:
        MultipleConditionError if a conditions is not a list or a tuple
        
    >>> assert_multiple_that(2 > 1)
    Traceback (most recent call last):
        ...
    assert_functions.MultipleConditionError: Require a list or tuple of conditions
    >>> assert_multiple_that(conditions=(2 > 1, 1 < 2, 2 == 2))
    >>> assert_multiple_that(conditions=(2 > 1, 1 < 2, 2 < 2))
    Traceback (most recent call last):
        ...
    AssertionError
    >>> assert_multiple_that(
    ...    conditions=(2 > 1, 1 < 2, 2 > 2),
    ...    errors=[ValueError]*3,
    ...    messages=['Wrong numeric condition.'])
    Traceback (most recent call last):
        ...
    ValueError
    >>> assert_multiple_that(
    ...    conditions=(2 > 1, 1 < 2, 2 > 2),
    ...    errors=[ValueError]*3,
    ...    messages=['Wrong numeric condition.']*3)
    Traceback (most recent call last):
        ...
    ValueError: Wrong numeric condition.
    >>> assert_multiple_that(
    ...    conditions=(2 == 1, 1 < 2, 2 > 2),
    ...    messages=['Wrong numeric condition.']*3)
    Traceback (most recent call last):
        ...
    AssertionError: Wrong numeric condition.
    """
    assert_instance(conditions,
                    (tuple, list),
                    error=MultipleConditionError,
                    message='Require a list or tuple of conditions')
    conditions_errors_messages = zip_longest(conditions,
                                             errors,
                                             messages,
                                             fillvalue=None)

    for condition, error, message in conditions_errors_messages:
        # I failed to do that in zip_longest
        # Below works, but it's not beatiful here, and not clear why
        # it's not in zip_longest but here
        if error is None:
            error = AssertionError
        assert_that(condition, error=error, message=message)


def compare(item_1, operator, item_2):
    # DOES NOT WORK FOR STRINGS! ONLY FOR NUMERIC VALUES
    """Compare item_1 and item_2 using string-formatter operator.
    
    operator is a string-like operator, working with the
    comparisons module. You can get its possible values using
    get_possible_string_operators()
    
    >>> compare(2, 'lesser than', 3)
    Traceback (most recent call last):
        ...
    assert_functions.IncorrectOperatorError: Incorrect string operator
    >>> assert compare(2, 'equal', 2)
    >>> assert compare(2, 'EQUAL', 2)
    >>> assert compare(2, 'eQuAL', 2) 
    >>> assert not compare(2, 'equal', 2.01)
    
    >>> assert compare(2, 'lt', 3)
    >>> assert compare(2, 'LT', 3)
    >>> assert compare(2, 'less_than', 3)
    >>> assert compare(2, 'less than', 3)
    >>> assert compare(2, 'Less than', 3)
    >>> assert not compare(3, 'less_than', 3)
    >>> assert not compare(3, 'less than', 3)
    >>> assert not compare(3, 'lt', 2)
    
    >>> assert compare(2, 'lte', 2)
    >>> assert compare(2, 'less_than_or_equal', 2)
    >>> assert compare(2, 'LESS_THAN_OR_EQUAL', 2)
    >>> assert compare(2, 'less than or equal', 2)
    >>> assert compare(2, 'lte', 3)
    >>> assert compare(2, 'less_than_or_equal', 3)
    >>> assert compare(2, 'less than or equal', 3)
    >>> assert not compare(2.11, 'lte', 2.100001)
    >>> assert not compare(2.11, 'less_than_or_equal', 2.100001)
    >>> assert not compare(2.11, 'less than or equal', 2.100001)
    
    >>> assert compare(3, 'gt', 2)
    >>> assert compare(3, 'greater_than', 2)
    >>> assert compare(3, 'greater than ', 2)
    >>> assert compare(3, ' Greater than', 2)
    >>> assert not compare(3, 'gt', 3)
    >>> assert not compare(3, 'greater_than', 3)
    >>> assert not compare(3, 'greater than', 3)
    >>> assert not compare(2.11, 'gt', 2.12)
    >>> assert not compare(2.11, 'greater_than', 2.12)
    >>> assert not compare(2.11, 'greater than', 2.12)
    
    >>> assert compare(2, 'gte', 2)
    >>> assert compare(2, 'greater_than_or_equal', 2)
    >>> assert compare(2, 'greater than or equal', 2)
    >>> assert compare(3, 'gte', 2)
    >>> assert compare(3, 'greater_than_or_equal', 2)
    >>> assert compare(3, 'greater than or equal', 2)
    >>> assert not compare(2.1, 'gte', 2.11)
    >>> assert not compare(2.1, 'greater_than_or_equal', 2.11)
    >>> assert not compare(2.1, 'greater than or equal', 2.11)
    """
    operator = normalize_operator(operator)
    assert_in_iterable(operator,
                       get_possible_string_operators(),
                       error=IncorrectOperatorError,
                       message='Incorrect string operator')
    return eval(f"{operator}({item_1}, {item_2})")


def assert_comparison(item_1, operator, item_2,
                      error=AssertionError,
                      message=None):
    # Is there a better name? Maybe assert_compare?
    """Assert that a direct comparison of two items is true.
    
    operator is a string-like operator, working with the
    comparisons module.
    
    >>> assert_comparison(2, 'less than', 2)
    Traceback (most recent call last):
        ...
    ValueError
    >>> assert_comparison(2, 'Equal', 2)
    >>> assert_comparison(2, 'greater than or equal', 1.1)
    
    #>>> assert_comparison('One text', 'LT', 'one text')
    #>>> assert_comparison('One text', 'less than', 'another text')
    #>>> assert_comparison('one text', 'less than', 'another text')
    
    """
    operator = normalize_operator(operator)
    assert_in_iterable(operator,
                       get_possible_string_operators(),
                       error=IncorrectOperatorError,
                       message='Incorrect string operator')
    assert_that(compare(item_1, operator, item_2),
                error=ValueError,
                message=message)

