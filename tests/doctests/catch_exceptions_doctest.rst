Catching exceptions instead of raising them
-------------------------------------------

If you do not want to raise exceptions but to catch them instead, you can do so using the :code:`catch_check()` function:

.. code-block:: python

    >>> from checkit import check_if, check_instance, catch_check
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
