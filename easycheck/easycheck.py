"""A module for simple checks to be used within code and testing.

The easycheck module offers simple functions to check conditions and either raise
an exception or issue a warning if the condition is violated; otherwise,
nothing happens (the function returns None). You can either choose default
exceptions and messages (or no message) or customize them. Unlike the assertion
expression, you can use easycheck functions within code.

The module also offers aliases to be used in testing, all of which have the
word "assert" in their names (assert_if(), assert_if_not(),
assert_instance(), assert_length(), and assert_path()).
"""
import os
import warnings
from collections.abc import Generator, Iterable, Callable
from operator import eq, le, lt, gt, ge, ne, is_, is_not
from pathlib import Path


class LengthError(Exception):
    """Exception class used by the check_length() function."""
    pass


class OperatorError(Exception):
    """Exception class used for catching incorrect operators."""
    pass


class ComparisonError(Exception):
    """Optional exception class for the check_comparison() function.

    The default exception class for check_comparison() is ValueError, but
    this class is ready for you to use in case you want to catch a customized
    error for comparison purposes.
    """
    pass


class ArgumentValueError(Exception):
    """Exception class to catch incorrect values of arguments.

    Normally such situations are represented by ValueError, but since we are
    checking this aspect of function calls very often, it may be good to use
    a dedicated exception. The function check_argument() uses this class as
    a default exception.
    """
    pass


def check_if(condition, handle_with=AssertionError, message=None):
    """Check if a condition is true.

    Args:
        condition (bool): condition to check.
        handle_with (type): the type of exception to be raised or warning to
            be issued
        message (str): a text to use as the exception/warning message

    Returns:
        None, if check succeeded.

    Raises:
        Exception of the type provided by the handle_with parameter,
        AssertionError by default (unless handle_with is a warning).

    >>> check_if(2 > 1)
    >>> check_if(2 < 1)
    Traceback (most recent call last):
        ...
    AssertionError
    >>> check_if(2 < 1,
    ...    handle_with=ValueError,
    ...    message='2 is not smaller than 1')
    Traceback (most recent call last):
        ...
    ValueError: 2 is not smaller than 1

    with its shorter version of
    >>> check_if(2 < 1, ValueError, '2 is not smaller than 1')
    Traceback (most recent call last):
        ...
    ValueError: 2 is not smaller than 1

    You can also make the condition a complex condition:
    >>> args = 33, 275, 'fifty-four'
    >>> check_if(args[0] < 50 and args[1] > 100 and isinstance(args[2], str))

    This might be more readable using unpacking (particularly if each element
    of the tuple has meaning):
    >>> a, b, c = args
    >>> check_if(a < 50 and b > 100 and isinstance(c, str))

    or
    >>> check_args = a < 50 and b > 100 and isinstance(c, str)
    >>> check_if(check_args)

    In such combined comparisons, you can easily use any logical operator:
    >>> check_if((a < 50 and b > 100) or isinstance(c, str))

    To issue a warning, use the Warning class or its subclass:
    >>> check_if(2 < 1, handle_with=Warning, message='2 is not smaller than 1')

    or shorter
    >>> check_if(2 < 1, Warning, '2 is not smaller than 1')

    """
    _check_easycheck_arguments(handle_with=handle_with,
                             message=message,
                             condition=condition)
    if not condition:
        _raise(handle_with, message)


def check_if_not(condition, handle_with=AssertionError, message=None):
    """Check if a condition is not true.

    Args:
        condition (bool): condition to check.
        handle_with (type): the type of exception or warning to be raised
        message (str): a text to use as the exception/warning message

    Returns:
        None, if check succeeded.

    Raises:
        Exception of the type provided by the handle_with parameter,
        AssertionError by default (unless handle_with is a warning).

    You would normally use these functions in situations like these: This is
    engine speed in the object engine_speed:
    >>> engine_speed = 5900

    In this case, assume that if this value is higher than 6000, than this
    situation may cause problems. So, let us check this:
:
    >>> check_if_not(engine_speed > 6000, ValueError, 'Danger!')

    Sure, you can do so using the check_if() function, like here:
    >>> check_if(engine_speed <= 6000, ValueError, 'Danger!')

    and both are fine. You simply have two functions to choose from in order to
    make the code as readable as you want. Sometimes the negative version
    sounds more natural, and so it's all about what kind of language you want
    to use in this particular situation.

    Consider the examples below:
    >>> check_if_not(2 == 1)
    >>> check_if_not(2 > 1)
    Traceback (most recent call last):
        ...
    AssertionError
    >>> check_if_not(2 > 1, ValueError, '2 is not smaller than 1')
    Traceback (most recent call last):
        ...
    ValueError: 2 is not smaller than 1

    >>> BMI = 50
    >>> disaster = True if BMI > 30 else False
    >>> check_if_not(disaster, message='BMI disaster! Watch out for candies!')
    Traceback (most recent call last):
        ...
    AssertionError: BMI disaster! Watch out for candies!

    To issue a warning, use the Warning class or one of its subclasses:
    >>> check_if_not(2 > 1, Warning, '2 is not bigger than 1')
    """
    _check_easycheck_arguments(handle_with=handle_with,
                             message=message,
                             condition=condition)

    check_if(not condition, handle_with=handle_with, message=message)


def check_length(item,
                 expected_length,
                 handle_with=LengthError,
                 message=None,
                 operator=eq,
                 assign_length_to_others=False):
    """Compare item's length with expected_length, using operator.

    Args:
        item: the object whose type we want to validate
        expected_length (int): the expected type of the item
        handle_with (type): the type of exception or warning to be raised
        message (str): a text to use as the exception/warning message
        operator: one of the functions returned by get_possible_operators()
        assign_length_to_others (bool): treat all numeric types as having the
            length of 1. If False, any attempt to validate a numeric type
            will raise an exception/warning, as numeric types don't implement
            __len__()

    Returns:
        None, if check succeeded.

    Raises:
        Exception of the type provided by the handle_with parameter, LengthError
        by default (unless handle_with is a warning).

    >>> check_length(['string'], 1)
    >>> check_length('string', 6)
    >>> check_length([1, 2], 2)
    >>> check_length(len(i for i in range(3)))
    Traceback (most recent call last):
        ...
    TypeError: object of type 'generator' has no len()
    >>> check_length(2, 1, assign_length_to_others=True)
    >>> check_length(2, 0, operator=gt, assign_length_to_others=True)
    >>> check_length(True, 1, assign_length_to_others=True)

    To issue a warning, use the Warning class or its subclass:
    >>> check_length('string', 6, Warning)
    """
    _check_easycheck_arguments(handle_with=handle_with,
                             message=message,
                             operator=operator,
                             expected_length=expected_length,
                             assign_length_to_others=assign_length_to_others)

    if assign_length_to_others:
        if isinstance(item, (int, float, complex, bool)):
            item = [item]

    condition_to_check = operator(len(item), expected_length)
    check_if(condition_to_check, handle_with=handle_with, message=message)


def check_instance(item, expected_type, handle_with=TypeError, message=None):
    """Check if item has the type of expected_type.

    Args:
        item: the object whose type we want to validate
        expected_type (type, Iterable[type]): the expected type of the item
        handle_with (type): the type of exception or warning to be raised
        message (str): a text to use as the exception/warning message

    Returns:
        None, if check succeeded.

    Raises:
        Exception of the type provided by the handle_with parameter, TypeError
        by default.

    If you want to check if the item is None, you can do so in two ways:
    >>> my_none_object = None
    >>> check_if(my_none_object is None, handle_with=TypeError)

    or
    >>> check_instance(my_none_object, None)

    None is not a type, but it gets special treatment so that you can use
    the check_instance() function for None objects.

    >>> check_instance(['string'], list)
    >>> check_instance('string', str)
    >>> check_instance((1, 2), tuple)
    >>> check_instance([1, 2], (tuple, list), message='Neither tuple nor list')
    >>> check_instance('souvenir',
    ...    (tuple, list),
    ...    message='Neither tuple nor list')
    Traceback (most recent call last):
        ...
    TypeError: Neither tuple nor list
    >>> check_instance((i for i in range(3)), tuple)
    Traceback (most recent call last):
        ...
    TypeError
    >>> check_instance(
    ...    (i for i in range(3)), tuple, message='This is not tuple.')
    Traceback (most recent call last):
        ...
    TypeError: This is not tuple.
    >>> check_instance((i for i in range(3)), Generator)

    You can include None:
    >>> check_instance('a', (str, None))
    >>> check_instance(None, expected_type=(str, None))

    To issue a warning, do the following:
    >>> check_instance('a', (str, None), Warning, 'Undesired instance')
    """
    _check_easycheck_arguments(handle_with=handle_with,
                             message=message,
                             expected_type=expected_type)

    if expected_type is None:
        check_if(item is None, handle_with=handle_with, message=message)
        return None

    if isinstance(expected_type, Iterable):
        if item is None and any(t is None for t in expected_type):
            return None
        expected_type = tuple(t for t in expected_type if t is not None)

    check_if(isinstance(item, expected_type),
             handle_with=handle_with,
             message=message)


def check_if_paths_exist(paths,
                         handle_with=FileNotFoundError,
                         message=None,
                         execution_mode='raise'):
    """Check if a path or paths exist.

    If it does not, either raise (or return) an exception or issue (or return)
    a warning.

    Args:
        paths (str, Iterable[str]): path or paths to validate
        handle_with (type): type of exception or warning to be raised/returned
        message (str): a text to use as the exception/warning message
        execution_mode (str): defines what happens if not all the paths exist
            May take one of the following values:
                - 'raise': exception/warning will be raised
                - 'return': function will return information about the errors

    Returns:
        None, if execution_mode is 'raise' and check succeeded
        A tuple, if execution_mode is 'return'. The tuple has two elements:
            - an instance of the type provided by the handle_with parameter
            - a list of the non-existing paths

    Raises:
        Exception of the type provided by the handle_with parameter,
        FileNotFoundError by default (unless handle_with is a warning).

    >>> check_if_paths_exist('Q:/Op/Oop/')
    Traceback (most recent call last):
        ...
    FileNotFoundError
    >>> check_if_paths_exist(os.listdir()[0])
    >>> check_if_paths_exist(os.listdir())

    >>> check_if_paths_exist('Q:/Op/Oop/', execution_mode='return')
    (FileNotFoundError(), ['Q:/Op/Oop/'])
    >>> check_if_paths_exist(os.listdir()[0], execution_mode='return')
    (None, [])
    >>> check_if_paths_exist(os.listdir(), execution_mode='return')
    (None, [])

    To issue a warning, do the following:
    >>> check_if_paths_exist('Q:/Op/Oop/', handle_with=Warning)
    >>> check_if_paths_exist('Q:/Op/Oop/',
    ...    execution_mode='return',
    ...    handle_with=Warning)
    (Warning(), ['Q:/Op/Oop/'])
    >>> check_if_paths_exist('Q:/Op/Oop/',
    ...    execution_mode='return',
    ...    handle_with=Warning,
    ...    message='Attempt to use a non-existing path')
    (Warning('Attempt to use a non-existing path'), ['Q:/Op/Oop/'])
    """
    _check_easycheck_arguments(handle_with=handle_with,
                             message=message,
                             execution_mode=execution_mode)

    if isinstance(paths, str):
        paths = (paths,)

    if isinstance(paths, Iterable):
        error = None
        non_existing_paths = [
            path for path in paths
            if not Path(path).exists()
        ]

        if non_existing_paths:
            if execution_mode == 'raise':
                _raise(handle_with, message)
            elif execution_mode == 'return':
                if message:
                    error = handle_with(str(message))
                else:
                    error = handle_with()

        if execution_mode == 'return':
            return error, non_existing_paths
    else:
        raise TypeError('Argument paths must be string or iterable of strings')


def check_comparison(item_1, operator, item_2,
                     handle_with=ValueError,
                     message=None):
    """Check if a comparison of two items is true.

    Args:
        item_1: the first item to compare
        operator: one of the functions returned by get_possible_operators()
        item_2: the second item to compare
        handle_with (type): the type of exception or warning to be raised
        message (str): a text to use as the exception/warning message

    Returns:
        None, if check succeeded.

    Raises:
        Exception of the type provided by the handle_with parameter, ValueError
        by default (unless handle_with is a warning).

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

    You can use a dedicated ComparisonError class (defined in this module):
    >>> check_comparison('one text', lt, 'another text',
    ...                  handle_with=ComparisonError,
    ...                  message='Not less!')
    Traceback (most recent call last):
        ...
    easycheck.ComparisonError: Not less!

    To issue a warning, do the following:
    >>> check_comparison('one text', lt, 'another text',
    ...                  handle_with=Warning,
    ...                  message='Not less!')
    """
    _check_easycheck_arguments(handle_with=handle_with,
                             message=message,
                             operator=operator)

    check_if(operator(item_1, item_2),
             handle_with=handle_with,
             message=message)


def check_all_ifs(*args):
    """Check all multiple conditions and return all checks.

    Args:
        args: tuples of the form (check_function, arguments), where:
            - arguments is a tuple of arguments to be passed to a
              check_function
            - check_function is any of the check functions from this module
            (that is, any of the functions starting off with check_).

    Returns:
        A dict of the following structure:
            {'1: check_if': True, '2: check_if': True}
            This means that two checks were run, both using check_if, and
            both returned True confirmation status (so no exception was
            raised). In case of an exception raised, the resulting dict has the
            following structure:
            {'1: check_if': True, '2: check_if_not': AssertionError()}
            if a failure message was not provided, and otherwise
            {'1: check_if': True, '2: check_if_not': AssertionError('Wrong')}
            where 'Wrong' was the message provided as the argument.

    Use this function if you want to check a list of multiple conditions and
    catch all the errors (and messages) - it does not behave like the other
    functions in the module, since it returns the results of the checks, instead
    of raising an exception (or issuing a warning).

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

    You can also use this function with warnings:
    >>> check_all_ifs(
    ...    (check_if, 2 > 1),
    ...    (check_if_not, 'a' == 'a', Warning, 'It might be wrong!')
    ...    )
    {'1: check_if': True, '2: check_if_not': Warning('It might be wrong!')}
    """
    check_length(args, 0,
                 operator=gt,
                 handle_with=ValueError,
                 message='Provide at least one condition.')
    tuple_error_message = (
        'Provide all function calls as tuples in the form of '
        '(check_function, *args)'
    )
    for arg in args:
        check_instance(arg, tuple, message=tuple_error_message)

    results_of_checks = dict()
    for i, this_check in enumerate(args):
        function, *arguments = this_check
        run_this_check = True
        try:
            with warnings.catch_warnings(record=True) as this_warn:
                function(*arguments)
            if this_warn:
                run_this_check = this_warn[-1].message
        except Exception as e:
            run_this_check = e

        results_of_checks[f'{i + 1}: {function.__name__}'] = run_this_check

    return results_of_checks


def check_argument(argument,
                   argument_name=None,
                   expected_type=None,
                   expected_choices=None,
                   expected_length=None,
                   handle_with=ArgumentValueError,
                   message=None,
                   **kwargs):
    """Check if the user provided a correct argument value.

    Args:
        argument: argument value to be validated
        argument_name (str): original name of the argument in the calling
            function. If argument_name is not defined, the error messages will
            not include the name of the argument, but will instead only report
            the default text 'argument'

    Returns:
        None, if checks succeeded.

    Raises:
        Exception of the type provided by the handle_with parameter,
        ArgumentValueError by default (unless handle_with is a warning).

    You can use this function to check whether an argument's value meets
    various conditions. This is an alternative approach to independent checking
    of these conditions using separate easycheck functions.

    The function performs lazy checking, meaning that it first checks the
    instance (if provided), then choices (if provided), and then the expected
    length (if provided). These checks must not raise a built-in error, because
    this error would be raised before the check is performed.

    >>> check_argument(
    ...    [1, 2, 3], 'x',
    ...    expected_type=tuple,
    ...    expected_length=3
    ...    )
    Traceback (most recent call last):
        ...
    easycheck.ArgumentValueError: Incorrect type of x; valid type(s): <class 'tuple'>

    The expected_choices argument helps you check whether the user provided
    a valid value for the argument:
    >>> def foo(x):
    ...    check_argument(x, 'x', expected_choices=('first choice',
    ...                                             'second_choice'))
    ...    # whatever foo is doing...
    >>> foo('first choice')
    >>> foo('no choice') # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    easycheck.ArgumentValueError: x's value, no choice, is not among valid ...

    >>> x = 2.0
    >>> check_argument(
    ...    x, 'x',
    ...    expected_type=int) # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    easycheck.ArgumentValueError: Incorrect type of x; valid ... <class 'int'>

    This is how you can check exceptions and errors provided as arguments:
    >>> check_argument(TypeError, 'error_arg', expected_type=type)
    >>> check_argument(TypeError(), 'error_arg', expected_type=Exception)

    You can also issue a warning instead of raising an exception:
    >>> check_argument(
    ...    x, 'x',
    ...    expected_type=int,
    ...    handle_with=Warning,
    ...    message="Incorrect argument's value")
    """
    if all(item is None
           for item in (expected_type,
                        expected_choices,
                        expected_length
                        )):
        raise ValueError('check_argument() requires at least one condition'
                         ' to be checked')

    if argument_name is None:
        argument_name = 'argument'
    check_instance(argument_name,
                   str,
                   handle_with=handle_with,
                   message='argument_name must be string')

    if expected_type is not None:
        instance_message = _make_message(
            message,
            (f'Incorrect type of {argument_name}; valid type(s):'
             f' {expected_type}'))
        check_instance(item=argument,
                       expected_type=expected_type,
                       handle_with=handle_with,
                       message=instance_message)
    if expected_choices is not None:
        choices_message = _make_message(
            message,
            (f'{argument_name}\'s value, {argument}, '
             f'is not among valid values: {expected_choices}.'))
        check_if(argument in expected_choices,
                 handle_with=handle_with,
                 message=choices_message)
    if expected_length is not None:
        length_message = _make_message(
            message,
            (f'Unexpected length of {argument_name}'
             f' (should be {expected_length})'))
        check_length(item=argument,
                     expected_length=expected_length,
                     handle_with=handle_with,
                     message=length_message,
                     **kwargs)


def _make_message(message_provided, message_otherwise):
    """If message was provided, use it; otherwise, use the alternative one.

    Args:
        message_provided: message to use if provided
        message_otherwise: message to use if the first one was not provided

    Returns:
        First message that evaluates to True

    This function is used by the check_argument() function.

    >>> _make_message(None, 'Otherwise')
    'Otherwise'
    >>> _make_message('Provided', 'Otherwise')
    'Provided'
    """
    return message_provided or message_otherwise


def catch_check(check_function, *args, **kwargs):
    """Catch an exception or warning raised/issued by a easycheck function.

    Args:
        check_function: function to call (one of the public easycheck functions)
        args: positional arguments to pass on to check_function
        kwargs: keyword arguments to pass on to check_function

    Returns:
        Exception or warning instance

    Raises:
        TypeError, if check_function is not a callable
        ArgumentValueError, if check_function is not one of the allowed functions
        ValueError, if an attempt to call another error-catching function is
            detected

    Most easycheck functions return None when the check is successful, and
    otherwise either raise an exception or issue a warning. You can use this
    function to change this behavior: the check_function will still return None
    when all conditions pass, but instead of raising an exception or issuing
    a warning in case of problems, it will return the specified exception
    or warning.

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
    >>> catch_check(check_if, condition=2>2, handle_with=ValueError)
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

    You can also catch warnings:
    >>> catch_check(check_if, condition=2>2, handle_with=Warning)
    Warning('Warning')
    >>> catch_check(check_if,
    ...    condition=2>2,
    ...    handle_with=UserWarning,
    ...    message='Beware of this problem')
    UserWarning('Beware of this problem')
    """
    check_if(isinstance(check_function, Callable),
             handle_with=TypeError,
             message=(f'{check_function} does not '
                      'seem to be a easycheck function')
             )
    check_if_not(check_function == check_all_ifs,
                 handle_with=ValueError,
                 message=('Do not use catch_check for check_all_ifs() '
                          'because it itself returns its checks.')
                 )
    paths_condition = (
        check_function == check_if_paths_exist
        and
        ('return' in args or kwargs.get('execution_mode', '') == 'return')
    )
    check_if_not(paths_condition,
                 handle_with=ValueError,
                 message=('Do not use catch_check for check_if_paths_exist() '
                          'with execution_mode="return" because it itself '
                          'returns its checks.')
                 )
    check_argument(
        argument=check_function,
        argument_name=check_function.__name__,
        expected_choices=(
            check_if, assert_if,
            check_if_not, assert_if_not,
            check_argument,
            check_comparison,
            check_if_paths_exist, assert_paths,
            check_instance, assert_instance,
            check_length, assert_length,
        ),
        handle_with=ArgumentValueError,
        message=(f'{check_function.__name__} is not'
                 ' among acceptable valid easycheck functions')
    )

    try:
        with warnings.catch_warnings(record=True) as possible_warn:
            check_function(*args, **kwargs)
        if possible_warn:
            return possible_warn[-1].message
    except Exception as e:
        return e


def _raise(error, message=None):
    """Raise exception with or without message, or issue a warning.

    Args:
        error (type): the type of exception or warning to be raised
        message (str): a text of the exception/warning message. If error
        is a Warning subclass, you should provide your own message, otherwise
        a default message ('Warning') will be used.

    Raises:
        Exception of the type provided by the error parameter
        TypeError if error parameter is not an exception or warning class

    Raising exceptions:
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

    Issuing warnings (we will catch them in order to see what they contain):
    >>> with warnings.catch_warnings(record=True) as w:
    ...    _raise(Warning)
    ...    assert_if(issubclass(w[-1].category, Warning))
    ...    assert_if('Warning' in str(w[-1].message))
    >>> with warnings.catch_warnings(record=True) as w:
    ...    _raise(Warning, 'Watch out! Something might be wrong.')
    ...    assert_if('Watch out!' in str(w[-1].message))
    """
    if not isinstance(error, type) or not issubclass(error, Exception):
        raise TypeError('The error argument must be an exception or a warning')

    if issubclass(error, Warning):
        if message is None:
            message = 'Warning'
        check_instance(message, str, message='message must be string')
        warnings.warn(message, error)
    else:
        if message is None:
            raise error
        else:
            check_instance(message, str, message='message must be string')
            raise error(message)


def _check_easycheck_arguments(handle_with=None,
                             message=None,
                             condition=None,
                             operator=None,
                             assign_length_to_others=None,
                             execution_mode=None,
                             expected_length=None,
                             expected_type=None):
    """Validate the most common arguments used in easycheck functions.

    This is a generic function that works for most easycheck functions, and can
    be customized by providing selected arguments from a given function.
    Other arguments, not included in this function, need to be checked using
    other ways.

    >>> _check_easycheck_arguments(handle_with=LengthError)
    >>> _check_easycheck_arguments(handle_with=ValueError)

    You must provide an exception (or warning) class, not its instance:
    >>> _check_easycheck_arguments(handle_with=ValueError())
    Traceback (most recent call last):
        ...
    TypeError: handle_with must be an exception

    >>> _check_easycheck_arguments(handle_with=LengthError, message=False)
    Traceback (most recent call last):
        ...
    TypeError: message must be either None or string
    >>> _check_easycheck_arguments(handle_with=ValueError, condition=2<1)
    """
    if all(argument is None
           for argument
           in (handle_with,
               message,
               condition,
               operator,
               assign_length_to_others,
               execution_mode,
               expected_length,
               expected_type)):
        raise ValueError('Provide at least one argument')

    if handle_with is not None:
        try:
            is_subclass = issubclass(handle_with, Exception)
        except TypeError:
            is_subclass = False
        if not is_subclass:
            raise TypeError('handle_with must be an exception')
    if message is not None:
        if not isinstance(message, str):
            raise TypeError('message must be either None or string')
    if condition is not None:
        if not isinstance(condition, bool):
            raise ValueError('The condition does not return a boolean value')
    if operator is not None:
        if operator not in get_possible_operators():
            raise OperatorError(
                'Incorrect operator. Check get_possible_operators()')
    if expected_length is not None:
        if not isinstance(expected_length, (int, float)):
            raise TypeError(
                'expected_length should be an integer (or a float)')
    if assign_length_to_others is not None:
        if not isinstance(assign_length_to_others, bool):
            raise TypeError('assign_length_to_others should be'
                            ' a boolean value')
    if execution_mode is not None:
        if execution_mode not in ('raise', 'return'):
            raise ValueError(
                'execution_mode should be either "raise" or "return"')
    if expected_type is not None:
        if isinstance(expected_type, Iterable):
            if any(not isinstance(t, type)
                   for t in expected_type
                   if t is not None):
                raise TypeError('all items in expected_type must be valid types')
        elif not isinstance(expected_type, type):
            raise TypeError('expected_type must be a valid type')


def get_possible_operators():
    """Provide a list of possible operators to be used in easycheck functions.

    All of these operators come from the operator module, but not all operators
    from this module are allowed.

    >>> operators = get_possible_operators()
    >>> type(operators[0])
    <class 'builtin_function_or_method'>
    >>> len(operators)
    8
    """
    return eq, le, lt, gt, ge, ne, is_, is_not


# Aliases to be used for testing. Beware not to use warnings with them.

assert_if = check_if
assert_if_not = check_if_not
assert_length = check_length
assert_instance = check_instance
assert_paths = check_if_paths_exist
