checkit
======

checkit is a lightweight tool for running functionized assertion-like checks within Python code (so outside of testing). The idea is to use the checkit functions in a similar way as assertions, but with more functionalities and with a slightly different aim: when a condition you check is met, nothing happens (in fact, the function return None); if it's violated, an exception is raised. Nonetheless, while you should not use assertions in your Python code, the checkit module is designed in a ways so its function can be used in code. You can also use them in testing (whether in pytests or in doctests).

The main checkit functions (starting off with check_) are designed so that they can be used as easy-to-understand one-liners. They can be used instead of if-blocks, which you normally use to check conditions and raise exceptions if they are not met. The checkit approach has two main advantages over this classical approach:

(i) it saves a little space; not much, since most of the time you'll end up with one line of code instead of two, and not always, particularly when you provide an exception type to be raised and a long message; 
can (ii) but mainly it increases code simplicity and readability, since both the names of checkit functions and their arguments are designed in such a way that the reader immediately see what is being checked.

NOTE: the checkit package should be used to check conditions in assertion-like situations. Use checkit when you want to ensure that everything is right so that you can follow, or that something is wrong; if something is wrong indeed, you can easily handle the exception raised. So, checkit is not designed to be used to check conditions in your code (like in if-elif blocks that do not raise exceptions).

Dev installation
----------------

(temporary section)

.. code-block:: text

    python -m venv env
    . env/bin/activate
    pip install -e .
    pip install pytest

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
    python -m doctest src/checkit/*.py


Example 1: Use checkit in code
------------------------------

The basic aim of checkit is to provide you with quick-to-use, simple and readable assertion-like functions to make sure that particular conditions you are interested in are met. They are assert-like because what you do is indeed similar to what assert expressions do, since the functions: (i) check a condition, (ii) do nothing when it's met, but (iii) raise an exception when it is not. However, checkit differs from assertions in one significant functionality: Unlike when using the :code:`assert` expression, you can raise any error you want. What is perhaps more important, you are not supposed to use the assert expression in code outside of testing, but you can do so with checkit assert-like functions (starting off with check_).

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
    
If something is wrong, the corresponding exception is raised. If you need to catch these exceptions and handle them accordingly, you can certainly do so (note that two different types of errors can be raised by :code:`get_family_name()`).
        
Above, the :code:`check_instance()` itself function can handle the None situation! This will make the code simpler and shorter:

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

But the checkit module offers also a dedicated function for checking arguments, :code:`check_argument`. It offers much more flexibility in some terms (combining various checks) but less in others (since it uses its own messages only). We could use the following approach to reach the same objective:

.. code-block:: python
    
    def get_family_name(full_name):
        check_argument(
            'full_name', full_name,
            expected_instance=(str, None),
            expected_condition=' ' in full_name.strip()
            )
        
        return full_name.split(' ')[0]

If the instance condition is violated, it would throw ArgumentValueError with the following message: "Incorrect instance of full_name; valid instance(s): <class 'str'>". If the expected_condition is violated, then the ArgumentValueError would be raised with the following message: "Provided condition violated for full_name". So, it's up to you which approach you will choose: the :code:`check_argument()` function, which offers a dedicated API to check arguments, or a number of function calls that check the particular aspects of the argument you want to check. In :code:`check_argument()`, you can also use a dedicated message, although this functionality is less obvious when you are checking several aspects of the argument at the same time (in which case it's better to use the in-built default messages).

Example 2: Use checkit in code: handle errors
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
            check_if_file_exists(archived_data_file)
            with open(archived_data_file) as f:
                data = f.readlines()
        return data
    
Of course, you might use here a dedicated context manager. Sure, you can write it in a shorter way, without checkit, but the flow of information will not that that smooth, resulting in lower readability:

.. code-block:: python

    def get_data(db_details, db_credentials, archived_data_file):
            data = get_data_from_db(db_details, db_credentials)
            if not data:
                with open(archived_data_file) as f:
                    data = f.readlines()
            return data

Of course, the :code:`open()` context manager will itself throw an error, but when you use the :code:`check_if()` function and explicitely define an exception class, you clearly show the reader that you're checking if this file exists and raise a particular exception if it doesn't.
        
Example 3: Readability: the check_argument function
---------------------------------------------------

Compare the two following functions (the first one is the actual function from the checkit function), both doing the same thing, though with slightly different messages they might provide in terms an exception is raised. The first one is written in a classical way, while the second using the :code:`check_argument()` function:

.. code-block:: python

    import checkit


    def _check_checkit_arguments(error=None,
                                 message=None,
                                 condition=None,
                                 operator=None,
                                 assign_length_to_numbers=None,
                                 execution_mode=None,
                                 expected_length=None,
                                 expected_instance=None):
        if error is not None:
            if not isinstance(error(), Exception):
                raise TypeError('error must be an exception')
        if message is not None:
            if not isinstance(message, str):
                raise TypeError('message must be either None or string')
        if condition is not None:
            if not isinstance(condition, bool):
                raise ValueError('The condition does not give a True/False answer')
        if operator is not None:
            if operator not in get_possible_operators():
                raise OperatorError(
                    'Unacceptable operator. Check get_possible_operators()')
        if expected_length is not None:
            if not isinstance(expected_length, (int, float)):
                raise TypeError(
                    'expected_length should be an integer (or a float)')
        if assign_length_to_numbers is not None:
            if not isinstance(assign_length_to_numbers, bool):
                raise TypeError('assign_length_to_numbers should be a bool')
        if execution_mode is not None:
            if not execution_mode in ('raise', 'return'):
                raise ValueError(
                    'execution_mode should be either "raise" or "return"')
        if expected_instance is not None:
            if not isinstance(expected_instance, (tuple, list)):
                if not isinstance(expected_instance, type):
                    raise TypeError('expected_instance must be a valid type')
            else:
                expected_instance = [i for i in expected_instance if i is not None]
                for instance in expected_instance:
                    if not isinstance(instance, type):
                        raise TypeError(
                            'all items in expected_instance must be valid types')
    
    
    def _check_checkit_arguments_checkit(error=None,
                                 message=None,
                                 condition=None,
                                 operator=None,
                                 assign_length_to_numbers=None,
                                 execution_mode=None,
                                 expected_length=None,
                                 expected_instance=None):
        if error is not None:
            checkit.check_argument('error', error(),
                                   expected_instance=Exception,
                                   message='error must be an exception')
        if message is not None:
            checkit.check_argument('message', message,
                                   expected_instance=str,
                                   message='message must be either None or string')
        if condition is not None:
            checkit.check_argument('condition', condition, expected_instance=bool)
        if operator is not None:
            checkit.check_argument(
                'operator', operator,
                choices=get_possible_operators(),
                error=OperatorError,
                message='Unacceptable operator. Check get_possible_operators()')
        if expected_length is not None:
            checkit.check_argument('expected_length', expected_length,
                                   expected_instance=(int, float))
        if assign_length_to_numbers is not None:
            checkit.check_argument('assign_length_to_numbers',
                                   assign_length_to_numbers,
                                   expected_instance=bool)
        if execution_mode is not None:
            checkit.check_argument('execution_mode', execution_mode,
                                   expected_choices=('raise', 'return'))
        if expected_instance is not None:
            checkit.check_argument(
                argument_name='expected_instance',
                argument=expected_instance,
                expected_instance=type)

It's all about readability, so we will leave you the decision which of the two is more readable. In both cases we kept line length of 79 or shorter. Note that in a couple of cases in the latter function, we did not have to use a message since the default one would do the job very well. 

Unfortunately, we used the former version of the function in the package itself, in order to avoid possible recursion. (Like in, check arguments in check_if using a function that uses check_if to check the arguments in check_if, and so on...)


Example 4: Catching instead of raising exceptions
-------------------------------------------------

If you do not want to raise exceptions but to catch them, you can do so using the :code:`catch_check()` function:

.. code-block:: python

    >>> my_check = catch_check(check_if, 2>2, ValueError)
    >>> my_check
    ValueError()
    >>> type(my_check)
    <class 'ValueError'>
    >>> check_instance(my_check, ValueError)
    >>> raise(my_check)
    Traceback (most recent call last):
        ...
    ValueError

Example 5: Testing
--------------------

Although we stress that checkit functions are dedicated to be used in code (unlike classical assertions), it does not mean that they cannot be used in testing. We do use them from time to time in doctests (although we not to overuse them, to not risk accusations that we are testing our solution with our solution; this is why we do not use the module in pytests at all). But the checkit functions can easily replace many assertions. Consider the below pairs of assertions to be used in testing.

.. code-block: python

    def test_something():
        a, b = my_function_1(), my_function_2()
        
        assert a == 2; 
        # or
        check_if(a == 2)
        
        assert isinstance(a, int)
        # or
        check_instance(a, int)
        
        assert isinstance(b, tuple)
        assert len(b) == 5
        # or
        check_instance(b, tuple)
        check_length(b, 5)
              
IDEA: makes aliases to be used in testing, like here:

.. code-block:: python

    def test_something():
        a, b = my_function_1(), my_function_2()
        
        assert a == 2; 
        # or
        assert_if(a == 2)
        
        assert isinstance(a, int)
        # or
        assert_instance(a, int)
        
        assert isinstance(b, tuple)
        assert len(b) == 5
        # or
        assert_instance(b, tuple)
        assert_length(b, 5)

It would simply mean making :code:`assert_if = check_if; assert_instance = check_instance` and so on. What do you think about it? 