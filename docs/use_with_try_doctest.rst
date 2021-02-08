Use with the try-except block
-----------------------------

You can use :code:`easycheck` functions within a :code:`try-except` block to catch exceptions. See:

.. code-block:: python

    >>> from easycheck import check_if_not, check_instance
    >>> def foo(a, b):
    ...    try:
    ...        check_instance(a, int, message='a must be integer')
    ...        check_instance(b, int, message='b must be integer')
    ...        check_if_not(a > b, ValueError, 'a must not be higher than b')
    ...    except Exception as e:
    ...        print(f'Error: {e}')
    >>> foo('string', 10)
    Error: a must be integer
    >>> foo(10, 'string')
    Error: b must be integer
    >>> foo(11, 10)
    Error: a must not be higher than b
    >>> foo(9, 10)

You can get similar functionality using the function that catches exceptions, that is, :code:`catch_check()` (see `how to catch exceptions instead of raise them <https://github.com/nyggus/easycheck/blob/master/docs/catch_exceptions_doctest.rst>`_). In order to do so, you could do the following:

.. code-block:: python

    >>> from easycheck import check_if_not, check_instance, catch_check
    >>> def bar(a, b):
    ...    a_check = catch_check(check_instance, a, int, message='a must be integer')
    ...    b_check = catch_check(check_instance, b, int, message='b must be integer')
    ...    if not a_check and not b_check:
    ...        a_b_check = catch_check(check_if_not, a > b, ValueError, 'a must not be higher than b')
    ...        if a_b_check:
    ...            print(f'Error: {a_b_check}')
    ...    else:
    ...        print(f'Error: {a_check}, {b_check}')
    >>> bar('string', 10)
    Error: a must be integer, None
    >>> bar(10, 'string')
    Error: None, b must be integer
    >>> bar(11, 10)
    Error: a must not be higher than b
    >>> foo(9, 10)

Note that this code is much more complex than the above code. This is because we need to take care of *not* running :code:`catch_check(check_if_not, a > b, ValueError, 'a must not be higher than b')` if `a > b` gives an error (as does the comparison of an integer with a string). Using the :code:`catch_exception()` function, we need to catch each such check, something that the :code:`try-except` block did before. What's more, we did not format what :code:`print()` returns, since it would introduce additional complexity. 

As we see, in many instances the simpler approach with the :code:`try-except` block will be better and more readable.