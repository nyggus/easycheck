"""A module for simple checks to be used outside of testing.

The module offers very simple functions to check various conditions. These
functions are to be used when one would like to use assertions in code,
which we should not do in Python. In such cases, this module comes as
helpful, offering simple and readable functions to check various condutions.

They do not offer much new functionality over raising exceptions when
a particular condition is violated. Rather, they offer simple and easy to
understand wrappers for checking conditions and raising the corresponding
exceptions. The idea was to keep code clean and readable.

The main function is check_if, which in fact could be enough for all
checks. The other functions are actually its wrappers, used to
test particular conditions.

The check_if function is general and checks condition; if it
is not met, raises error (which is one of the Exception classes,
either a built-in or self-created), optionally using message.

For example:
>>> check_if(0 > 1, error=ValueError, message='One is bigger than zero')
Traceback (most recent call last):
    ...
ValueError: One is bigger than zero

You can use check_if_not, a simple wrapper for negative conditions:
>>> check_if_not(2 > 1,
...    error=ValueError,
...    message='The condition is true')
Traceback (most recent call last):
    ...
ValueError: The condition is true

The other functions use this function to check a particular condition,
like length:
>>> my_list = [1, 12, 1]
>>> check_length(my_list, 3)
>>> check_length(my_list, 10, operator=less_than_or_equal)
>>> check_length('the SimpleAssert module', 23)

You can override a Pythonic approach to treating numbers (and boolean values)
as not having length:
>>> check_length(True, 1, assign_length_to_numbers=True)

Instead of the following if-block to check the instance:
>>> my_string = '_'.join(str(item) for item in [1, 2, 3])
>>> if not isinstance(my_string, str):
...    raise TypeError('A string is needed')
>>> check_if_instance(my_string, str, message='This is not a string')
>>> check_if_instance('string', list, message='List is required here')
Traceback (most recent call last):
    ...
TypeError: List is required here

The module also offers two-item comparisons (for the moment working only for numbers):
>>> a, b, c = 2, 4, 2
>>> check_comparison(a, less_than_or_equal, b)
>>> check_comparison(a, lte, b)
>>> check_comparison(b, greater_than_or_equal, a)
>>> check_comparison(b, gte, a)
>>> check_comparison(a, equal, c)

Some comments:
We thought of adding functions like check_if_equal(item_1, item_2, message=None),
but we think that check_if_equal(item_1, item_2) is less readable than
check_if(item_1 == item_2) or check_if(item_1 is item_2) (depending on
what is being checked). The same way we did not write functions check_if_unequal,
check_if_greater_than and the like. The generic function check_if(condition)
is in our opinion more readable.

The list of functions of certainly open, but such a new function must follow
all of the following conditions:
* it must be readable (easy to understand in a one-liner), and it must be more
  readable than any other function from the module  (see the above comparison of
  check_if(item_1 == item_2) and check_if_equal(item_1, item_2)
* its name must clearly convey what is being checked
* it uses a new Exception class only if this is justified
* it returns nothing when the checked condition is passed, and it raises
  an exception otherwise
* it covers all possible situations that the check can meet
* if atypical situations are handled, this is done in a reasonable way
  (consider how the check_length function handles the length of numbers)
* its behavior is fully covered by tests (both doctests and pytests)

TODO: pytests need to be implemented
"""

from comparisons import (equal,
                         less_than, lt,
                         less_than_or_equal, lte,
                         greater_than, gt,
                         greater_than_or_equal, gte,
                         get_possible_operators,
                         get_possible_string_operators,
                         normalize_operator
                         )
from collections.abc import Generator
from itertools import zip_longest


class LengthError(Exception):
    pass


class MultipleConditionError(Exception):
    pass


class IncorrectOperatorError(Exception):
    pass


def check_if(condition, error=AssertionError, message=None):
    """Check if a condition is true.

    If yes, returns nothing. If not, throws an error with optional message.
    This is a generic function, used by other functions of the module.
    >>> check_if(2 > 1)
    >>> check_if(2 < 1)
    Traceback (most recent call last):
        ...
    AssertionError
    >>> check_if(2 < 1, error=ValueError, message='2 is not smaller than 1')
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


def check_if_not(condition, error=AssertionError, message=None):
    """Check if a condition is not true.

    Use this function to chekc if something did not happen.
    If it did, the function returns nothing. If it did not, it throws
    an error with an optional message.
    >>> check_if_not(2 == 1)
    >>> check_if_not(2 > 1)
    Traceback (most recent call last):
        ...
    AssertionError
    >>> check_if_not(2 > 1, error=ValueError, message='2 is not smaller than 1')
    Traceback (most recent call last):
        ...
    ValueError: 2 is not smaller than 1
    """
    check_if(not condition, error=error, message=message)


def check_length(item,
                 expected_length,
                 operator=equal,
                 message=None,
                 assign_length_to_numbers=False):
    """Compare the length of item with expected_length, using condition.

    The operator can be from among get_possible_operators().

    If the condition is met, the function returns nothing. If not, it throws
    LengthError with optional message. The function takes a Pythonic approach,
    treating numbers as not having length. Param assign_length_to_numbers lets
    you change this behavior, in which case integers, doubles floats,
    complex values, and bool values take length as 1.

    >>> check_length(['string'], 1)
    >>> check_length('string', 6)
    >>> check_length([1, 2], 2)
    >>> check_length(len(i for i in range(3)))
    Traceback (most recent call last):
        ...
    TypeError: object of type 'generator' has no len()
    >>> check_length(2, 1, assign_length_to_numbers=True)
    >>> check_length(2, 0, operator=gt, assign_length_to_numbers=True)
    """
    check_if(
        operator in get_possible_operators(),
        error=IncorrectOperatorError,
        message=f'Unknown operator'
    )
    if assign_length_to_numbers:
        if isinstance(item, (int, float, complex, bool)):
            item = [item]

    condition_to_check = compare(len(item), operator, expected_length)
    check_if(condition_to_check, error=LengthError, message=message)


def check_if_instance(item, expected_instance, error=TypeError, message=None):
    """Check if item has type of expected_instance.

    expected_instance can be a tuple of instances.
    If the condition is true, the function returns nothing. Otherwise, it throws
    LengthError with optional message.
    >>> check_if_instance(['string'], list)
    >>> check_if_instance('string', str)
    >>> check_if_instance((1, 2), tuple)
    >>> check_if_instance((1, 2), (tuple, list), message='Neither tuple nor list')
    >>> check_if_instance([1, 2], (tuple, list), message='Neither tuple nor list')
    >>> check_if_instance(
    ...    'souvenir',
    ...    (tuple, list),
    ...    message='Neither tuple nor list')
    Traceback (most recent call last):
        ...
    TypeError: Neither tuple nor list
    >>> check_if_instance((i for i in range(3)), tuple)
    Traceback (most recent call last):
        ...
    TypeError
    >>> check_if_instance((i for i in range(3)), tuple, message='This is not tuple.')
    Traceback (most recent call last):
        ...
    TypeError: This is not tuple.
    >>> check_if_instance((i for i in range(3)), Generator)
    """
    check_if(isinstance(item, expected_instance),
             error=error,
             message=message)


def compare(item_1, operator, item_2):
    """Compare item_1 and item_2 using operator.

    operator should be from get_possible_operators().

    >>> compare(2, equal, 2)
    True
    >>> compare(2, equal, 2.01)
    False
    >>> compare(2.11, lte, 2.100001)
    False
    >>> compare(2.11, less_than_or_equal, 2.100001)
    False
    >>> compare(2, gte, 2)
    True
    >>> compare(2.1, greater_than_or_equal, 2.11)
    False
    """
    check_if(operator in get_possible_operators(),
             error=IncorrectOperatorError,
             message='Incorrect operator')
    return operator(item_1, item_2)


def check_comparison(item_1, operator, item_2,
                     error=ValueError, message=None):
    """Check if a comparison two items is true.
        
    operator should be from get_possible_operators().
    
    >>> check_comparison(2, less_than, 2)
    Traceback (most recent call last):
        ...
    ValueError
    >>> check_comparison(2, equal, 2)
    >>> check_comparison(2, greater_than_or_equal, 1.1)
    
    >>> check_comparison('One text', lt, 'one text')
    >>> check_comparison('One text', less_than, 'another text')
    >>> check_comparison('one text', less_than, 'another text')
    Traceback (most recent call last):
        ...
    ValueError
    """
    check_if(operator in get_possible_operators(),
             error=IncorrectOperatorError,
             message='Incorrect operator')
    check_if(compare(item_1, operator, item_2),
             error=error,
             message=message)


def _clean_message(message):
    """
    >>> _clean_message('"Incorrect argument")')
    'Incorrect argument'
    >>> _clean_message('"This is testing message (because why not).")')
    'This is testing message (because why not).'
    """
    if isinstance(message, str):
        message = (message)[:-1].replace('"', '')
    elif isinstance(message, (tuple, list)):
        message = '('.join(message)[:-1].replace('"', '')
    if message == '':
        message = None
    return message


def _parse_error_and_message_from(error_and_message):
    """
    >>> error_and_message = (
    ...    'TypeError("Incorrect argument")'
    ...    )
    >>> _parse_error_and_message_from(error_and_message)
    ('TypeError', 'Incorrect argument')
    >>> error_and_message = 'ValueError'
    >>> _parse_error_and_message_from(error_and_message)
    ('ValueError', None)
    """
    if not error_and_message:
        return None
    splitted_error_and_message = error_and_message.split('(')
    error, *message = splitted_error_and_message
    message = _clean_message(message)
    return error, message


def check_all_ifs(*args):
    """Check all multiple conditions and return all checks.

    If you want to check several conditions, you can simply check them
    line by line. Use this function if you want to check each condition
    and catch all the errors (and messages).
    
    The args are to be a list of tuples of the form
    (check_function, *args, **kwargs), where args and kwargs are
    positional and keyword arguments to be passed to check_function;
    check_function is any of the check functions from this module (that is,
    any of the functions starting off with check_).
    
    Returns: A dict with the results, of the following (example) structure:
             {'1: check_if': True, '2: check_if': True}
             This means that two checks were run, both using check_if, and
             both were returned confirmation (so no exception was raised).
             In case of an exception raised, the resulting dict gets the
             following structure:
             {'1: check_if': True, '2: check_if_not': AssertionError()}
             when you did not provide the message, and
             

    
    >>> check_all_ifs(
    ...    (check_if, 2 > 1),
    ...    (check_if, 'a' == 'a')
    ...    )
    {'1: check_if': True, '2: check_if': True}
    >>> check_all_ifs(
    ...    (check_if, 2 > 1),
    ...    (check_if_not, 'a' == 'a')
    ...    )
    {'1: check_if': True, '2: check_if_not': AssertionError()}
    >>> check_all_ifs(
    ...    (check_if, 2 > 1),
    ...    (check_if_not, 'a' == 'a', ValueError, 'Wrong!')
    ...    )
    {'1: check_if': True, '2: check_if_not': aAssertionError()}
    
    """
    tuple_error_message = (
        'Provide all function calls as tuples in the form of '
        '(check_function, *args).'
    )
    for arg in args:
        check_if_instance(arg,
                          tuple,
                          message=tuple_error_message)

    results_of_checks = dict()

    for i, this_check in enumerate(args):
        function, *arguments = this_check
        print('arguments', arguments)
        try:
            run_this_check = function(arguments)
            run_this_check = True
        except Exception as e:
            run_this_check = e

        results_of_checks[f'{i + 1}: {function.__name__}'] = run_this_check

    return results_of_checks


def check_if_in_iterable(item, iterable, error=ValueError, message=None):
    # TO BE REMOVED: check_if(2 in [2, 3, 4]) is clearer and more readable
    """Check if item is in iterable.

    >>> check_if_in_iterable(2, [2, 3, 4])
    """
    check_if(item in iterable, error=error, message=message)

