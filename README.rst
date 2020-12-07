checkit
=======

checkit is a lightweight tool for running functionized assertion-like checks within Python code; it also offers functions to be used in testing (particularly in doctests, but also in pytests, for which purpose some of the functions have dedicated aliases). The idea is to use the checkit functions in a similar way as assertions, but with more functionalities and with a slightly different aim: When a condition you check is met, nothing happens (in fact, the function returns None); if it's violated, an exception is raised. Two main  difference between checkit functions and assertions are that (i) while you should not use assertions in your Python code, the checkit module is designed in a way so its function can be used in code; and (ii) while assertions raise the :code:`AssertionError`, you can choose any exception to be raised by checkit functions.

Main checkit functions (starting off with :code:`check_`) are designed so that they can be used as easy-to-understand code that ensures that required conditions are met. They can be used instead of if-blocks, which you normally use to check conditions and raise exceptions if they are not met. So, you can do the following:

.. code-block:: python

    if not isinstance(x, (float, int)):
	    raise TypeError('x must be a number')
	if x > 10:
	    raise ValueError('Too high value of x')

or you can use checkit for this:

.. code-block:: python

    check_instance(x, (float, int), message='x must be a number')
	check_if(x <= 10, ValueError, 'Too high value of x')

The checkit approach has two main advantages over this classical approach:
* it saves a little space; not much, since most of the time you'll end up with one line of code instead of two, and not always, particularly when you provide an exception type to be raised and a long message; but mainly 
* it increases code simplicity and readability, since both the names of checkit functions and their arguments are designed in such a way that the reader immediately sees what is being checked.

NOTE: the checkit package should be used to check conditions in assertion-like situations. Use checkit when you want to ensure that everything is right so that you can follow, or that something is wrong; if something is wrong indeed, you can easily handle the exception raised. So, checkit is not designed to replace regular if-elif blocks.

Installing
----------

Install and update using pip:

.. code-block:: text

    pip install -U checkit

Testing
--------

The package is covered with both doctests and pytests. You can run them using the following commands run in shell from the package's root folder, after activating the virtual environment:

.. code-block:: text

    python -m pytest
    python -m doctest src/checkit.py tests/doctests/*.txt


Use in code, example 1
----------------------

Here are several examples of a simple use of basic checkit functions. The most basic use resembles the following:

.. code-block:: python

    check_if(a < 10)
	
This simply checks if :code:`a` is smaller than 10; if it is, nothing happens (in fact, :code:`check_if(a < 10)` returns :code:`None`), but if the condition is violated, the function raises :code:`AssertionError`. :code:`AssertionError` is the default exception of :code:`check_if()`, but you can change it:

.. code-block:: python

    check_if(a < 10, error=ValueError)
	# or shorter and equally readable: check_if(a < 10, ValueError)

but you can also add a message:

.. code-block:: python

    check_if(a < 10, error=ValueError, message='Too high a')
	# or shorter and equally readable: check_if(a < 10, ValueError, 'Too high a')

Some other functions have different default errors; for instance, this call

.. code-block:: python

    check_instance(a, expected_instance=str)
	# or check_instance(a, str)

will raise :code:`TypeError` while this

.. code-block:: python

    check_length([1, 2, 3])
	
will raise :code:`LengthError` (an exception defined in the checkit module).

Here is a list of checkit functions the module offers, along with their aliases to be used for testing:

* :code:`check_if()`, with alias of :code:`assert_if()`
* :code:`check_if_not()`, with alias of :code:`assert_if_not()`
* :code:`check_length()`, with alias of :code:`assert_length()`
* :code:`check_instance()`, with alias of :code:`assert_instance()`
* :code:`check_if_paths_exist()`, with aliast of :code:`assert_paths()`
* :code:`check_all_ifs()` (used to check multiple conditions and return all the checks)
* :code:`check_argument()` (used to make several checks of a function's argument)

You can also use a :code:`catch_check()` function, if you want to catch an exception the checkit function you use would raise.

Use in code, example 2
----------------------

You want to connect to a database; if the connection fails for any reason, you want to read an archived flat file. (We will use some undefined functions whose names will clearly convey what the functions are to do.)

.. code-block:: python

    from checkit import check_if, check_if_paths_exist
    
    class DataBaseConnectionError(Exception):
        pass
    
    def get_data_from_db(db_details, db_credentials):
        try:
            connect_to_db(db_details, db_credentials)
        except:
            return False
        data = get_records_from_db()
        return data

The checkit code could look like the following:

.. code-block:: python

    def get_data(db_details, db_credentials):
        data = get_data_from_db(db_details, db_credentials)
        check_if(
            data,
            error=DataBaseConnectionError,
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
                error=DataBaseConnectionError,
                message='Cannot communicate with the database'
            )
        except DataBaseConnectionError:
            check_if_paths_exist(archived_data_file)
            with open(archived_data_file) as f:
                data = f.readlines()
        return data
    
Of course, you might use here a dedicated context manager. Sure, you can write it in a shorter way, without checkit, but the flow of information will not be that smooth, resulting in lower readability:

.. code-block:: python

    def get_data(db_details, db_credentials, archived_data_file):
            data = get_data_from_db(db_details, db_credentials)
            if not data:
                with open(archived_data_file) as f:
                    data = f.readlines()
            return data

Of course, the :code:`open()` context manager will itself throw an error, but when you use the :code:`check_if()` function and explicitely define an exception class, you clearly show the reader that you're checking if this file exists and raise a particular exception if it doesn't.
        
Use in testing
--------------

As mentioned above, most functions have their aliases to be used in testing. Of course, you can use :code:`check_if()`, but to align with the common use of assertions, the checkit module offers those aliases so that the reader will immediately see that you're using these functions to test. Consider these examples:

.. code-block:: python

	# Using assertions
	def test_something():
		a, b = my_function_1(), my_function_2()
		
		assert a == 2; 
		assert isinstance(a, int)
		assert isinstance(b, tuple)
		assert len(b) == 5
		
	# Using checkit assert-like functions:

	def test_something():
        a, b = my_function_1(), my_function_2()
        
        assert_if(a == 2)
        assert_instance(a, int)
        assert_instance(b, tuple)
        assert_length(b, 5)

Do note that only the first one will raise :code:`AssertionError` while the others will raise more meaningful errors (:code:`TypeError` and :code:`LengthError`), which might help you out interpret the tests that did not pass.

Other examples
--------------

You will find a number of examples if doctest files located in the package's tests/doctests folder.
