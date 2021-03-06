easycheck
=========

The :code:`easycheck` package offers a lightweight tool for running functionized assertion-like checks within Python code; it also offers functions to be used in testing - particularly in doctests, but also in pytests, for which purpose some of the functions have dedicated aliases. The idea is to use the :code:`easycheck` functions in a similar way as assertions, but with more functionality and with a slightly different aim: When a condition you define is met, nothing happens (in fact, the function returns :code:`None`); if the condition is violated, an exception is raised or a warning is issued. The main differences between :code:`easycheck` functions and assertions are as follows:

* While you should not use assertions in your Python code, you can do so with the :code:`easycheck` functions.
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

    check_instance(x, (float, int), message='x must be a number')
    check_if(x <= 10, ValueError, 'Too high value of x')

The :code:`easycheck` approach has two main advantages over this classical approach:

* It saves a little space; not much, since most often you'll end up with one line of code instead of two, but not always, particularly when you provide an exception type to be raised and a long message. 
* Mainly, it increases code simplicity and readability, since both the names of easycheck functions and their arguments are designed in such a way that the reader immediately understands what is being checked.

You can also issue a warning:

.. code-block:: python

    check_if(x <= 10, Warning, 'For stable functioning of the function, x should not be greater than 10.')

The package also offers functions dedicated to testing, e.g.,

.. code-block:: python

    assert_instance(x, (float, int))
    assert_if(x <= 10)

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

but you can also add a message:

.. code-block:: python

    check_if(a < 10, handle_with=ValueError, message='Too high a')
    # or shorter and equally readable:
    check_if(a < 10, ValueError, 'Too high a')

Some other functions have different default errors; for instance, this call

.. code-block:: python

    check_instance(a, expected_type=str)
    # or shorter:
    check_instance(a, str)

will raise :code:`TypeError` while this

.. code-block:: python

    check_length([1, 2, 3], 1)
	
will raise :code:`LengthError` (an exception class defined in the :code:`easycheck` module).

Here is a list of :code:`easycheck` functions the module offers, along with their aliases to be used for testing:

* :code:`check_if()`, with the alias of :code:`assert_if()`
* :code:`check_if_not()`, with the alias of :code:`assert_if_not()`
* :code:`check_length()`, with the alias of :code:`assert_length()`
* :code:`check_instance()`, with the alias of :code:`assert_instance()`
* :code:`check_if_paths_exist()`, with the alias of :code:`assert_paths()`
* :code:`check_comparison()` (used to compare two items)
* :code:`check_all_ifs()` (used to check multiple conditions and return all the checks)
* :code:`check_argument()` (used to make several checks of a function's argument)

You can also use a :code:`catch_check()` function, if you want to catch an exception or a warning the :code:`easycheck` function you use would raise (see examples `here <https://github.com/nyggus/easycheck/blob/master/docs/catch_exceptions_doctest.rst>`_). Sometimes, however, you will do better using a :code:`try-except` block to catch exceptions (`see examples <https://github.com/nyggus/easycheck/blob/master/docs/use_with_try_doctest.rst>`_).

Use in code to issue warnings
-----------------------------

In order to issue a warning if a condition is violated, simply use a warning class (in the :code:`handle_with` argument) instead of an exception class:

.. code-block:: python

    check_if(2 > 1, Warning, 'Too high a value')
    check_length([1, 2, 3], 10, Warning, 'Too short list with data')

Remember to always use a message with warnings, in order to make them meaningful. (See more in `use_with_warnings_doctest.rst <https://github.com/nyggus/easycheck/blob/master/docs/use_with_warnings_doctest.rst>`_).


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
        assert_instance(a, int)
        assert_instance(b, tuple)
        assert_length(b, 5)

Note that only the first one will raise :code:`AssertionError` while the others will raise more meaningful errors (:code:`TypeError` and :code:`LengthError`), which may better explain the reasons that the tests did not pass.

You will find more about using :code:`easycheck` in `use_in_testing_doctest.rst <https://github.com/nyggus/easycheck/blob/master/docs/use_in_testing_doctest.rst>`_.

Other examples
--------------

You will find a number of examples in `doctest files <https://github.com/nyggus/easycheck/tree/master/docs/>`_, which also serve as doctests.
