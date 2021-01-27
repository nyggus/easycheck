Use easycheck in code
-------------------

The basic aim of :code:`easycheck` is to provide you with easy-to-use, simple and readable assertion-like functions to make sure that particular conditions you wish to check are met. They are similar to assertions because the functionality is indeed similar to the :code:`assert` expression, since these functions

* check a condition
* do nothing when the condition is met,
* raise an exception (or, alternatively, issue a warning) when the condition is not met.

Of course, :code:`easycheck` is meant to help you when Python does not handle a particular situation. For example, Python handles division-by-zero errors, so you need not use :code:`easycheck` for this. However, there are many other situations which you may want to handle.

Here are several examples of the simplest uses of :code:`easycheck`:

.. code-block:: python

	>>> from easycheck import check_if, check_if_not, check_instance
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

If a condition fails, the chosen exception is raised; or alternatively, the chosen warning is issued. If you need to catch these exceptions and handle them accordingly, you can certainly do so (note that two different types of errors can be raised by :code:`get_family_name()`). You can also catch warnings.
        
Without :code:`easycheck`, this function might have the following form:
    
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

The non-easycheck counterpart is rather less readable:

.. code-block:: python

	def get_family_name(full_name):
	...    if (full_name is None
	...        or not isinstance(full_name, str)
	...        or ' ' not in full_name.strip()):
	...        raise Exception
	...    return full_name.split(' ')[1]

See `catch_exceptions_doctest.rst <https://github.com/nyggus/easycheck/tree/blob/master/docs/catch_exceptions_doctest.rst>`_ to check out how to catch exceptions instead of raising them, and `use_with_warnings_doctest.rst <https://github.com/nyggus/easycheck/tree/blob/master/docs/use_with_warnings_doctest.rst>`_ to check out what you can do with warnings in :code:`easycheck`.