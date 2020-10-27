"""Testing module of checkit.

It offers
* assert-like functions, which are simply aliases of the checkit
functions: assert_if(), assert_if_not(), assert_instance(),
  assert_length() and assert_paths()
* functions to create simple mockup of functions and other objects:
  easy_mock() and mock()
"""

from checkit.checks import (check_if,
                            check_if_not,
                            check_length,
                            check_instance,
                            check_if_paths_exist,
                            )

assert_if = check_if
assert_if_not = check_if_not
assert_length = check_length
assert_instance = check_instance
assert_paths = check_if_paths_exist


def easy_mock(item, returns):
    """Return a mock object to be used in doctests.
    
    The functions works with both functions and objects, but not with classes.
    
    Using easy_mockup for in doctests can help you in various situations, like:
      * the original function needs time to run
      * you do not want to obtain all the necessary arguments you would
        normally need; in that case, you can create mocks of those arguments
      * you do not want to use big objects (like pandas data frames or long
        lists), so you want to create their small mocks
    
    You could certainly do the same without mocking, but mocking helps you keep
    clarity, by enabling you to show how the original function should be used.
    It will also help you run doctests without the necessity of running the
    same function in a doctest for each function. For instance, you can have a
    get_data() function that gets data from a database, a memory-inefficient
    process. You can write a docktest for this function, and it will take time
    to run it. But you will unlikely want to run this function for every other
    doctest in which you do need these data. So, you can create a mock for this,
    like here:
    
    >>> def read_from_data_base():
    ...    # the original function, which takes about 5 sec to run
    ...    import time
    ...    time.sleep(5)
    ...    something, success, data = 50, True, range(1000)
    ...    return something, success, data
    >>> def analyze_data(data):
    ...    # do whatever you need to do with the data
    ...    return sum(data)
    
    So, we have a function that uses the data got by the read_from_data_base()
    function. You can write a doctest for read_from_data_base(), but it will
    take those five seconds. A doctest for the analyze_data() function,
    however, will require to run the read_from_data_base() function, something
    you want to avoid because of the time it would take. Here, the eacy_mockup
    comes to rescue. Here is how you could write a doctest for it:
    >>> read_from_data_base = easy_mock(
    ...    read_from_data_base,
    ...    returns=(50, True, [20, 30, 40]))
    >>> *whatever, data = read_from_data_base()
    >>> print(analyze_data(data))
    90
    
    If item is a function, you create a mock that is callable with any
    arguments. This means that it will also with with incorrect arguments, so
    you need to take care of using only valid ones.
    >>> print(read_from_data_base())
    (50, True, [20, 30, 40])
    >>> print(read_from_data_base(20))
    (50, True, [20, 30, 40])
    >>> print(read_from_data_base(20, "nothing"))
    (50, True, [20, 30, 40])
    >>> print(read_from_data_base(first_arg=20, second_arg="nothing"))
    (50, True, [20, 30, 40])
    
    You can use it with various functions:
    >>> import os
    >>> os.getcwd = easy_mock(os.getcwd, returns='Q:/Whatever_folder')
    >>> assert os.getcwd() == 'Q:/Whatever_folder'
    >>> assert not os.path.exists(os.getcwd())
        
    If item is not a callable, then it will return whatever you want it to,
    thanks to the returns argument. You can for instance use it to mock
    big objects in your doctests, e.g., to check if a function taking a huge
    list or a generator as an argument works fine, but you want to do it using
    a small list (generator).
    >>> x = range(100000)
    >>> x = easy_mock(x, range(5))
    
    WARNING!
    easy_mock() is dedicated to doctests, because its behavior cannot be
    restored (at least not in an easy way). This is basically what works fine
    in doctests, and so easy_mock() offers you simplicity. You can also use it
    in pytests, though, but when doing so, remember that in doctests mocks of
    external functions are global! See:
    >>> def check_getcwd():
    ...    os.getcwd = easy_mock(os.getcwd, returns='Q:/A_different_folder')
    ...    assert os.getcwd() == 'Q:/A_different_folder'
    
    This is what we have now
    >>> assert os.getcwd() == 'Q:/Whatever_folder'
    
    Let's run the function:
    >>> check_getcwd()
    
    and note that it changes the global return of os.getcwd():
    >>> assert os.getcwd() != 'Q:/Whatever_folder'
    >>> assert os.getcwd() == 'Q:/A_different_folder'
    
    Basically, mock functions do not work locally, so it's safer to define them
    in the global environment. This is unlikely to poise a problem in testing
    environments, however. When you want to do it inside a function, you will
    likely end up defining it in a global scope anyway, using a global
    expression. Compare:
    >>> def foo(): return 5
    >>> def bar():
    ...    foo = easy_mock(foo, returns=10)
    >>> bar()
    Traceback (most recent call last):
        ...
    UnboundLocalError: local variable 'foo' referenced before assignment
    
    But:
    >>> foo()
    5
    >>> def bar():
    ...    global foo
    ...    foo = easy_mock(foo, returns=10)
    ...    print(foo())
    >>> bar()
    10
    >>> foo()
    10
    
    So, you should define mocks in the global environment.
    """
    if item is None:
        mock_item = returns
    if callable(item):
        def mock_item(*args, **kwargs):
            return returns
    else:
        mock_item = returns
    return mock_item


def mock(item, returns):
    """Return a reversible mock object to be used in doctests.
    
    This function works the same way as does easy_mock, but it in addition
    return the original item along with its mock. So, if you need to be able
    to reverse the mock, you should use this function instead of easy_mock.
    It returns a tuple of the original item and its mock.
    >>> def foo(): return 5
    >>> foo()
    5
    >>> original_foo, foo = mock(foo, returns=10)
    >>> foo()
    10
    >>> foo = original_foo
    >>> foo()
    5
    >>> x = range(1000)
    >>> len(x)
    1000
    >>> original_x, x = mock(x, returns=range(10))
    >>> len(original_x)
    1000
    >>> len(x)
    10
    >>> x = original_x
    >>> len(x)
    1000
    """
    original_item = item
    mock_item = easy_mock(item, returns)
    return original_item, mock_item
