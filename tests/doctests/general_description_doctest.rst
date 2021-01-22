The :code:`checkit` module
--------------------------

The main function is :code:`check_if()`, with its negative counterpart :code:`check_if_not()`. The other functions are actually wrappers built around :code:`check_if()`, customized to particular situations and conditions. :code:`check_if()` checks a condition provided as its argument; if the condition is not met, the function raises an exception (which can be either one of the exception classes, built-in ones, ones from the checkit module, or user-created) or issues a warning (which must derive from the Warning class); you can (optionally) send a message along with the exception, and you should send a message with the warning. Note that when you use the built-in assert expression, you're limited to :code:`AssertionError`, but when using checkit assert functions, you can use any exception you want.

Consider the following example:

.. code-block:: python

    >>> from checkit import (check_if, check_if_not, check_length, check_instance,
    ...                      check_comparison, check_if_paths_exist, assert_if, assert_length,
    ...                      assert_instance)
    >>> if 1 > 0:
    ...    raise ValueError('One is bigger than zero')
    Traceback (most recent call last):
        ...
    ValueError: One is bigger than zero

The idea is to simplify this call by using

.. code-block:: python

   >>> check_if(0 > 1, handle_with=ValueError, message='One is bigger than zero')
   Traceback (most recent call last):
       ...
   ValueError: One is bigger than zero

or even simpler

.. code-block:: python

    >>> check_if(0 > 1, ValueError, 'One is bigger than zero')
    Traceback (most recent call last):
        ...
    ValueError: One is bigger than zero

Of course, it's not only brevity that we aim for: The package's main purpose is code readability. As always, whether this approach results in more readable code is a subjective matter, but you will see many examples that, in our opinion, make the checkit approach more readable than the equivalent if-blocks.

If you are fine with AssertionError (actually, the only built-in exception class for regular asserts in Python), you can use this simple code:

.. code-block:: python

    >>> check_if(0 > 1)
    Traceback (most recent call last):
        ...
    AssertionError

This may be the most efficient way for debugging using simple assertions.

In case you want to issue a warning, do the following:

.. code-block:: python

    >>> check_if(0 > 1, handle_with=Warning, message='0 is too small')

or simpler

.. code-block:: python

    >>> check_if(0 > 1, Warning, '0 is too small')

You can use a :code:`check_if_not()` wrapper for negative conditions:

.. code-block:: python

    >>> check_if_not(2 > 1, ValueError, 'The condition is true')
    Traceback (most recent call last):
        ...
    ValueError: The condition is true

Other checkit functions use :code:`check_if()` to check a particular condition, like length:

.. code-block:: python

    >>> my_list = [1, 12, 1]
    >>> check_length(my_list, 3)
    >>> from operator import (eq, le, lt, ge, gt, ne) 
    >>> check_length(my_list, 10, operator=le)
    >>> check_length('the SimpleAssert module', 23)

You can override a Pythonic approach to treating numbers (integers, doubles, floats, complex values) and boolean values as not having length:

.. code-block:: python

    >>> check_length(True, 1, assign_length_to_others=True)
    >>> check_length(1, 1, assign_length_to_others=True)
    >>> check_length(1, 2, assign_length_to_others=True)
    Traceback (most recent call last):
        ...
    checkit.LengthError

Note that in the above example, we used the parameter operator. You can use this in several functions, and it can take up to eight operators from the operator module (use :code:`get_possible_operators()` too see the list, which includes :code:`eq`, :code:`le`, :code:`lt`, :code:`gt`, :code:`ge`, :code:`ne`, :code:`is_`, :code:`is_not`). Since these operators are functions, you provide them as function names, as we did above. 

Now we want to check the instance of the following string:

.. code-block:: python

    >>> my_string = '_'.join(str(item) for item in [1, 2, 3])

Instead of the following if-block to check its instance:

.. code-block:: python

    >>> if not isinstance(my_string, str):
    ...    raise TypeError('A string is needed')

you can do the following:

.. code-block:: python

    >>> check_instance(my_string, str, message='This is not a string')

If the condition is not met, it will raise :code:`TypeError`:

.. code-block:: python

    >>> check_instance('string', list, message='List is required here')
    Traceback (most recent call last):
        ...
    TypeError: List is required here

You can also assert that a path exists, using

.. code-block:: python

    >>> check_if_paths_exist('A:/my_file.txt')
    Traceback (most recent call last):
        ...
    FileNotFoundError

or that many paths exist:

.. code-block:: python

    >>> check_if_paths_exist(('A:/my_file.txt', 'A:/my_other_file.csv'))
    Traceback (most recent call last):
        ...
    FileNotFoundError

(The function works with both directories and files, but in both cases raises FileNotFoundError upon exception; you can change this default behavior using the :code:`handle_with` parameter.)

The module also offers two-item comparisons, also using the operator parameter:

.. code-block:: python

    >>> a, b, c = 2, 4, 2
    >>> check_comparison(a, lt, b)
    >>> check_comparison(b, gt, a)
    >>> check_comparison(a, eq, c)
    >>> check_comparison('a', eq, 'a')
    >>> check_comparison('a', ne, 'b')
    >>> check_comparison(['1', '2'], eq, ['1', '2'])
    >>> check_comparison(['1', '2'], ne, ['1', 2])

Use in testing
--------------

The module offers assert-like functions, which are simply aliases of the corresponding checkit functions: :code:`assert_if()`, :code:`assert_if_not()`, :code:`assert_instance()`, :code:`assert_length()` and :code:`assert_paths()`. You can use them in doctesting and pytesting, and their main advantage over the classical assertion expression is that they can use any exception you want, which makes testing output more informative. Also, due to the way they are written, you can design customized testing functions for particular situations.

For instance, instead of

.. code-block:: python

    >>> string = 'Shout Bamalama'
    >>> assert isinstance(string, str)
    >>> assert string != 'Silence prefered'
    >>> assert len(string) > 10

you can do the following:

.. code-block:: python

    >>> assert_instance(string, str)
    >>> check_if_not(string == 'Silence prefered')
    >>> assert_length(string, 10, operator=gt)

Issuing warnings
----------------

In order to issue a warning instead of raising an exception, simply choose a warning class (which must derive from the :code:`Warning` class). Since when issuing a warning you must provide a message, it's wise to define a message to use; otherwise, a default message 'Warning' will be output, which is of little use as it provides no further information. Consider the examples below:

.. code-block:: python

    >>> my_list = [1, 3, 3]
    >>> import warnings
    >>> with warnings.catch_warnings(record=True) as w:
    ...    check_length(my_list,
    ...                 2,
    ...                 handle_with=Warning,
    ...                 message='The list is too short')
    ...    print(w[-1].message)
    The list is too short
    >>> with warnings.catch_warnings(record=True) as w:
    ...    check_if(sum(my_list) > 10, Warning, 'Too small values of the list')
    ...    print(w[-1].message)
    Too small values of the list

Comments
--------

We thought of adding some more functions, like :code:`check_if_equal(item_1, item_2, message=None)`, but we think that :code:`check_if_equal(item_1, item_2)` is less readable than :code:`check_if(item_1 == item_2)` or :code:`check_if(item_1 is item_2)` (depending on what is being checked). For the same reason, we did not add functions :code:`check_if_unequal()`, :code:`check_if_greater_than()` and the like. In our opinion, the generic function :code:`check_if()` is enough to provide usability and readability.

The list of functions in the module is open, and we are open to suggestions, but any new function must meet all of the following conditions:

* It must be readable, in terms of both its code and using it in code, and it must be more readable than any other function from the module (see the above comparison of :code:`check_if(item_1 == item_2)` and :code:`check_if_equal(item_1, item_2)`) being used to check the same condition.
* Its name must clearly convey what is being checked; for checks, the name should follow the :code:`check_` convention.
* It uses a new exception class only if this is justified.
* It returns nothing when the checked condition is passed, and otherwise either raises an exception (so it mimics how assertions work, but offers the possibility to raise other exception types than :code:`AssertionError`) or issues a warning (but functions with other functionalities are also possible, like :code:`catch_check()`).
* It covers all possible situations that the check can meet (at least all those that make logical sense).
* Atypical situations are handled in a reasonable way; for instance, if the function does something in an atypical way for Python (such as how the :code:`check_length()` function handles the length of numbers), it is hidden in non-default behavior.
* It has a well-written docstring that includes doctests.
* Its behavior is fully covered by tests (both doctests and pytests).

More examples
-------------

You will see more examples in the doctest files collected in this folder.