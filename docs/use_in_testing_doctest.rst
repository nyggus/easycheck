Use in testing
--------------

Although we stress that :code:`easycheck` check functions are designed to be used within code, it does not mean that they cannot be used in testing. In fact, they can be quite helpful. The :code:`easycheck` package offers several assert functions. They have very similar signatures to the corresponding check functions, but they work like the :code:`assert` expression, meaning they are run only in the debug mode (that is, when :code:`__debug__` is :code:`True`). These functions are

* :code:`assert_if` (for :code:`check_if`)
* :code:`assert_if_not` (for :code:`check_if_not`)
* :code:`assert_if_in_limits` (for :code:`check_if_in_limits`)
* :code:`assert_length` (for :code:`check_length`)
* :code:`assert_type` (for :code:`check_type`)
* :code:`assert_paths` (for :code:`check_if_paths_exist`)
* :code:`assert_if_isclose` (for :code:`check_if_isclose`)

They use the same syntax and arguments as their :code:`easycheck` counterparts, the only differences is that they work only for :code:`__debug__ = True`, which is always true for tests. See:

.. code-block:: python

    >>> from easycheck import assert_if, assert_type, assert_length
    >>> def multiply_string(string, k):
    ...    """Make a list consisting of string k times.
    ...    >>> single_string = 'aka'
    ...    >>> string_multiplied = multiply_string(single_string, 3)
    ...    >>> assert_type(string_multiplied, list)
    ...    >>> for i, item in enumerate(string_multiplied):
    ...            assert_type(item, str)
    ...            assert_if(item == single_string)
    ...    >>> assert_length(string_multiplied, 3)
    ...    """
    ...    return [string] * k

When you run doctests, all tests will run without error, as in the below simulation of the corresponding doctests from the above docstring:

.. code-block:: python

    >>> single_string = 'aka'
    >>> string_multiplied = multiply_string(single_string, 3)
    >>> assert_type(string_multiplied, list)
    >>> for i, item in enumerate(string_multiplied):
    ...    assert_type(item, str)
    ...    assert_if(item == single_string)
    >>> assert_length(string_multiplied, 3)

Do remember, however, that the testing functions use only `AssertionError`! They do not have the `handle_with` argument, as they are designed to work in a similar way to regular assertions, the only difference being specificity of each function.

.. code-block:: python
    
    >>> from easycheck import check_if
    >>> check_if(2 < 1)
    Traceback (most recent call last):
	    ...
    AssertionError
    
