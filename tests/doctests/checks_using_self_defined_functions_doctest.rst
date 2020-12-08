Complex checks using a self-defined function
--------------------------------------------

You can also define complex checks using a function that collects calls to checkit functions. That way, you can simplify the function in which you want to make the check, by using just one line instead of several (8 in the example below).

.. code-block::python

    >>> from checkit import check_if, check_instance, check_argument
    >>> def check_glm_args(glm_args):
    ...    check_instance(glm_args[0], (int, float))
    ...    check_instance(glm_args[1], str)
    ...    check_instance(glm_args[2], str)
    ...    check_if(glm_args[0] > 0 and
    ...        glm_args[0] <= 1 and
    ...        glm_args[1] in ('poisson', 'quasi-poisson') and
    ...        glm_args[2] in ('log', 'identity'),
    ...        handle_by=ValueError,
    ...        message='Incorrect argument value'
    ...    )
    >>> def run_glm(glm_args):
    ...    check_glm_args(glm_args)
    ...    # do whatever is to do
    ...    return 'glm model'
    >>> glm_args = 1, 'quasi-poisson', 'log'
    >>> run_glm(glm_args)
    'glm model'
    >>> glm_args = 1., 'quasi-poisson', 'logit'
    >>> check_glm_args(glm_args)
    Traceback (most recent call last):
        ...
    ValueError: Incorrect argument value
  
We can do it in a more comprehensive way:

.. code-block::python

    >>> from checkit import check_if, check_instance
    >>> def check_glm_args(glm_args):
    ...    check_instance(glm_args[0], (int, float))
    ...    check_instance(glm_args[1], str)
    ...    check_instance(glm_args[2], str)
    ...    check_if(glm_args[0] > 0 and glm_args[0] <= 1,
    ...        handle_by=ValueError,
    ...        message='The first argument\'s value is incorrect'
    ...    )
    ...    check_argument(
    ...        glm_args[1],
    ...        expected_choices=('poisson', 'quasi-poisson')
    ...    )
    ...    check_argument(
    ...        glm_args[2],
    ...        expected_choices=('log', 'identity')
    ...    )
    >>> glm_args = 1, 'quasi-poisson', 'log'
    >>> run_glm(glm_args)
    'glm model'

    >>> glm_args = 1., 'quasi-poisson', 'logit'
    >>> check_glm_args(glm_args)
    Traceback (most recent call last):
        ...
    checkit.ArgumentValueError: argument's value, logit, is not among valid values: ('log', 'identity').

    >>> glm_args = 1., 'quasi-poissons', 'logit'
    >>> check_glm_args(glm_args)
    Traceback (most recent call last):
        ...
    checkit.ArgumentValueError: argument's value, quasi-poissons, is not among valid values: ('poisson', 'quasi-poisson').
