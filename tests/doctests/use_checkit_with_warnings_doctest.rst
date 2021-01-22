Use checkit with warnings
-------------------------

One of the aims of the :code:`checkit` package is to enable you to issue a warning (instead of raising an exception) when a condition is violated. You can use the standard-library :code:`warnings` module for this, but :code:`checkit` lets you issue warnings using the same :code:`checkit` syntax as you would use to raise exceptions. In order to issue a warning, you need to provide a :code:`Warning` class, or its subclass, to the :code:`handle_with` argument, like here:

.. code-block:: python

    >>> from checkit import check_if, check_instance, check_length
    >>> check_if(2 > 2, Warning)

This will raise a warning (of the :code:`Warning` class), with a default (and unhelpful) message 'Warning', leading to the warning :code:`Warning: Warning`. To change this (rather unhelpful) message, use the :code:`message` parameter, as below:

.. code-block:: python

    >>> check_if(2 > 2, Warning, 'Incorrect value')
	
By using the :code:`checkit` module, your warnings can be as informative as the message you provide (for example, :code:`Warning: Incorrect value`, although you can make it much more specific). You really should define messages for all warnings, since while an exception without a message can be informative, a warning without a message is not.

Let's check other examples, but this time we will catch the warnings in order to study them:

.. code-block:: python

    >>> import warnings
    >>> x = 50
    >>> with warnings.catch_warnings(record=True) as this_warning:
    ...     check_instance(x, (tuple, list), Warning, 'Incorrect value')
    ...     assert 'Incorrect value' in str(this_warning[-1].message)
    ...     assert str(this_warning[-1].category) == "<class 'Warning'>"

You can use warnings in most :code:`checkit` functions, and you can catch them using :code:`catch_check()`:
    
.. code-block:: python

    >>> from checkit import catch_check
    >>> catch_check(check_length,
    ...    [1, 2, 3],
    ...    expected_length=5,
    ...    handle_with=Warning,
    ...    message='The list should be 5-element long')
    Warning('The list should be 5-element long')
    >>> catch_check(check_instance,
    ...    'some string but for sure not a float',
    ...    expected_type=float,
    ...    handle_with=Warning,
    ...    message='This does not seem to be a float!')
    Warning('This does not seem to be a float!')
