import os
import pytest
import sys
import checkit

from checkit.comparisons import (equal,
                                 less_than, lt,
                                 less_than_or_equal, lte,
                                 greater_than, gt,
                                 greater_than_or_equal, gte,
                                 get_possible_operators,
                                 )

from checkit.checks import (check_if,
                            check_if_not,
                            check_instance,
                            check_if_paths_exist,
                            check_length,
                            check_all_ifs,
                            check_argument,
                            check_comparison,
                            ComparisonError,
                            ArgumentValueError,
                            LengthError,
                            IncorrectOperatorError,
                            _compare,
                            _parse_error_and_message_from,
                            _clean_message,
                            _raise,
                            )

from collections.abc import Generator


def test_check_if():
    assert check_if(2 > 1) is None
    assert check_if(0 == 0) is None
    assert check_if(None is None) is None
    with pytest.raises(AssertionError):
        check_if(2 < 1)
    with pytest.raises(ValueError):
        check_if(2 < 1, error=ValueError)
    with pytest.raises(ValueError):
        check_if(2 < 1, error=ValueError)
    with pytest.raises(TypeError):
        check_if('a' > 2)


def test_check_if_not():
    assert check_if_not(2 < 1) is None
    with pytest.raises(AssertionError):
        check_if_not(2 > 1)
    with pytest.raises(ValueError):
        check_if_not(2 > 1, error=ValueError)
    with pytest.raises(ValueError):
        check_if_not(2 > 1, error=ValueError)
    with pytest.raises(TypeError):
        check_if_not('a' > 2)


def test_check_length():
    assert check_length(['string'], 1) is None
    assert check_length('string', 6) is None
    assert check_length([1, 2], 2) is None
    assert check_length(range(0, 3), 3) is None
    with pytest.raises(TypeError):
        check_length(len(i for i in range(3)), 3)
    with pytest.raises(TypeError):
        check_length(None)
    with pytest.raises(TypeError):
        check_length(10)
    assert check_length(10, 1, assign_length_to_numbers=True) is None


def test_check_instance():
    assert check_instance(['string'], list) is None
    assert check_instance('string', str) is None
    assert check_instance((1, 2), tuple) is None
    assert check_instance(
        (1, 2), (tuple, list),
        message='Neither tuple nor list'
    ) is None
    assert check_instance((i for i in range(3)), Generator) is None
    with pytest.raises(TypeError):
        check_instance(
            'souvenir',
            (tuple, list),
            message='Neither tuple nor list'
        )
    with pytest.raises(TypeError):
        check_instance((i for i in range(3)), tuple)
    with pytest.raises(TypeError):
        check_instance((i for i in range(3)), tuple, message='This is not tuple.')


def test_compare():
    assert _compare(2, equal, 2)
    assert not _compare(2, equal, 2.01)
    assert _compare(2, lt, 3)
    assert _compare(2, less_than, 3)
    assert not _compare(3, less_than, 3)
    assert not _compare(3, lt, 2)
    assert _compare(2, lte, 2)
    assert _compare(2, less_than_or_equal, 2)
    assert _compare(2, lte, 3)
    assert _compare(2, less_than_or_equal, 3)
    assert not _compare(2.11, lte, 2.100001)
    assert not _compare(2.11, less_than_or_equal, 2.100001)
    assert _compare(3, gt, 2)
    assert _compare(3, greater_than, 2)
    assert not _compare(3, gt, 3)
    assert not _compare(3, greater_than, 3)
    assert not _compare(2.11, gt, 2.12)
    assert not _compare(2.11, greater_than, 2.12)
    assert _compare(2, gte, 2)
    assert _compare(2, greater_than_or_equal, 2)
    assert _compare(3, gte, 2)
    assert _compare(3, greater_than_or_equal, 2)
    assert not _compare(2.1, gte, 2.11)
    assert not _compare(2.1, greater_than_or_equal, 2.11)


def test_check_comparison():
    assert check_comparison(2, equal, 2) is None
    with pytest.raises(ValueError):
        check_comparison(2, less_than, 2)
    with pytest.raises(ValueError):
        check_comparison(2, lt, 2)
    assert check_comparison(2, less_than_or_equal, 2) is None
    assert check_comparison(2, lte, 2) is None
    with pytest.raises(ValueError):
        check_comparison(2, greater_than, 2)
    with pytest.raises(ValueError):
        check_comparison(2, gt, 2)
    assert check_comparison(2, greater_than_or_equal, 2) is None
    assert check_comparison(2, gte, 2) is None

    with pytest.raises(ValueError):
        assert check_comparison(3, equal, 2)
    with pytest.raises(ValueError):
        check_comparison(3, less_than, 2)
    with pytest.raises(ValueError):
        check_comparison(3, lt, 2)
    with pytest.raises(ValueError):
        check_comparison(3, less_than_or_equal, 2)
    with pytest.raises(ValueError):
        check_comparison(3, lte, 2)
    assert check_comparison(3, greater_than, 2) is None
    assert check_comparison(3, gt, 2) is None
    assert check_comparison(3, greater_than_or_equal, 2) is None
    assert check_comparison(3, gte, 2) is None

    assert check_comparison('One text', lt, 'one text') is None
    assert check_comparison('One text', less_than, 'another text') is None
    with pytest.raises(ValueError):
        check_comparison('one text', less_than, 'another text')
    with pytest.raises(ComparisonError):
        check_comparison('one text', less_than, 'another text',
                         error=ComparisonError)

    with pytest.raises(AssertionError):
        check_comparison('one text', less_than, 'another text',
                         error=AssertionError)


def test_clean_message():
    assert _clean_message('"This is wrong")') == 'This is wrong'
    assert _clean_message(
        '"Incorrect argument (change it).")'
    ) == 'Incorrect argument (change it).'


def test_parse_error_and_message_from():
    error_and_message = (
        'TypeError("Incorrect argument")'
    )
    error, message = _parse_error_and_message_from(error_and_message)
    assert error == 'TypeError'
    assert message == 'Incorrect argument'

    error, message = _parse_error_and_message_from('ValueError')
    assert error == 'ValueError'
    assert message is None


def test_check_all_ifs():
    multiple_check_1 = check_all_ifs(
        (check_if, 2 > 1),
        (check_if, 'a' == 'a')
    )
    assert all(value for key, value in multiple_check_1.items())

    multiple_check_2 = check_all_ifs(
        (check_if, 2 > 1),
        (check_if_not, 'a' == 'a')
    )
    assert any(type(value) == AssertionError for key, value in multiple_check_2.items())

    multiple_check_3 = check_all_ifs(
        (check_if, 2 > 1),
        (check_if_not, 'a' == 'a', ValueError)
    )
    assert any(type(value) == ValueError for key, value in multiple_check_3.items())


def test_check_if_paths_exist():
    with pytest.raises(ValueError):
        check_if_paths_exist('Q:/Op/Oop/', _type='buuu')
    with pytest.raises(FileNotFoundError):
        check_if_paths_exist('Z:/Op/Oop/')
    with pytest.raises(IOError):
        check_if_paths_exist('Z:/Op/Oop/', error=IOError)
    with pytest.raises(FileNotFoundError):
        check_if_paths_exist(['Q:/Op/Oop/'] + os.listdir('.'))
    assert check_if_paths_exist(os.listdir('.')) is None
    assert check_if_paths_exist(os.listdir('.'), _type='return')


def test_raise():
    with pytest.raises(ValueError):
        _raise(ValueError)
    with pytest.raises(TypeError):
        _raise(TypeError)
    with pytest.raises(TypeError, match='Incorrect type'):
        _raise(TypeError, 'Incorrect type')


def test_check_argument_instance():
    def foo(x):
        check_argument('x', x, expected_instance=str)
        pass
    assert foo('one') is None
    assert foo(('one')) is None
    with pytest.raises(ArgumentValueError):
        foo(4)
        foo(('one', 'two'))

    assert check_argument('my_arg', 50, expected_instance=int) is None
    with pytest.raises(ArgumentValueError):
        check_argument('my_arg', 50, expected_instance=str)
        check_argument('my_arg', 'one', expected_instance=int)
    assert check_argument('my_arg', 'one', expected_instance=str) is None


def test_check_argument_choices():
    assert check_argument('my_arg',
                          5,
                          expected_choices=range(10),
                          ) is None

    def foo(x):
        check_argument('x', x, expected_choices=('first choice', 'second choice'))
        pass
    assert foo('first choice') is None
    assert foo('second choice') is None
    with pytest.raises(ArgumentValueError, match='not among valid values'):
        foo('no choice')

    def foo(x):
        check_argument('x', x, expected_choices=('one', 'two'))
        pass
    assert foo('one') is None
    with pytest.raises(ArgumentValueError, match="x's value, three, is not among valid values"):
        foo('three')


def test_check_argument_length():
    assert check_argument('my_arg',
                          5,
                          expected_length=1,
                          assign_length_to_numbers=True) is None

    def foo(x):
        check_argument('x', x, expected_length=3, assign_length_to_numbers=True)
        pass
    assert foo([1, 2, 3]) is None
    with pytest.raises(ArgumentValueError):
        foo(1)

    def foo(x):
        check_argument('x', x, expected_length=3, assign_length_to_numbers=True)
        pass
    assert foo([1, 2, 3]) is None
    with pytest.raises(ArgumentValueError):
        foo(1)


def test_check_argument_condition():
    x = 5
    assert check_argument('my_argument',
                          x,
                          expected_condition=x in range(0, 10)
                          ) is None

    def foo(x):
        check_argument('x', x, expected_condition=x % 2 == 0)
        pass
    with pytest.raises(ArgumentValueError):
        foo(3)
    assert foo(2) is None


def test_check_argument_mix():
    def foo(x):
        check_argument('x',
                       x,
                       expected_instance=int,
                       condition=x % 2 == 0)
        pass
    with pytest.raises(TypeError):
        x = 'one'
        check_argument(argument_name='x',
                       argument=x,
                       expected_instance=int,
                       condition=x % 2 == 0)
    with pytest.raises(TypeError):
        foo('one')

        def check_glm_args(glm_args):
            return (
                isinstance(glm_args[0], (int, float)) and
                glm_args[0] > 0 and
                glm_args[0] <= 1 and
                isinstance(glm_args[1], str) and
                isinstance(glm_args[2], str) and
                glm_args[1] in ('poisson', 'quasi-poisson') and
                glm_args[2] in ('log', 'identity')
             )

        glm_args = 1, 'quasi-poisson', 'log'
        check_argument(
            argument_name='glm_args',
            argument=glm_args,
            expected_instance=tuple,
            expected_condition=check_glm_args(glm_args))

        glm_args = 1., 'quasi-poisson', 'logit'
        check_argument(
            argument_name='glm_args',
            argument=glm_args,
            expected_instance=tuple,
            expected_condition=check_glm_args(glm_args))
