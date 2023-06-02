Using :code:`easycheck` for assertion
--------------------------

:code:`easycheck` gives the users a set of tools to add assertions to their code. There are two main reasons to do it. The first one is, of course, testing (see the `use_in_testing_doctest <https://github.com/nyggus/easycheck/blob/master/docs/use_in_testing_doctest.rst>`_ file). The second one is when you try to catch a situation that should never happen (see `this article <https://towardsdatascience.com/python-assertions-or-checking-if-a-cat-is-a-dog-ce11c55d143>`_).

Imagine you want to write a function that calculates the cumulative length of all elements of a list. So, for :code:`[[1, 2, 3], "hey"]`, this should be 6. 

After some development, you come up with the following function:
.. code-block:: python
    >>> def inside_len(list_: list) -> int:
    ...     if not isinstance(list_, list):
    ...         raise TypeError("inside_len() works with lists only")
    ...     if not list_:
    ...         return 0
    ...     length = 0
    ...     for l in list_:
    ...         try:
    ...             length += len(l)
    ...         except TypeError:
    ...             continue
    ...     assert_if(length > 0)
    ...     assert_type(length, int)
    ...     return length

As you see, the function has two assertions, one that the cumulative length of a non-empty list is over zero, and that the length is an integer. These are *not* checks but assertions, as their purpose is to check whether the code is correct. That's why it makes sense to run them in the :code:`__debug__` mode only, and not in the production mode. 

Let's use the function:
.. code-block:: python
    >>> cum_length([1, 2, 3], "hey")
    6
    >>> cum_length([[1]])
    1
    >>> cum_length("whatever", "works", "works", "for", "me")
    23
    >>> cum_length([1, 2, 3])
    Traceback (most recent call last):
        ...
    AssertionError

Ha? Something's wrong? Difficult to see without customizing the assertions. We could do this:
.. code-block:: python

...     assert_if(length > 0, ValueError)
...     assert_type(length, int, TypeError)

or by adding messages. This shows that it does make sense to customize assertions.

In our situation, the error came from the first assertion, since the condition :code:`length > 0` was violated. Is the function incorrect?

In this scenario, actually, the assertion was incorrect. It showed that our preliminary assumption that the cumulative length cannot be zero was incorrect. It can, when none of the elements has length or has length over zero. Hence, the only thing we need to do is to change the assertion to :code:`length >= 0`.

This example showed that assertions can help catch not only incorrect implementation, but also incorrect understanding of the function or its purpose..
