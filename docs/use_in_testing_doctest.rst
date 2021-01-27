Use in testing
--------------

Although we stress that :code:`easycheck` functions are designed to be used within code (unlike classical assertions, which should not be used in code outside of testing), it does not mean that they cannot be used in testing. In fact, they can be quite helpful, particularly in doctests, and also in pytests. The :code:`easycheck` package offers several aliases of its main :code:`easycheck` functions, which make the functions resemble the :code:`assert` expression. These aliases are

* :code:`assert_if` (for :code:`check_if`)
* :code:`assert_if_not` (for :code:`check_if_not`)
* :code:`assert_length` (for :code:`check_length`)
* :code:`assert_instance` (for :code:`check_instance`)
* :code:`assert_paths` (for :code:`check_if_paths_exist`)

As aliases, they use the same syntax and arguments as their :code:`easycheck` counterparts. See:

.. code-block:: python

    >>> from easycheck import assert_if, assert_instance, assert_length
    >>> def multiply_string(string, k):
    ...    """Make a list consisting of string k times.
    ...    >>> single_string = 'aka'
    ...    >>> string_multiplied = multiply_string(single_string, 3)
    ...    >>> assert_instance(string_multiplied, list)
    ...    >>> for i, item in enumerate(string_multiplied):
    ...            assert_instance(item, str)
    ...            assert_if(item == single_string)
    ...    >>> assert_length(string_multiplied, 3)
    ...    """
    ...    return [string] * k

When you run doctests, all tests will run without error, as in the below simulation of the corresponding doctests from the above docstring:

.. code-block:: python

    >>> single_string = 'aka'
    >>> string_multiplied = multiply_string(single_string, 3)
    >>> assert_instance(string_multiplied, list)
    >>> for i, item in enumerate(string_multiplied):
    ...    assert_instance(item, str)
    ...    assert_if(item == single_string)
    >>> assert_length(string_multiplied, 3)

Do remember, however, *not* to use warnings in testing! Consider the following:

.. code-block:: python
    
    >>> from easycheck import check_if
    >>> check_if(2 < 1)
    Traceback (most recent call last):
	    ...
    AssertionError
    >>> check_if(2 < 1, ValueError)
    Traceback (most recent call last):
        ...
    ValueError
    >>> assert_if(2 < 1, Warning)
    >>> assert_if(2 < 1, UserWarning)
    
As you can see, the two last assertions issue warnings (see `here <https://github.com/nyggus/easycheck/tree/master/docs/use_with_warnings_doctest.rst>`_ to learn more about using :code:`easycheck` with warnings), but will not raise exceptions – this could dramatically affect your testing. However, warnings *do not* make the test fail! So, remember this basic rule: Never use warnings in testing when you want to catch critical errors.