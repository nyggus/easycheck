checkit
======

checkit is a lightweight tool for running functionized assertions within Python code, outside of testing, though it can be used in testing, too. The idea is to use the checkit functions in a similar way as assertions: when a condition you check is met, nothing happens; if it's violated, an exception is raised. Nonetheless, while you should not use assertions in your Python code, the checkit functions are designed to be used in code. You can of course use them in testing (whether pytests or doctests).

The main checkit functions (starting off with check_) are designed so that they cna be used as easy-to-understand one-liners. They can be used instead of if-blocks, which you normally use to check conditions and raise exceptions if the conditions are not met. The checkit approach has two main advantages:He

(i) it saves a little space; not much, since most of the time you'll end up with one line of code instead of two; but mainly
(ii) it increases code simplicity and readability, since both the names of checkit functions and their arguments are designed in such a way that the reader immediately knows what is being checked.

NOTE: the checkit package should be used to check conditions in assertion-like situations. use checkit when you want to ensure that everything is right so that you can follow, or that something is wrong; if something is wrong indeed, you can easily handle exceptions. So, checkit is not designed to be used to check conditions in your code (like in if-elif blocks that do not raise exceptions). 

Dev installation
----------------

(temporary section)

.. code-block:: text

    python -m venv env
    . env/bin/activate
    pip install -e .
    pip install pytest wheel
    python setup.py sdist bdist_wheel

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
    python -m doctest src/checkit/checks.py src/checkit/comparisons.py


Example 1: Use checkit in code
------------------------------

The basic aim of checkit is to give you quick-to-use, simple and readable assertion-like functions to check conditions. They are assert-like because what you do is indeed similar to assert expressions, since you: (i) check a condition, (ii) do nothing when it's met, but (iii) raise an exception when it is not. However, checkit differs from assertions in one significant functionality: Unlike when using `assert`, you can raise any error you want. What is perhaps more important, you are not supposed to use the assert expression in code outside of testing, but you can use checkit assert-like functions (starting off with check_).

Of course, checkit is to help you when Python does not handle a particular situation. For example, it does so when you're trying to divide a number by zero, so you need not use checkit then. But there is a plethora of various situations which you want to handle.

Here are several examples of the simplest uses of checkit:

.. code-block:: python
    
    def get_family_name(full_name):
        check_if_not(full_name is None,
                 error=TypeError,
                 message='Missing name')
        check_instance(full_name, str, message='Full name must be string')
        check_if(' ' in full_name.strip(),
            error=ValueError,
            message=('No space in full name:'
                     ' impossible to split first and second name')
        
        return full_name.split(' ')[0]
    
If something is wrong, the corresponding exception is raised. If you need to catch these exceptions and handle them accordingly, you can certainly do so (note that two different types of errors can be raised by `get_family_name()`).
        
Above, the `check_instance()` itself function can handle the None situation! This will make the code simpler and shorter:

.. code-block:: python
    
    def get_family_name(full_name):
        check_instance(full_name, (str, None), message='Full name must be string')
        check_if(' ' in full_name.strip(),
            error=ValueError,
            message=('No space in full name:'
                     ' impossible to split first and second name')
        
        return full_name.split(' ')[0]

    
Without checkit, this function might have the following form:
    
.. code-block:: python

    def get_first_name(full_name):
        if full_name is None:
            raise TypeError('Missing full name')
        elif not isinstance(full_name, str):
            raise TypeError('Full name must be string')
        elif ' ' not in full_name.strip():
            raise ValueError('No space in full name:'
                             ' impossible to split first and second name')
        
        return full_name.split(' ')[0]
    
    In the shortest version (with default values), we might do it like here:
    
.. code-block:: python

    def get_first_name(full_name):
        check_instance(full_name, (str, None))
        check_if(' ' in full_name.strip())
        
        return full_name.split(' ')[0]
    
with its non-checkit counterpart being rather less readable:

.. code-block:: python

    def get_first_name(full_name):
        if (full_name is None
            or not isinstance(full_name, str) or
            ' ' not in full_name.strip()):
            raise Exception
        
        return full_name.split(' ')[0]

But the checkit module offers also a dedicated function for checking arguments, `check_argument`. It offers much more flexibility in some terms (combining various checks) but less in others (since it uses its own messages only). We could use the following approach to reach the same objective:

.. code-block:: python
    
    def get_family_name(full_name):
        check_argument(
            'full_name', full_name,
            expected_instance=(str, None),
            expected_condition=' ' in full_name.strip()
            )
        
        return full_name.split(' ')[0]

If the instance condition is violated, it would throw ArgumentValueError with the following message: "Incorrect instance of full_name". If the expected_condition is violated, then the ArgumentValueError would be raised with the following message: "Provided condition violated for full_name". So, it's up to you which approach you will choose: the `check_argument()` function, which offers a dedicated API to check arguments, but without a possibility to change error messages, or a number of function calls that check the particular aspects of the argument you want to check.

Example 2: Use checkit in code and handle errors
---------------------------------------------

You want to connect to a database; if the connection fails for any reason, you want to read an archived flat file. (We will use some undefined functions whose names will clearly convey what the functions are to do.)

.. code-block:: python

    import checkit.checks as checker
    
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

..code-block:: python

    def get_data(db_details, db_credentials, archived_data_file):
        data = get_data_from_db(db_details, db_credentials)
        try:
            check_if(
            data,
            error=DataBaseConnectionError,
            message='Cannot communicate with the database'
            )
        except DataBaseConnectionError:
            check_if_file_exists(archived_data_file)
            with open(archived_data_file) as f:
                data = f.readlines()
        return data
    
You can write it in a shorter way, without checkit, but the flow of information will not that that smooth, resulting in lower readability:

..code-block:: python

    def get_data(db_details, db_credentials, archived_data_file):
            data = get_data_from_db(db_details, db_credentials)
            if not data:
                with open(archived_data_file) as f:
                    data = f.readlines()
            return data

Of course, the `open()` context manager will itself throw anm error, but when you use the `check_if()` function and explicitely define an exception class, you clearly show the reader that you're checking if this file exists and raise a particular exception if it doesn't.
        
Example 3: Catching instead of raising exceptions
-------------------------------------------------

If you do not want to raise exceptions but catch them, you can do so using the `catch_check()` function:

..code-block:: python

    my_check = catch_check(check_if, 2>2, ValueError)
    my_check
    # ValueError()
    type(my_check)
    # <class 'ValueError'>
    # check_instance(my_check, ValueError)
    raise(my_check)
    #Traceback (most recent call last):
    #    ...
    #ValueError

Example 4: Testing
--------------------

Although we stress that checkit functions are dedicated to be used in code (unlike classical assertions), it does not mean that they cannot be used in testing. We do use them from time to time in doctests (although we not to overuse them, to not risk accusations that we are testing our solution with our solution; this is why we do not use the module in pytests at all). But the checkit functions can easily replace many assertions. Consider the below pairs of assertions to be used in testing.

.. code-block: python

    def test_something():
        a, b = my_function_1(), my_function_2()
        
        assert a == 2; 
        # and
        check_if(a == 2)
        
        assert isinstance(a, int)
        # and
        check_instance(a, int)
        
        assert isinstance(b, tuple)
        assert len(b) == 5
        # and
        check_instance(b, tuple)
        check_length(b, 5)
              
        
        