Use checkit in code
-------------------

The basic aim of :code:`checkit` is to provide you with quick-to-use, simple and readable assertion-like functions to make sure that particular conditions you are interested in are met. They are assertion-like because what you do is indeed similar to what the :code:`assert` expression does, since the functions

* check a condition
* do nothing when it is met, but
* raise an exception (or, alternatively, issue a warning) when it is not

Of course, :code:`checkit` is to help you when Python does not handle a particular situation. For example, it does so when you're trying to divide a number by zero, so you need not use :code:`checkit` then. But there is a plethora of various situations which you want to handle.

Here are several examples of the simplest uses of :code:`checkit`:

.. code-block:: python

	>>> from checkit import check_if, check_if_not, check_instance
	>>> def get_family_name(full_name):
	...    check_if_not(full_name is None, TypeError, 'Missing name')
	...    check_instance(full_name, str, message='Full name must be string')
	...    check_if(' ' in full_name.strip(),
	...        ValueError,
	...        'No space in name: impossible to split first and second name'
	...    )
	...    return full_name.split(' ')[1]
	>>> get_family_name('John Smith')
	'Smith'
	>>> get_family_name('John_Smith')
	Traceback (most recent call last):
		...
	ValueError: No space in name: impossible to split first and second name

	>>> get_family_name(57)
	Traceback (most recent call last):
		...
	TypeError: Full name must be string

	>>> get_family_name(None)
	Traceback (most recent call last):
		...
	TypeError: Missing name

If something is wrong, the chosen exception is raised, or alternatively, the chosen warning is issued. If you need to catch these exceptions and handle them accordingly, you can certainly do so (note that two different types of errors can be raised by :code:`get_family_name()`). You can also catch warnings.
        
Without :code:`checkit`, this function might have the following form:
    
.. code-block:: python

	>>> def get_family_name(full_name):
	...    if full_name is None:
	...        raise TypeError('Missing full name')
	...    elif not isinstance(full_name, str):
	...        raise TypeError('Full name must be string')
	...    elif ' ' not in full_name.strip():
	...        raise ValueError('No space in name:'
	...            ' impossible to split first and second name')
	...    return full_name.split(' ')[1]
    
Above, we used specified errors and messages, but we can make the call shorter by using default exceptions and messages. Consider the following:
    
.. code-block:: python

	>>> def get_family_name(full_name):
	...    check_if_not(full_name is None, ValueError)
	...    check_instance(full_name, str)
	...    check_if(' ' in full_name.strip(), ValueError)
	...    return full_name.split(' ')[1]

	>>> get_family_name('John Smith')
	'Smith'
	>>> get_family_name('John_Smith')
	Traceback (most recent call last):
		...
	ValueError

	>>> get_family_name(57)
	Traceback (most recent call last):
		...
	TypeError

	>>> get_family_name(None)
	Traceback (most recent call last):
		...
	ValueError

The non-checkit counterpart is rather less readable:

.. code-block:: python

	def get_family_name(full_name):
	...    if (full_name is None
	...        or not isinstance(full_name, str)
	...        or ' ' not in full_name.strip()):
	...        raise Exception
	...    return full_name.split(' ')[1]

See the catch_exceptions_doctest.rst file to check out how to catch exceptions instead of raising them, and use_checkit_with_warnings_doctest.rst to check out what you can do with warnings in :code:`checkit`.