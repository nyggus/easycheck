The :code:`easycheck` module
--------------------------

Every check decreases performance. You can implement the checks in a way that they are run only in a particular scenario. You can also implement using :code:`__debug__` (see `this article <https://towardsdatascience.com/python-assertions-or-checking-if-a-cat-is-a-dog-ce11c55d143>`_).

:code:`easycheck`, however, offers you a simpler way of _not_ running its checks. You do not have to change anything in your program to switch them off. Enough to set the :code:`"EASYCHECK_RUN"` environmental variable to :code:`"0"`, and the checks will be switched off.

This will change :code:`easycheck` functions: instead of running checks, they will do nothing. In other words, they will be empty functions. Of course, this does not mean this approach will be the same performant as removing the checks from the code. Nonetheless, you can gain quite some performance.

An obvious advantage of :code:`EASYCHECK_RUN = 0` is that you do not need to do anything else, just set this environmental variable to :code:`"0"`, like here:

.. code-block:: shell

    > EASYCHECK_RUN = 0
    > python my_script.py

The my_script.py script will be run with all :code:`easycheck` functions replaced with an empty function.

You can also switch off easycheck directly from Python:

.. code-block:: python

    >>> import easycheck
    >>> import os
    >>> os.environ["EASYCHECK_RUN"] = "0"
    >>> os.environ["EASYCHECK_RUN"]
    '0'
    >>> easycheck.check_if(1 == 1)
    >>> easycheck.check_if(1 != 1)

As you see, nothing happens even if the condition being checked is false. This is what would happen when :code:`easycheck` is on:

.. code-block:: python

    >>> os.environ["EASYCHECK_RUN"] = "1" # can be "True" (not just `True`) or anything, just not "0"
    >>> os.environ["EASYCHECK_RUN"]
    '1'
    >>> easycheck.check_if(1 == 1)
    >>> easycheck.check_if(1 != 1)
    Traceback (most recent call last):
        ...
    AssertionError

---

> **Warning**: Do remember to use this option wisely. While it will increase performance, it can also change the behavior of the Python program.

---
