Using :code:`easycheck` for assertion
--------------------------

:code:`easycheck` gives the user a set of tools to add assertion to his code. There is two main reason to do it. First one is testing (check for more in `use_in_testing_doctest`). Second one is situation when we try to catch situation that should never happen (for more check `article <https://towardsdatascience.com/python-assertions-or-checking-if-a-cat-is-a-dog-ce11c55d143>`)
Here are some examples of when you might consider adding assertions (please note that these are just examples, you may find that in your similar situation you will need to use check function or not use anything):

You are working only on integers, for example pixels when rendering images, or placing objects on board. You are sure that output will be integer, so you can assert on integers:

.. code-block:: python

    >>> pos.x = 10
    >>> assert_type(pos.x, int)

Similar situation you will have when you have output from some `len` method:

.. code-block:: python

    >>> out = len("example")
    >>> assert_type(out, int)

You created the file and worked on it - path assert (note that we are talking about a situation where you have evidence bordering on the certainty that the file exists, you should not use assert if you are not sure if you created the file correctly) e.g. you are working on a README file with example code inside it:

.. code-block:: python

    >>> file_path = "README.rst"
    >>> assert_paths(file_path)

You are working on subset of some data. So the size of the data should not be larger than the initial one, but also not smaller than 0:

.. code-block:: python

    >>> x = [1,2,3]
    >>> x1 = x[0:2]
    >>> assert_if_in_limits(len(x1), 0, len(x))

And some more examples:

    >>> x = 0
    >>> assert_if(x = 0)
    >>> assert_if_not(x > 0)
    >>> assert_if_isclose(x, 0, 0.01)   
    >>> assert_length(x, 1)   
