Comparing floating-point numbers
-------------------------------------------

To find out whether two floats are close enough, you can use the :code:`math.isclose()` function. :code:`easycheck` offers a :code:`check_if_isclose()` function, which in fact is a simple wrapper around :code:`math.isclose()`; the difference is that when the condition is not met, :code:`check_if_isclose()` throws an error (or issues a warning), while :code:`math.isclose()` would return `False`. You can use both to compare two floats using either :code:`abs_tol` (for absolute tolerance) or :code:`rel_tol` () for relative tolerance. In :code:`check_if_isclose()` (and its testing counterpart, :code:`assert_if_isclose()`), you can define both and both checks will be performed. 

> The default settings of :code:`check_if_isclose()` (and :code:`assert_if_isclose()`) are exactly the same as those of :code:`math.isclose()`: :code:`rel_tol=1e-09` and :code:`abs_tol=0.0`. So, if you want to use only :code:`abs_tol`, remember to set :code:`rel_tol` to 0, as otherwise it will be used.

Here's how you can use this function

.. code-block:: python

    >>> from easycheck import check_if_isclose
    >>> check_if_isclose(2.01, 2.02, abs_tol=0.05)
    
As you see, nothing has happened, as indeed the absolute difference of 2.01 and 2.02 is 0.01, which is smaller than 0.05 (:code:`abs_tol`) - hence the check passes. But

    >>> check_if_isclose(2.01, 2.02, abs_tol=0.005)
    Traceback (most recent call last):
        ...
    easycheck.easycheck.NotCloseEnoughError: The two float numbers are not close enough.

If you do not to see the message after the exception's name, provide an empty string as a message:

    >>> check_if_isclose(2.01, 2.02, abs_tol=0.005, message='')
    Traceback (most recent call last):
        ...
    easycheck.easycheck.NotCloseEnoughError


Do note that the first two arguments (the numbers) are positional-only while all the other arguments are keyword-only. This makes you provide the argument's name, and thanks to this, any call to this function will be clearer. For instance, :code:`check_if_isclose(2.01, 2.02, 0.05)` would be less clear than :code:`check_if_isclose(2.01, 2.02, abs_tol=0.05)`.

The default exception used by this function is :code:`easycheck:NotCloseEnoughError`. It's very clear and often does not even require any additional message. But you can, of course, change it:

    >>> check_if_isclose(2.01, 2.02,
    ...                  abs_tol=0.005,
    ...                  handle_with=ValueError)
    Traceback (most recent call last):
        ...
    ValueError
    >>> check_if_isclose(2.01, 2.02,
    ...                  abs_tol=0.005,
    ...                  handle_with=ValueError,
    ...                  message="The two values are not close enough")
    Traceback (most recent call last):
        ...
    ValueError: The two values are not close enough


In testing, you should rather use :code:`assert_if_isclose()`; its API is exactly the same as that of :code:`check_if_isclose()`.
