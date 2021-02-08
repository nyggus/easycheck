Catching exceptions instead of raising them
-------------------------------------------

If you do not want to raise exceptions but to catch them instead, you can do so using the :code:`catch_check()` function:

.. code-block:: python

    >>> from easycheck import check_if, check_instance, catch_check
    >>> my_check = catch_check(check_if, 2 > 2, ValueError)
    >>> my_check
    ValueError()
    >>> my_check = catch_check(check_if, 2 > 2, ValueError, 'Incorrect value')
    >>> my_check
    ValueError('Incorrect value')
    >>> type(my_check)
    <class 'ValueError'>
    >>> check_instance(my_check, ValueError)
    >>> raise(my_check)
    Traceback (most recent call last):
        ...
    ValueError: Incorrect value

Nonetheless, in many situations, you will do better using a simpler and more readbale approach, that is, catching exceptions using the :code:`try-except` block. This approach is particularly readable and efficient when you want to check several things. See  `how to use in try-except blocks <https://github.com/nyggus/easycheck/blob/master/docs/use_with_try_doctest.rst>`_).