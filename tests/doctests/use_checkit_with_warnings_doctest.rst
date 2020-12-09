Use checkit with warnings
-------------------------------------------

One of the aims of the `checkit` package is to enable you to issue warnings when a condition is violated. Of course, you can use the standard-library `warnings` module for this, but `checkit` lets you issue warnings using the very same syntax as that you would use to raise exceptions (using `checkit`, of course). In order to issue a warning, you need to use the `handle_by` argument, like here:

.. code-block:: python

    >>> from checkit import check_if, check_instance, check_length
    >>> check_if(2 > 2, Warning)

This will raise a Warning, with a default (and unhelpful) message 'Warning', so the warning will be `Warning: Warning`. To customize the message (which you really should do, since while an exception without a message can be informative, a warning without one will not), use the `message` parameter:

.. code-block:: python

    >>> check_if(2 > 2, Warning, 'Incorrect value')
	
Now, the warning will be as informative as the message you provided: `Warning: Incorrect value`.

Let's check other examples, and this time we will catch the warnings and study them:

.. code-block:: python

    >>> import warnings
    >>> x = 50
    >>> with warnings.catch_warnings(record=True) as this_warning:
    ...     check_instance(x, (tuple, list), Warning, 'Incorrect value')
    ...     assert 'Incorrect value' in str(this_warning[-1].message)
    ...     assert str(this_warning[-1].category) == "<class 'Warning'>"

You can use warnings in most functions, you can also catch them using `catch_check()`:
    
.. code-block:: python

    >>> from checkit import catch_check
    >>> catch_check(check_length,
    ...    [1, 2, 3],
    ...    expected_length=5,
    ...    handle_by=Warning,
    ...    message='The list should be 5-element long')
    Warning('The list should be 5-element long')
    >>> catch_check(check_instance,
    ...    'some string but for sure not a float',
    ...    expected_instance=float,
    ...    handle_by=Warning,
    ...    message='This does not seem to be a float!')
    Warning('This does not seem to be a float!')
    