checkit
======

checkit is a lightweight tool for running functionized assertions within Python code, outside of testing, though it can be used in testing, too. The idea is to use the checkit functions in a similar way as assertions: when a condition you check is met, nothing happens; if it's violated, an exception is raised. Nonetheless, while you should not use assertions in your Python code, the checkit functions are designed to be used in code. You can of course use them in testing (whether pytests or doctests).

The main checkit functions (starting off with check_) are designed so that they cna be used as easy-to-understand one-liners. They can be used instead of if-blocks, which you normally use to check conditions and raise exceptions if the conditions are not met. The checkit approach has two main advantages:

(i) it saves a little space; not much, since most of the time you'll end up with one line of code instead of two; but mainly
(ii) it increases code simplicity and readability, since both the names of checkit functions and their arguments are designed in such a way that the reader immediately knows what is being checked.

NOTE: the checkit package should be used to check conditions in assertion-like situations. use checkit when you want to ensure that everything is right so that you can follow, or that something is wrong; if something is wrong indeed, you can easily handle exceptions. So, checkit is not designed to be used to check conditions in your code (like in if-elif blocks that do not raise exceptions). 

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


Example 1: Use checkit in code, simplest case
----------------

The basic aim of checkit is to give you quick-to-use, simple and readable assertion-like functions to check conditions. They are assert-like because what you do is indeed similar to assert expressions, since you: (i) check a condition, (ii) do nothing when it's met, but (iii) raise an exception when it is not. However, checkit differs from assertions in one significant functionality: Unlike when using `assert`, you can raise any error you want. What is perhaps more important, you are not supposed to use the assert expression in code outside of testing, but you can use checkit assert-like functions (starting off with check_).

Of course, checkit is to help you when Python does not handle a particular situation. For example, it does so when you're trying to divide a number by zero, so you need not use checkit then. But there is a plethora of various situations which you want to handle.

Here are several examples of the simplest uses of checkit:

.. code-block:: python

    def get_first_name(full_name):
        check_if(full_name is not None,
                 error=TypeError, message='Missing full name')
        check_instance(full_name, str, message='Full name must be string')
        check_if(' ' in full_name.strip(),
            error=ValueError,
            message=('No space in full name:'
                     ' impossible to split first and second name')
        
        return full_name.split(' ')[0]
    
You can then use such a function in an automated way. If something is wrong, the corresponding exception is raised. You can catch these exceptions and handle them accordingly.
    
Above, we could handle the None situation using check_instance(), but the approach we chose gives us a little more flixibility.
    
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
    
    You need to choose which of the two styles is more readable. Both are more or less of the same length, so this factor does not count here. Using the checkit approach, you do not have to overuse negative conditions (known to be more difficult to grasp), and the command says itself what you're doing. In the shortest version (with default values), we might do it like here:
    
.. code-block:: python

    def get_first_name(full_name):
        check_if(full_name is not None)
        check_instance(full_name, str)
        check_if(' ' in full_name.strip())
        
        return full_name.split(' ')[0]
    
with its non-checkit counterpart being rather less readable:

.. code-block:: python

    def get_first_name(full_name):
        if full_name is None:
            raise Exception
        elif not isinstance(full_name, str):
            raise Exception
        elif ' ' not in full_name.strip():
            raise Exception
        
        return full_name.split(' ')[0]


Example 2: Use checkit in code, handle errors
----------------

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
       
    def get_data(db_details, db_credentials):
        data = get_data_from_db(db_details, db_credentials)
        check_if(
            data,
            error=DataBaseConnectionError,
            message='Cannot communicate with the database'
            )
        return data()
    
        
    
If is_connection() returns False, an exception is raised. You can of course handle this exception, for example like here:

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
        
Example 3: Testing
--------------------
