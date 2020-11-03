"""A module for simple checks to be used within code, but also in doctesting.

The module offers simple functions to check various conditions. These
functions are to be used when you would like to use assertions in code,
something you should not do in Python. In such cases, this module comes as
handy, offering simple and readable functions to check various conditions.
But this actually does not mean that you cannot use these functions in
testing: You can do so, like in pytest testing, and the module offers aliases
of its functions specifically devoted to testing (e.g., assert_if,
assert_instance, assert_length).

What the package offers is simplicity and code readability. Instead of
raising exceptions in if-blocks, you can use devoted functions that are
easy to use, at the same time being easy to understand. These functions are
simple and easy-to-follow wrappers for checking conditions and raising the
corresponding exceptions. The idea is to keep the resulting code as clean and
readable as possible.

The main function is `check_if()`. The other functions are actually wrappers
built around it, customized to particular situations and conditions.

The `check_if()` function is general and checks a condition provided as its
argument; if it is not met, the function raises an exception (which is one of
the Exception classes, either built-in ones, or from the checkit module, or
created by you); you can optionally send a message along with the exception.
What's more, when you're using the assert expression, you're left with
AssertionError, but when using the checkit functions, you can use any exception
you want.

Consider the following example:
>>> if 1 > 0:
...    raise ValueError('One is bigger than zero')
Traceback (most recent call last):
    ...
ValueError: One is bigger than zero

The idea is to simplify this call by using
>>> check_if(0 > 1, error=ValueError, message='One is bigger than zero')
Traceback (most recent call last):
    ...
ValueError: One is bigger than zero

Of course, it's not only the brevity that we aim for, but the readability
of code. Of course, as usually, whether this approach is more readdable or not
is subjenctive, but you will see many examples that in our opinion do make
 the checkit approach more readable than the corresponding if-blocks.

If you are fine with AssertionError (actually, the only exception class
for regular asserts in Python), you can use this code:
>>> check_if(0 > 1)
Traceback (most recent call last):
    ...
AssertionError

This might be the most efficient way for debugging through quick-to-add
assertions.

You can use a check_if_not() wrapper for negative conditions:
>>> check_if_not(2 > 1, error=ValueError, message='The condition is true')
Traceback (most recent call last):
    ...
ValueError: The condition is true

Other checkit functions use this function to check a particular condition,
like length:
>>> my_list = [1, 12, 1]
>>> check_length(my_list, 3)
>>> check_length(my_list, 10, operator=le)
>>> check_length('the SimpleAssert module', 23)

You can override a Pythonic approach to treating numbers (and boolean values)
as not having length:
>>> check_length(True, 1, assign_length_to_others=True)

Note that above we used the parameter `operator`. You can use it in several
functions, and it can take nine operators from the operator module (use
`get_possible_operators()` too see their list, which is eq, le, lt, gt, ge, ne,
is_, is_not). These operators are actually functions, so you simple provide
them as function names, as we did above.

Now we want to check the instance of the following string:
>>> my_string = '_'.join(str(item) for item in [1, 2, 3])

Instead of the following if-block to check its instance:
>>> if not isinstance(my_string, str):
...    raise TypeError('A string is needed')

You do the following:
>>> check_instance(my_string, str, message='This is not a string')

If the condition is not met, it will raise TypeError:
>>> check_instance('string', list, message='List is required here')
Traceback (most recent call last):
    ...
TypeError: List is required here

You can also assert that a path exists, using
>>> check_if_paths_exist('my_file.txt')
Traceback (most recent call last):
    ...
FileNotFoundError

or that many paths exist:
>>> check_if_paths_exist(('my_file.txt', 'my_other_file.csv'))
Traceback (most recent call last):
    ...
FileNotFoundError

The module also offers two-item comparisons (for the moment working only
for numbers), again using the operator parameter:
>>> a, b, c = 2, 4, 2
>>> check_comparison(a, lt, b)
>>> check_comparison(b, gt, a)
>>> check_comparison(a, eq, c)

When you're using Python 3.8 or newer, you can use the walrus operator with
the checkit functions.

The module also offers assert-like functions, which are simply aliases of the
corresponding checkit functions: `assert_if()`, `assert_if_not()`,
`assert_instance()`, `assert_length()` and `assert_paths()`.

Comments:
We thought of adding some more functions, like
`check_if_equal(item_1, item_2, message=None)`, but we think that
`check_if_equal(item_1, item_2)` is less readable than
`check_if(item_1 == item_2)` or `check_if(item_1 is item_2)` (depending on what
is being checked). The same way we did not write functions
`check_if_unequal()`, `check_if_greater_than()` and the like. The generic
function `check_if(condition)` is in our opinion enough.

The list of functions is open and we are open to ideas, but such a new function
must follow all of the following conditions:
* it must be readable, in terms of both its code and using it in code,
  and it must be more readable than any other function from the module
  (see the above comparison of `check_if(item_1 == item_2)` and
  `check_if_equal(item_1, item_2)`) being used to check the same condition
* its name must clearly convey what is being checked; for checks, the name
  should follow the check_ convention
* it uses a new Exception class only if this is justified
* it returns nothing when the checked condition is passed, and it raises
  an exception otherwise (so it mimicks how assertions work, but offering
  the possibility to raise other exception types than AssertionError)
* it covers all possible situations that the check can meet
* if atypical situations are handled, this is done in a reasonable way; for
  instance, if it does something in an atypical way for Python (consider how
  the `check_length()` function handles the length of numbers), it does not so
  with its default behavior
* it has a well-written docstring that includes doctests
* its behavior is fully covered by tests (both doctests and pytests)
"""

import os
import sys

from operator import eq, le, lt, gt, ge, ne, is_, is_not
from collections.abc import Generator
from itertools import zip_longest
from pathlib import Path


class LengthError(Exception):
    """Exception class used by `check_length()` function."""
    pass


class OperatorError(Exception):
    """Exception class used for catching incorrect operators."""
    pass


class ComparisonError(Exception):
    """Optional exception class for check_comparison() functions.

    The default exception class for check_comparison is ValueError,
    but this class is ready for you to use in case you want to catch a
    customized error for comparisons.
    """
    pass


class ArgumentValueError(Exception):
    """New exception class to catch incorrect values of arguments.

    Normally such situations are represented by ValueError, but since
    we are checking this aspect of function calls very often, it may
    be good to use a dedicated exception. The function `check_argument()`
    uses this class as a default exception.
    """
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

    You can also make it a complex condition:
    >>> args = 33, 275, 'fifty-four'
    >>> check_if(args[0] < 50 and args[1] > 100 and isinstance(args[2], str))

    which would be better using unpacking (particularly if each element of
    the tuple has meaning):
    >>> a, b, c = args
    >>> check_if(a < 50 and b > 100 and isinstance(c, str))

    or
    >>> check_args = a < 50 and b > 100 and isinstance(c, str)
    >>> check_if(check_args)

    In such combined comparisons, you can easily use any logical operator:
    >>> check_if(
    ...    (a < 50 and b > 100) or
    ...    isinstance(c, str)
    ...    )

    This function does not use checkit checks for its arguments, since it would
    lead to infinite recursion.
    """
    _check_checkit_arguments(error=error,
                             message=message,
                             condition=condition)
    if not condition:
        _raise(error, message)


def check_if_not(condition, error=AssertionError, message=None):
    """Check if a condition is not true.

    Use this function to check if something did not happen.
    If it did not happen indeed, the function returns nothing. If it did, it throws
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

    >>> BMI = 50
    >>> disaster = True if BMI > 30 else False
    >>> check_if_not(disaster)
    Traceback (most recent call last):
        ...
    AssertionError
    """
    _check_checkit_arguments(error=error,
                             message=message,
                             condition=condition)

    check_if(not condition, error=error, message=message)


def check_length(item,
                 expected_length,
                 operator=eq,
                 error=LengthError,
                 message=None,
                 assign_length_to_others=False,
                 execution_mode='raise'):
    """Compare the length of item with expected_length, using condition.

    The operator can be from among get_possible_operators().

    If the condition is met, the function returns nothing. If not, it throws
    LengthError with an optional message. The function takes a Pythonic approach,
    treating numbers as not having length (and throwing TypeError then).
    Param assign_length_to_others lets you change this behavior, in which case
    integers, doubles floats, complex values, and bool values take length as 1.

    >>> check_length(['string'], 1)
    >>> check_length('string', 6)
    >>> check_length([1, 2], 2)
    >>> check_length(len(i for i in range(3)))
    Traceback (most recent call last):
        ...
    TypeError: object of type 'generator' has no len()
    >>> check_length(2, 1, assign_length_to_others=True)
    >>> check_length(2, 0, operator=gt, assign_length_to_others=True)
    """
    _check_checkit_arguments(error=error,
                             message=message,
                             operator=operator,
                             expected_length=expected_length,
                             assign_length_to_others=assign_length_to_others,
                             execution_mode=execution_mode)

    if assign_length_to_others:
        if isinstance(item, (int, float, complex, bool)):
            item = [item]

    condition_to_check = _compare(len(item), operator, expected_length)
    check_if(condition_to_check, error=error, message=message)


def check_instance(item, expected_instance, error=TypeError, message=None):
    """Check if item has type of expected_instance.

    The param expected_instance can be a tuple of instances. If the condition
    is true, the function returns nothing. Otherwise, it throws TypeError,
    with optional message.

    If you want to check if the item is None, you can do so in two ways:
    >>> my_none_object = None
    >>> check_if(my_none_object is None, error=TypeError)

    or
    >>> check_instance(my_none_object, None)

    The former approach is Pythonic while the latter less so, but we keep this
    functionality so that you can use the check_instance function also for
    None objects.

    >>> check_instance(['string'], list)
    >>> check_instance('string', str)
    >>> check_instance((1, 2), tuple)
    >>> check_instance([1, 2], (tuple, list),
    ...                           message='Neither tuple nor list')
    >>> check_instance('souvenir',
    ...                   (tuple, list),
    ...                   message='Neither tuple nor list')
    Traceback (most recent call last):
        ...
    TypeError: Neither tuple nor list
    >>> check_instance((i for i in range(3)), tuple)
    Traceback (most recent call last):
        ...
    TypeError
    >>> check_instance((i for i in range(3)), tuple, message='This is not tuple.')
    Traceback (most recent call last):
        ...
    TypeError: This is not tuple.
    >>> check_instance((i for i in range(3)), Generator)

    You can include None:
    >>> check_instance('a', (str, None))
    >>> check_instance(None, expected_instance=(str, None))

    """
    _check_checkit_arguments(error=error,
                             message=message,
                             expected_instance=expected_instance)

    if expected_instance is None:
        check_if(item is None,
                 error=error,
                 message=message
                 )
        return None

    if isinstance(expected_instance, (list, tuple)):
        if any(i is None for i in expected_instance):
            if item is None:
                return None
            else:
                expected_instance = tuple(i
                                          for i in expected_instance
                                          if i is not None)
    check_if(isinstance(item, expected_instance),
             error=error,
             message=message)


def check_if_paths_exist(paths,
                         error=FileNotFoundError,
                         message=None,
                         execution_mode='raise'):
    """Check if paths exists, and if not even raise error or return.

    Param paths is either a string or a list/tuple.

    The function's behavior depends on execution_mode. If you want to learn which
    paths do not exist, choose execution_mode='return', in which case you will get
    True if all the files exist, and a tuple of False, error(message),
    paths (the last item being non-existing paths).

    >>> check_if_paths_exist('Q:/Op/Oop/')
    Traceback (most recent call last):
        ...
    FileNotFoundError
    >>> check_if_paths_exist(os.listdir()[0])
    >>> check_if_paths_exist(os.listdir())

    >>> check_if_paths_exist('Q:/Op/Oop/', execution_mode='return')
    (FileNotFoundError(), 'Q:/Op/Oop/')
    >>> check_if_paths_exist(os.listdir()[0], execution_mode='return')
    (None, None)
    >>> check_if_paths_exist(os.listdir(), execution_mode='return')
    (None, [])
    """
    _check_checkit_arguments(error=error,
                             message=message,
                             execution_mode=execution_mode)

    if isinstance(paths, str):
        path = Path(paths)
        if execution_mode == 'raise':
            check_if(path.exists(), error=error, message=message)
        else:
            file_exists = path.exists()
            if not file_exists:
                return _return_from_check_if_paths_exist(error, message, paths)
            else:
                return None, None
    elif isinstance(paths, (tuple, list)):
        paths_exist = [Path(path).exists() for path in paths]
        if not all(paths_exist):
            non_existing_paths = [
                path for path in paths
                if not Path(path).exists()
            ]
            if execution_mode == 'raise':
                _raise(error, message)
            elif execution_mode == 'return':
                return _return_from_check_if_paths_exist(error, message, non_existing_paths)
        else:
            if execution_mode == 'return':
                return None, []
    else:
        raise TypeError('Argument paths must be string, tuple of strigs, or list of strings')


def _return_from_check_if_paths_exist(error, message, paths):
    """
    >>> _return_from_check_if_paths_exist(
    ...    error=FileNotFoundError,
    ...    message=None,
    ...    paths=[])
    (FileNotFoundError(), [])
    >>> _return_from_check_if_paths_exist(
    ...    error=FileNotFoundError,
    ...    message='No such file',
    ...    paths='D:/this_dir/this_path.csv') # doctest: +ELLIPSIS
    (FileNotFoundError('No such file'...
    """
    _check_checkit_arguments(error=error)

    if message:
        return error(str(message)), paths
    else:
        return error(), paths


def check_comparison(item_1, operator, item_2,
                     error=ValueError,
                     message=None):
    """Check if a comparison of two items is true.

    The operator should be from get_possible_operators().

    >>> check_comparison(2, lt, 2)
    Traceback (most recent call last):
        ...
    ValueError
    >>> check_comparison(2, eq, 2)
    >>> check_comparison(2, ge, 1.1)
    >>> check_comparison('One text', lt, 'one text')
    >>> check_comparison('One text', lt, 'another text')
    >>> check_comparison('one text', lt, 'another text')
    Traceback (most recent call last):
        ...
    ValueError

    You can use a dedicated ComparisonError (from this module):
    >>> check_comparison('one text', lt, 'another text',
    ...                  error=ComparisonError,
    ...                  message='Not less!')
    Traceback (most recent call last):
        ...
    checkit.ComparisonError: Not less!

    Style suggestion:
        Surely, use coding style you prefer, but in our opinion you can
        increase the readability of your code using the following style
        (in case you need to split the function call into more lines,
        which is when you need to change the last two parameters):
        >>> check_comparison(
        ...    'one text', lt, 'another text',
        ...    error = ComparisonError,
        ...    message='Comparison condition violated'
        ...    )
        Traceback (most recent call last):
            ...
        checkit.ComparisonError: Comparison condition violated

        The idea is to keep the first three arguments in one line, so that
        the comparison can be read like text: 2, greater_than, 0; or
        this_text, equal, example_text; etc.
    """
    check_if(operator in get_possible_operators(),
             error=OperatorError,
             message='Incorrect operator')
    check_if(_compare(item_1, operator, item_2),
             error=error,
             message=message)


def check_all_ifs(*args):
    """Check all multiple conditions and return all checks.

    If you want to check several conditions, you can simply check them
    line by line. Use this function if you want to check each condition
    and catch all the errors (and messages) - it does not behave like
    the other functions of the module, since it returns the results
    of the checks.

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
             when you did not provide the message, and ...???

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
    >>> check_all_ifs( # doctest: +ELLIPSIS
    ...    (check_if, 2 > 1),
    ...    (check_if_not, 'a' == 'a', ValueError, 'Wrong!')
    ...    )
    {'1: check_if': True, '2: check_if_not': ValueError(\'Wrong!...

    Style suggestion:
        Use coding style you prefer, but in our opinion you can increase
        the readability of your code using the style we used above, that
        is, presenting all the independent conditions in a separate line,
        unless the call is short if presented in one line.
    """
    check_length(args, 0, gt,
                 ValueError,
                 'Provide at least one condition.')
    tuple_error_message = (
        'Provide all function calls as tuples in the form of '
        '(check_function, *args)'
    )
    for arg in args:
        check_instance(arg,
                       tuple,
                       message=tuple_error_message)

    results_of_checks = dict()
    for i, this_check in enumerate(args):
        function, *arguments = this_check
        try:
            run_this_check = function(*arguments)
            run_this_check = True
        except Exception as e:
            run_this_check = e

        results_of_checks[f'{i + 1}: {function.__name__}'] = run_this_check

    return results_of_checks


def check_argument(argument,
                   argument_name=None,
                   expected_instance=None,
                   expected_choices=None,
                   expected_length=None,
                   expected_condition=None,
                   error=ArgumentValueError,
                   message=None,
                   **kwargs):
    """Check if the user provided a correct argument value.

    Use this function to check if the value the user provided is in the list
    of choices; a common situation is to check if an argument the user provided
    to the function is correct. If yes, nothing happens; if not, the function
    raises error with a default message that depends on what is happening.

    The argument_name param is the actual name of the argument in function,
    which normally will be just a string of the argument (see below examples).
    You can skip it, in which case the error messages will not include the
    name of the argument but will inform about 'argument'.

    The function performs lazy checking, meaning that it first checks the
    instance (if provided), then choices (if provided), then expected length
    (if provided), and finally condition (if provided). But they must not raise
    a built-in error, because it will be raised before the check is performed.
    For example, the below will not work because of the ValueError, resulting
    from an attempt to apply the `int()` function to a string:

    >>> x = 'one'
    >>> check_argument(
    ...    x, 'x',
    ...    expected_instance=int,
    ...    expected_condition=int(x) % 2 == 0)
    Traceback (most recent call last):
        ...
    ValueError: invalid literal for int() with base 10: 'one'

    The expected_condition, however, must actually include also the argument
    itself, like below:
    >>> x = 5
    >>> check_argument(x, 'x', expected_condition=x in range(0, 10))
    >>> def foo(x):
    ...    check_argument(x, 'x', expected_choices=('first choice',
    ...                                             'second_choice'))
    ...    # whatever foo is doing...
    >>> foo('first choice')
    >>> foo('no choice')
    Traceback (most recent call last):
        ...
    checkit.ArgumentValueError: x's value, no choice, is not among valid \
values: ('first choice', 'second_choice').

    >>> x = 2; check_argument(x, 'x', expected_condition=x % 2 == 0)
    >>> x = 3; check_argument(x, 'x', expected_condition=x % 2 == 0)
    Traceback (most recent call last):
        ...
    checkit.ArgumentValueError: Provided condition violated for x

    You can provide your own message, though:
    >>> check_argument(
    ...    x, 'x',
    ...    expected_condition=x % 2 == 0,
    ...    message='Wrong, my friend!')
    Traceback (most recent call last):
        ...
    checkit.ArgumentValueError: Wrong, my friend!

    >>> x = 2.0
    >>> check_argument(
    ...    x, 'x',
    ...    expected_instance=int,
    ...    expected_condition=int(x) % 2 == 0)
    Traceback (most recent call last):
        ...
    checkit.ArgumentValueError: Incorrect instance of x;\
 valid instance(s): <class 'int'>

    >>> x = 3
    >>> check_argument(
    ...    x, 'x',
    ...    expected_instance=int,
    ...    expected_condition=int(x) % 2 == 0)
    Traceback (most recent call last):
        ...
    checkit.ArgumentValueError: Provided condition violated for x

    This is how you can check Exceptions and errors provided as arguments:
    >>> assert check_argument(
    ...    TypeError, 'error_arg',
    ...    expected_instance=type) is None
    >>> assert check_argument(
    ...    TypeError(), 'error_arg',
    ...    expected_instance=Exception) is None

    You can also define quite complex checks:
    >>> def check_glm_args(glm_args):
    ...    return (
    ...        isinstance(glm_args[0], (int, float)) and
    ...        glm_args[0] > 0 and
    ...        glm_args[0] <= 1 and
    ...        isinstance(glm_args[1], str) and
    ...        isinstance(glm_args[2], str) and
    ...        glm_args[1] in ('poisson', 'quasi-poisson') and
    ...        glm_args[2] in ('log', 'identity')
    ...     )
    >>> glm_args = 1, 'quasi-poisson', 'log'
    >>> check_argument(
    ...    argument_name='glm_args',
    ...    argument=glm_args,
    ...    expected_instance=tuple,
    ...    expected_condition=check_glm_args(glm_args))
    >>> glm_args = 1., 'quasi-poisson', 'logit'
    >>> check_argument(
    ...    argument_name='glm_args',
    ...    argument=glm_args,
    ...    expected_instance=tuple,
    ...    expected_condition=check_glm_args(glm_args))
    Traceback (most recent call last):
        ...
    checkit.ArgumentValueError: Provided condition violated for glm_args
    """
    if all(item is None
           for item in (expected_instance,
                        expected_choices,
                        expected_length,
                        expected_condition)):
        raise ValueError('check_argument() requires at least one condition'
                         ' to be checked')

    if argument_name is None:
        argument_name = 'argument'
    check_instance(argument_name, str, message='argument_name must be string')

    if expected_instance is not None:
        instance_message = _make_message(
            message,
            (f'Incorrect instance of {argument_name}; valid instance(s):'
             f' {expected_instance}'))
        check_instance(item=argument,
                       expected_instance=expected_instance,
                       error=error,
                       message=instance_message)
    if expected_choices is not None:
        choices_message = _make_message(
            message,
            (f'{argument_name}\'s value, {argument}, '
             f'is not among valid values: {expected_choices}.'))
        check_if(argument in expected_choices,
                 error=error,
                 message=choices_message)
    if expected_length is not None:
        length_message = _make_message(
            message,
            (f'Unexpected length of {argument_name}'
             f' (should be {expected_length})'))
        check_length(item=argument,
                     expected_length=expected_length,
                     error=error,
                     message=length_message,
                     **kwargs
                     )
    if expected_condition is not None:
        condition_message = _make_message(
            message,
            f'Provided condition violated for {argument_name}')
        check_if(expected_condition,
                 error=error,
                 message=condition_message)


def _make_message(message_provided, message_otherwise):
    """
    >>> _make_message(None, 'Otherwise')
    'Otherwise'
    >>> _make_message('Provided', 'Otherwise')
    'Provided'
    """
    return message_provided if message_provided else message_otherwise


def catch_check(check_function, *args, **kwargs):
    """Catch exception raised by checkit functions.

    Most checkit functions return None when the check is fine and raise
    an exception otherwise. You can use this function to change this behavior:
    It still returns None when everything is fine, but instead of raising
    the exception in case of problems, it returns this exception.

    Note the particular behavior. Since the function returns

    >>> catch_check(check_if, 2==2)
    >>> catch_check(check_if, 2>2)
    AssertionError()
    >>> my_check = catch_check(check_if, 2>2, ValueError)
    >>> my_check
    ValueError()
    >>> type(my_check)
    <class 'ValueError'>
    >>> check_instance(my_check, ValueError)
    >>> raise(my_check)
    Traceback (most recent call last):
        ...
    ValueError
    >>> print(my_check)
    <BLANKLINE>
    >>> catch_check(check_if, condition=2>2, error=ValueError)
    ValueError()
    >>> catch_check(check_length, [2, 2], 3)
    LengthError()
    >>> my_check = catch_check(
    ...    check_instance, 25, float, ValueError, 'This is no float!')
    >>> my_check # doctest: +ELLIPSIS
    ValueError('This is no float!'...
    >>> print(str(my_check))
    This is no float!
    >>> my_check = catch_check(check_instance, 'a', int)
    >>> my_check
    TypeError()
    >>> raise(my_check)
    Traceback (most recent call last):
        ...
    TypeError
    """
    check_if(hasattr(check_function, '__call__'),
             error=TypeError,
             message=(f'{check_function} does not '
                      'seem to be a checkit function')
             )
    check_if_not(check_function == check_all_ifs,
                 error=ValueError,
                 message=('Do not use catch_check for check_all_ifs() '
                          'because it returns its checks.')
                 )
    paths_condition = (
        check_function == check_if_paths_exist and
        ('return' in args or 'execution_mode' in kwargs.keys())
    )
    check_if_not(paths_condition,
                 error=ValueError,
                 message=('Do not use catch_check for check_if_paths_exist() '
                          'with execution_mode="return" because it returns '
                          'its checks.')
                 )
    check_argument(
        argument=check_function,
        argument_name=check_function.__name__,
        expected_choices=(
            check_if,
            check_if_not,
            check_argument,
            check_comparison,
            check_if_paths_exist,
            check_instance,
            check_length,
        ),
        message=(f'{check_function.__name__} is not'
                 ' among acceptable valid checkit functions')
    )
    try:
        check_function(*args, **kwargs)
        return None
    except Exception as e:
        return e


def _compare(item_1, operator, item_2):
    """Compare item_1 and item_2 using operator.

    The operator should be from get_possible_operators().
    Returns True if the comparison is valid and False otherwise.

    >>> _compare(2, eq, 2)
    True
    >>> _compare(2, eq, 2.01)
    False
    >>> _compare(2.11, le, 2.100001)
    False
    >>> _compare(2.11, le, 2.100001)
    False
    >>> _compare(2, ge, 2)
    True
    >>> _compare(2.1, ge, 2.11)
    False
    """
    check_if(
        operator in get_possible_operators(),
        error=OperatorError,
        message='Incorrect operator'
    )
    return operator(item_1, item_2)


def _clean_message(message):
    """Clear message returned along with error.

    >>> _clean_message('"Incorrect argument")')
    'Incorrect argument'
    >>> _clean_message('"This is testing message (because why not).")')
    'This is testing message (because why not).'
    """
    if isinstance(message, str):
        message = (message)[:-1].replace('"', '')
    elif isinstance(message, (tuple, list)):
        if not all(isinstance(item, str) for item in message):
            raise TypeError(r'message must be string or tuple/list of strings')
        message = '('.join(message)[:-1].replace('"', '')
    else:
        raise TypeError(r'message must be string or tuple/list of strings')
    if message == '':
        message = None
    return message


def _parse_error_and_message_from(error_and_message):
    """Get error and message from one string.

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


def _raise(error, message=None):
    """Raise error with or without message.

    >>> _raise(ValueError)
    Traceback (most recent call last):
       ....
    ValueError

    >>> _raise(TypeError)
    Traceback (most recent call last):
       ....
    TypeError

    >>> _raise(TypeError, 'Incorrect type')
    Traceback (most recent call last):
       ....
    TypeError: Incorrect type
    """
    if message is None:
        raise error
    else:
        check_instance(message, str, message='message must be string')
        raise error(message)


def _check_checkit_arguments(error=None,
                             message=None,
                             condition=None,
                             operator=None,
                             assign_length_to_others=None,
                             execution_mode=None,
                             expected_length=None,
                             expected_instance=None):
    """Check common arguments in checkit functions.

    The check does use use checkit functions but standard if-conditions
    (for instance, to avoid recursions, but also to ensure that the checks
    are done using a standard-library-based approach).
    Other arguments should be checked using other ways.

    >>> _check_checkit_arguments(error=LengthError)
    >>> _check_checkit_arguments(error=ValueError)
    >>> _check_checkit_arguments(error=ValueError())
    >>> _check_checkit_arguments(error=LengthError, message=False)
    Traceback (most recent call last):
        ...
    TypeError: message must be either None or string
    >>> _check_checkit_arguments(error=ValueError, condition=2<1)
    """
    if all(argument is None
           for argument
           in (error,
               message,
               condition,
               operator,
               assign_length_to_others,
               execution_mode,
               expected_length,
               expected_instance)):
        raise ValueError('Provide at least one argument')
    if error is not None:
        try:
            if not isinstance(error, Exception):
                if (not isinstance(error(), Exception)):
                    raise TypeError('error must be an exception')
        except:
            raise TypeError('error must be an exception')
    if message is not None:
        if not isinstance(message, str):
            raise TypeError('message must be either None or string')
    if condition is not None:
        if not isinstance(condition, bool):
            raise ValueError('The condition does not give a True/False answer')
    if operator is not None:
        if operator not in get_possible_operators():
            raise OperatorError(
                'Unacceptable operator. Check get_possible_operators()')
    if expected_length is not None:
        if not isinstance(expected_length, (int, float)):
            raise TypeError(
                'expected_length should be an integer (or a float)')
    if assign_length_to_others is not None:
        if not isinstance(assign_length_to_others, bool):
            raise TypeError('assign_length_to_others should be a bool')
    if execution_mode is not None:
        if not execution_mode in ('raise', 'return'):
            raise ValueError(
                'execution_mode should be either "raise" or "return"')
    if expected_instance is not None:
        if not isinstance(expected_instance, (tuple, list)):
            if not isinstance(expected_instance, type):
                raise TypeError('expected_instance must be a valid type')
        else:
            expected_instance = [i for i in expected_instance if i is not None]
            for instance in expected_instance:
                if not isinstance(instance, type):
                    raise TypeError(
                        'all items in expected_instance must be valid types')


assert_if = check_if
assert_if_not = check_if_not
assert_length = check_length
assert_instance = check_instance
assert_paths = check_if_paths_exist


def get_possible_operators():
    """
    >>> operators = get_possible_operators()
    >>> type(operators[0])
    <class 'builtin_function_or_method'>
    >>> len(operators)
    8
    """
    return eq, le, lt, gt, ge, ne, is_, is_not
