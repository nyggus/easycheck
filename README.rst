.. image:: https://github.com/darsoo/easycheck/actions/workflows/python-package.yml/badge.svg
   :target: https://github.com/darsoo/easycheck/actions/workflows/python-package.yml
easycheck
=========

The :code:`easycheck` package offers a lightweight tool for running functionized checks within Python code; it also offers functions to be used in testing - particularly in doctests, but also in pytests, for which purpose some of the functions have dedicated aliases (starting off with :code:`assert_` instead of :code:`check_`). You can also switch off all :code:`easycheck` checks, by setting the :code:`"EASYCHECK_RUN"` environmental variable to :code:`"0"`.

The idea is to use the :code:`easycheck` functions to check conditions that are _not_ assertions. The checks work in the following general way: When a condition is met, nothing happens (in fact, the function returns :code:`None`); if it is violated, an exception is raised or a warning is issued. The main differences between :code:`easycheck` functions and assertions are as follows:

* Assertions are meant to be used conditions that _must_ be true (when only the code is correct). So, if an assertion is incorrect, it means something is wrong with the code. You should never use assertions to handle regular exceptions, like those related to data or arguments.
* Unlike assertions, :code:`easycheck` functions are to be used to check conditions related to things like data and argument values, and to handle regular exceptions.
* While assertions only raise :code:`AssertionError`, you can choose any exception to be raised by easycheck functions.
* When using :code:`easycheck`, instead of raising an exception, you can issue a warning.

The main :code:`easycheck` functions (with names starting off with :code:`check_`) are designed in such a way that they can be used as easy-to-understand code that checks whether one or more conditions are met. They can be used instead of :code:`if`-blocks, which are normally used to check conditions and raise exceptions (or issue warnings) if they are not met. So, you can do the following:

.. code-block:: python

    if not isinstance(x, (float, int)):
        raise TypeError('x must be a number')
    if x > 10:
        raise ValueError('Too high value of x')

or you can use :code:`easycheck` for this:

.. code-block:: python

    check_type(x, (float, int), message='x must be a number')
    check_if(x <= 10, ValueError, 'Too high value of x')

The :code:`easycheck` approach has two main advantages over this classical approach:

* It saves a little space; not much, since most often you'll end up with one line of code instead of two, but not always, particularly when you provide an exception type to be raised and a long message. 
* Mainly, it increases code simplicity and readability, since both the names of easycheck functions and their arguments are designed in such a way that the reader immediately understands what is being checked.

You can also issue a warning:

.. code-block:: python

    check_if(x <= 10,
             Warning,
             'For stable functioning of the function, '
             'x should not be greater than 10.')

The package also offers functions dedicated to testing, e.g.,

.. code-block:: python

    assert_type(x, (float, int))
    assert_if(x <= 10)

The :code:`message` argument has the default value of :code:`None`, which does the following. If the exception class provided in :code:`handle_with` is built-in (that is, can be found in :code:`dir(builtins)`), no message is provided. But if it is not a built-in exception (or warning) class, then the exception/warning class's docstring is taken as the message. This is a convenient way of providing a  typical message. If you want to customize the message (e.g., depending on the value of a variable), you should use a customized string (e.g., through an f-string). But if you do not want to use any message with a custom exception/warning, simply provide an empty string (:code:`message=''`).


Read about :code:`easycheck`
----------------------------

You will find more about assertions in `this article <https://medium.com/towards-data-science/python-assertions-or-checking-if-a-cat-is-a-dog-ce11c55d143>`_, entitled "Python Assertions, or Checking If a Cat Is a Dog" and published in *Towards Data Science*. It mentions :code:`easycheck`! You will read about :code:`easycheck` also in `the article "Comparing floating-point numbers with easycheck" <https://medium.com/towards-data-science/comparing-floating-point-numbers-with-easycheck-dcbae480f75f>`_  (also from *Towards Data Science*). The *Better Programming* article entitiled `"How to Overwrite AssertionError in Python and Use Custom Exceptions" <https://medium.com/better-programming/how-to-overwrite-asserterror-in-python-and-use-custom-exceptions-c0b252989977>`_, mentions the package, too.


Installing
----------

Install and update using pip:

.. code-block:: text

    pip install easycheck

Testing
-------

The package is covered with both pytests and doctests. The latter are included in both docstrings of all the functions, but also in `documentation files <https://github.com/nyggus/easycheck/tree/master/docs>`_.

Use in code to raise exceptions
-------------------------------

Here are several examples of a simple use of basic :code:`easycheck` functions. The most basic usage resembles the following:

.. code-block:: python

    check_if(a < 10)
	
This simply checks if :code:`a` is smaller than 10; if it is, nothing happens (in fact, :code:`check_if(a < 10)` returns :code:`None`). But if the condition is violated, the function raises :code:`AssertionError`. :code:`AssertionError` is the default exception returned by :code:`check_if()`, but you can change this:

.. code-block:: python

    check_if(a < 10, handle_with=ValueError)
    # or shorter and equally readable:
    check_if(a < 10, ValueError)

For built-in exceptions, like :code:`ValueError`, the default behaviour is to not print any message. For custom exceptions, however, the exception's docstring (`.__doc__`) serves as a message. You can use this when you create custom exceptions:

.. code-block:: python

    class IncorrectNameTypeError(Exception):
        """Argument name must be a string."""
    
    name = 40
    check_type(name, IncorrectNameTypeError)
    Traceback (most recent call last):
      ...
    IncorrectNameTypeError: Argument name must be a string.

If you want to ensure that no message is printed, even for a custom exception, override the default behaviour by passing an empty string :code:`message=''`. You can also add a custom message:

.. code-block:: python

    check_if(a < 10, handle_with=ValueError, message='Too high a')
    # or shorter and equally readable:
    check_if(a < 10, ValueError, 'Too high a')

Some other functions have different default errors; for instance, this call

.. code-block:: python

    check_type(a, expected_type=str)
    # or shorter:
    check_type(a, str)

will raise :code:`TypeError` while this

.. code-block:: python

    check_length([1, 2, 3], 1)
	
will raise :code:`LengthError` (an exception class defined in the :code:`easycheck` module).

Here is a list of :code:`easycheck` functions the module offers, along with their aliases to be used for testing:

* :code:`check_if()`, with the alias of :code:`assert_if()`; it's the most basic :code:`easycheck` function, similar to what you would get using :code:`if`;
* :code:`check_if_not()`, with the alias of :code:`assert_if_not()`; the opposite of :code:`check_if()`, helpful when you need to assure that a condition is _not_ met;
* :code:`check_if_isclose()`, with the alias of :code:`assert_if_isclose()`; to compare two floating-point numbers, based on :code:`match.isclose()` (see `this file <https://github.com/nyggus/easycheck/blob/master/docs/compare_floats_doctest.rst>`_);
* :code:`check_if_in_limits()`, with the alias of :code:`assert_if_in_limits()`;
* :code:`check_length()`, with the alias of :code:`assert_length()`; to compare length (equal to, smaller than, greater than, and the like);
* :code:`check_type()`, with the alias of :code:`assert_type()`; to check expected type, similar to :code:`isinstance()`;
* :code:`check_if_paths_exist()`, with the alias of :code:`assert_paths()`; to compare paths (or just one path) exist;
* :code:`check_comparison()` (used to compare two items); to compare to objectsm just like you would do using :code:`if obj1 != obj2: raise`
* :code:`check_all_ifs()`; used to check multiple conditions and return all the checks;
* :code:`check_argument()`; used to make one or more checks of a function's argument.

You can also use a :code:`catch_check()` function, if you want to catch an exception or a warning the :code:`easycheck` function you use would raise (see examples `here <https://github.com/nyggus/easycheck/blob/master/docs/catch_exceptions_doctest.rst>`_). Sometimes, however, you will do better using a :code:`try-except` block to catch exceptions (`see examples <https://github.com/nyggus/easycheck/blob/master/docs/use_with_try_doctest.rst>`_).

> Note that some :code:`easycheck` functions are simple wrappers around built-in functions, but their behavior is different, as they have the typical behavior of an :code:`easycheck` function: if a condition is not met, an exception is raised or an issue is raised.


Use in code to issue warnings
-----------------------------

In order to issue a warning if a condition is violated, simply use a warning class (in the :code:`handle_with` argument) instead of an exception class:

.. code-block:: python

    check_if(2 > 1, Warning, 'Too high a value')
    check_length([1, 2, 3], 10, Warning, 'Too short list with data')

Remember to always use a message with warnings, in order to make them meaningful. (See more in `use_with_warnings_doctest.rst <https://github.com/nyggus/easycheck/blob/master/docs/use_with_warnings_doctest.rst>`_).


Of course, you can use a custom warning:

.. code-block:: python

    class TooSmallSampleSize(Warning):
        """Results for samples size below 100 can be unstable."""
    
    n = 50
    check_if(n >= 100, TooSmallSampleSize)
    ... TooSmallSampleSize: Results for samples size below 100 can be unstable.
      warnings.warn(message, error)


Use in code, an example
-----------------------

Imagine you want to connect to a database; if the connection fails for any reason, you want to read an archived flat file. (We will use some undefined functions whose names will clearly convey what the functions do.)

.. code-block:: python

    from easycheck import check_if, check_if_paths_exist
    
    class DataBaseConnectionError(Exception):
        pass
    
    def get_data_from_db(db_details, db_credentials):
        try:
            connect_to_db(db_details, db_credentials)
        except:
            return False
        data = get_records_from_db()
        return data

The :code:`easycheck` code could look like the following:

.. code-block:: python

    def get_data(db_details, db_credentials):
        data = get_data_from_db(db_details, db_credentials)
        check_if(
            data,
            handle_with=DataBaseConnectionError,
            message='Cannot communicate with the database'
            )
        return data
              
You can of course handle this exception, for example like here:

.. code-block:: python

    def get_data(db_details, db_credentials, archived_data_file):
        data = get_data_from_db(db_details, db_credentials)
        try:
            check_if(
                data,
                handle_with=DataBaseConnectionError,
                message='Cannot communicate with the database'
            )
        except DataBaseConnectionError:
            check_if_paths_exist(archived_data_file)
            with open(archived_data_file) as f:
                data = f.readlines()
        return data
    
Of course, you might use here a dedicated context manager. Sure, you can write it in a shorter way, without :code:`easycheck`, but the flow of information will not be as smooth, resulting in less readability:

.. code-block:: python

    def get_data(db_details, db_credentials, archived_data_file):
        data = get_data_from_db(db_details, db_credentials)
        if not data:
            with open(archived_data_file) as f:
                data = f.readlines()
        return data

Of course, the :code:`open()` context manager will itself throw an error, but when you use the :code:`check_if()` function and explicitly define an exception class, you clearly show the reader that you're checking if this file exists and raise a particular exception if it doesn't.
        
Use in testing
--------------

As mentioned above, most :code:`easycheck` functions have aliases to be used in testing. Of course, you can use :code:`check_if()`, but to align with the common use of assertions, the :code:`easycheck` module offers those aliases so that the reader will immediately see that you're using these functions to test. Consider these examples:

.. code-block:: python

    # Using assertions
    def test_something():
        a, b = my_function_1(), my_function_2()

        assert a == 2; 
        assert isinstance(a, int)
        assert isinstance(b, tuple)
        assert len(b) == 5
		
    # Using easycheck assert-like functions:
    def test_something():
        a, b = my_function_1(), my_function_2()
        
        assert_if(a == 2)
        assert_type(a, int)
        assert_type(b, tuple)
        assert_length(b, 5)

Note that only the first one will raise :code:`AssertionError` while the others will raise more meaningful errors (:code:`TypeError` and :code:`LengthError`), which may better explain the reasons that the tests did not pass.

You will find more about using :code:`easycheck` in `use_in_testing_doctest.rst <https://github.com/nyggus/easycheck/blob/master/docs/use_in_testing_doctest.rst>`_.

Other examples
--------------

You will find a number of examples in `doctest files <https://github.com/nyggus/easycheck/tree/master/docs/>`_, which also serve as doctests.


Switching off :code:`easycheck`
-------------------------------

If you want to maximize performance, you may wish to switch off :code:`easycheck` checks. You would get the greatest increase in performance by removing (or commenting out) all calls to :code:`easycheck` functions, but this can be inconvenient. Hence, :code:`easycheck` offers you a more convenient way of doing so, namely, switching off via an environmental variable. This will be less efficient, as this will mean calling an empty function instead of actual :code:`easycheck` functions. While not the most performant, this approach can increase performance quite significantly. Its obvious advantage is that you do not need to do anything else than just setting the :code:`"EASYCHECK_RUN"` environmental variable to :code:`"0"`:

.. code-block:: shell

    > EASYCHECK_RUN = 0
    > python my_script.py

The my_script.py script will be run with all :code:`easycheck` functions replaced with an empty function.

You can also switch off easycheck directly from Python:

.. code-block:: python

    import os

    os.environ["EASYCHECK_RUN"] = "0"

> **Warning**: Do remember to use this option wisely. While it will increase performance, it can also change the behavior of the Python program.


Changelog
---------

* Version 0.6.0 came with significant optimization of performance. Before, :code:`easycheck` functions performed internal checks of the argument values provided to the function call. Most of these checks are not performed anymore, at least not for the most significant :code:`easycheck` functions, such as :code:`check_if()` or :code:`check_type()`. Some checks, however, are still done. These are mainly checks without which the behavior of the function would be either unwanted or unexpected. We decided to remove all checks that do not change much; for instance, they raise an error due to an incorrect type of an argument value — even though it would be raised anyway, but by the internal Python process, not by the :code:`easycheck` function itself. The point is to remove such unnecessary checks and that way remove the unnecessary :code:`if` blocks, which certainly add some cost to execution time. While one such check costs almost nothing, many of them (e.g., in a long loop) can mean a significant cost. As of version 0.6.0, we will try to optimize the performance of :code:`easycheck` by getting rid of such overhead costs, unless they are important for the behavior of the corresponding :code:`easycheck` function.