import warnings
import os
import pytest
from collections.abc import Generator
from operator import eq, le, lt, gt, ge, ne, is_, is_not
from checkit import (check_if, assert_if,
                     check_if_not, assert_if_not,
                     check_instance, assert_instance,
                     check_if_paths_exist, assert_paths,
                     check_length, assert_length,
                     check_all_ifs,
                     check_argument,
                     check_comparison,
                     catch_check,
                     ComparisonError,
                     ArgumentValueError,
                     LengthError,
                     OperatorError,
                     get_possible_operators,
                     _compare,
                     _parse_error_and_message_from,
                     _clean_message,
                     _raise,
                     _return_from_check_if_paths_exist,
                     _check_checkit_arguments,
                     _make_message,
                     )


def test_check_if_edge_cases():
    with pytest.raises(TypeError,
                       match="missing 1 required positional argument"):
        check_if()
    with pytest.raises(ValueError, match='The condition does not give'):
        check_if('tomato soup is good')
    with pytest.raises(ValueError, match='The condition does not give'):
        check_if('')
    with pytest.raises(ValueError, match='The condition does not give'):
        check_if(1)
    with pytest.raises(ValueError, match='The condition does not give'):
        check_if(0)
    assert check_if(True) is None
    with pytest.raises(AssertionError):
        check_if(False)
    with pytest.raises(TypeError, match='handle_by must be an exception'):
        check_if(1, 1)
    with pytest.raises(TypeError, match='message must be either None or string'):
        check_if(1, ValueError, 1)
    with pytest.raises(TypeError, match='takes from 1 to 3 positional'):
        check_if(1, 1, 1, 1)


def test_check_if_positive():
    assert check_if(2 > 1) is None
    assert check_if(2 > 1, Warning) is None
    assert check_if(0 == 0) is None
    assert check_if(0 == 0, Warning) is None
    assert check_if(None is None) is None
    assert check_if(None is None, Warning) is None


def test_check_if_negative():
    with pytest.raises(AssertionError):
        check_if(2 < 1)
    with pytest.raises(ValueError):
        check_if(2 < 1, handle_by=ValueError)
    with pytest.raises(ValueError, match='incorrect value'):
        check_if(2 < 1, handle_by=ValueError, message='incorrect value')


def test_check_if_negative_warnings():
    with warnings.catch_warnings(record=True) as w:
        check_if(2 < 1, Warning, 'This is a testing warning')
        assert 'This is a testing warning' in str(w[-1].message)

    with warnings.catch_warnings(record=True) as w:
        check_if(2 < 1, UserWarning, 'This is a testing warning')
        assert issubclass(w[-1].category, Warning)
        assert 'This is a testing warning' in str(w[-1].message)


def test_check_if_not_edge_cases():
    with pytest.raises(TypeError,
                       match="missing 1 required positional argument"):
        check_if_not()
    with pytest.raises(ValueError, match='The condition does not give'):
        check_if_not('tomato soup is good')
    with pytest.raises(ValueError, match='The condition does not give'):
        check_if_not('')
    with pytest.raises(ValueError, match='The condition does not give'):
        check_if_not(1)
    with pytest.raises(ValueError, match='The condition does not give'):
        check_if_not(0)
    assert check_if_not(False) is None
    with pytest.raises(AssertionError):
        check_if_not(True)
    with pytest.raises(TypeError, match='handle_by must be an exception'):
        check_if_not(1, 1)
    with pytest.raises(TypeError, match='message must be either None or string'):
        check_if_not(1, ValueError, 1)
    with pytest.raises(TypeError, match='takes from 1 to 3 positional'):
        check_if_not(1, 1, 1, 1)


def test_check_if_not_positive():
    assert check_if_not(2 < 1) is None
    assert check_if_not(2 < 1, Warning) is None
    assert check_if_not('a' == 'A') is None
    assert check_if_not('a' == 'A', Warning) is None


def test_check_if_not_negative():
    with pytest.raises(AssertionError):
        check_if_not(2 > 1)
    with pytest.raises(ValueError):
        check_if_not(2 > 1, handle_by=ValueError)
    with pytest.raises(ValueError, match='incorrect value'):
        check_if_not(2 > 1, handle_by=ValueError, message='incorrect value')


def test_check_if_not_negative_warnings():
    with warnings.catch_warnings(record=True) as w:
        check_if_not(2 > 1, Warning, 'This is a testing warning')
        assert 'This is a testing warning' in str(w[-1].message)

    with warnings.catch_warnings(record=True) as w:
        check_if_not(2 > 1, UserWarning, 'This is a testing warning')
        assert issubclass(w[-1].category, Warning)
        assert 'This is a testing warning' in str(w[-1].message)


def test_check_length_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        check_length()
    with pytest.raises(TypeError, match='required positional argument'):
        check_length(1)
    with pytest.raises(TypeError, match='required positional argument'):
        check_length('tomato soup is good')
    with pytest.raises(OperatorError, match='Unacceptable operator'):
        check_length(1, 1, 1)
    with pytest.raises(TypeError, match='BaseException type, not str'):
        pytest.raises('tomato soup', 'is good')


def test_check_length_positive():
    assert check_length(['string'], 1) is None
    assert check_length(['string'], 1, handle_by=Warning) is None
    assert check_length('string', 6) is None
    assert check_length('string', 6, handle_by=Warning) is None
    assert check_length([1, 2], 2) is None
    assert check_length([1, 2], 2, handle_by=Warning) is None
    assert check_length(range(0, 3), 3) is None
    assert check_length(range(0, 3), 3, handle_by=Warning) is None
    assert check_length(10, 1, assign_length_to_others=True) is None
    assert check_length(10,
                        1,
                        assign_length_to_others=True,
                        handle_by=Warning) is None


def test_check_length_negative():
    with pytest.raises(TypeError):
        check_length(len(i for i in range(3)), 3)
    with pytest.raises(TypeError):
        check_length(None)
    with pytest.raises(TypeError, match="object of type 'int' has"):
        check_length(10, 1)


def test_check_instance_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        check_instance()
    with pytest.raises(TypeError, match='required positional argument'):
        check_instance(1)
    with pytest.raises(TypeError, match='required positional argument'):
        check_instance(True)
    with pytest.raises(TypeError, match='required positional argument'):
        check_instance('tomato soup is good')
    with pytest.raises(TypeError, match='unexpected keyword'):
        check_instance(Item=2)
    with pytest.raises(TypeError, match='unexpected keyword'):
        check_instance(item=2, instance=str)


def test_check_instance_positive():
    assert check_instance(['string'], list) is None
    assert check_instance('string', str) is None
    assert check_instance((1, 2), tuple) is None
    assert check_instance(
        (1, 2), (tuple, list),
        message='Neither tuple nor list'
    ) is None
    assert check_instance((i for i in range(3)), Generator) is None
    assert check_instance(None, (int, None)) is None
    assert check_instance(20, (int, None)) is None
    assert check_instance(None, None) is None


def test_check_instance_negative():
    with pytest.raises(TypeError, match='Neither tuple nor list'):
        check_instance(
            'souvenir',
            (tuple, list),
            message='Neither tuple nor list'
        )
    with pytest.raises(TypeError):
        check_instance(20.1, (int, None))
    with pytest.raises(TypeError):
        check_instance((i for i in range(3)), tuple)
    with pytest.raises(TypeError, match='This is not tuple'):
        check_instance((i for i in range(3)),
                       tuple,
                       message='This is not tuple')
    with pytest.raises(TypeError):
        check_instance(10, None)
    with pytest.raises(TypeError):
        check_instance('string', None)
    with pytest.raises(TypeError):
        check_instance((10, 20), None)
    with pytest.raises(TypeError):
        check_instance([10, 20], None)


def test_catch_check_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        catch_check()
    with pytest.raises(TypeError, match='required positional argument'):
        catch_check(check=check_instance)
    with pytest.raises(TypeError, match='checkit function'):
        catch_check(1)
    with pytest.raises(ArgumentValueError,
                       match='acceptable valid checkit functions'):
        catch_check(sum)


def test_catch_check_if():
    my_check = catch_check(check_if, 2 == 2)
    assert my_check is None

    my_check_not = catch_check(check_if, 2 > 2)
    with pytest.raises(AssertionError):
        raise my_check_not

    my_check_not = catch_check(check_if, 2 > 2, ValueError)
    assert isinstance(my_check_not, ValueError)
    with pytest.raises(ValueError):
        raise my_check_not


def test_catch_check_if_not():
    my_check = catch_check(check_if_not, 2 > 2)
    assert my_check is None

    my_check_not = catch_check(check_if_not, 2 == 2)
    assert isinstance(my_check_not, AssertionError)
    with pytest.raises(AssertionError):
        raise my_check_not


def test_catch_check_length():
    my_check = catch_check(check_length, [2, 2], 2)
    assert my_check is None

    my_check_not = catch_check(check_length, [2, 2], 3)
    assert isinstance(my_check_not, LengthError)
    with pytest.raises(LengthError):
        raise my_check_not


def test_catch_check_instance():
    my_check = catch_check(check_instance, 25, int)
    assert my_check is None

    my_check_not = catch_check(check_instance,
                               25,
                               float,
                               ValueError,
                               'This is no float!')
    assert isinstance(my_check_not, ValueError)
    with pytest.raises(ValueError, match='This is no float!'):
        raise my_check_not

    my_check = catch_check(check_instance, 'a', int)
    assert isinstance(my_check, TypeError)
    with pytest.raises(TypeError):
        raise my_check


def test_catch_check_paths_with_return():
    existing_path = os.listdir('.')[0]
    with pytest.raises(ValueError, match='execution_mode="return"'):
        my_check_not = catch_check(check_if_paths_exist,
                                   paths=existing_path,
                                   execution_mode='return')
    with pytest.raises(ValueError, match='execution_mode="return"'):
        my_check_not = catch_check(check_if_paths_exist,
                                   existing_path,
                                   'return')


def test_catch_check_paths_one_path():
    existing_path = os.listdir('.')[0]
    my_check = catch_check(check_if_paths_exist, paths=existing_path)
    assert my_check is None

    non_existing_path = 'W:/Op/No_no'
    my_check_not = catch_check(check_if_paths_exist, paths=non_existing_path)
    assert isinstance(my_check_not, FileNotFoundError)
    with pytest.raises(FileNotFoundError):
        raise my_check_not


def test_catch_check_paths_many_paths():
    existing_paths = os.listdir('.')
    my_check = catch_check(check_if_paths_exist, paths=existing_paths)
    assert my_check is None

    non_existing_paths = ['W:/Op/No_no'] + os.listdir('.')
    my_check_not = catch_check(check_if_paths_exist, paths=non_existing_paths)
    assert isinstance(my_check_not, FileNotFoundError)
    with pytest.raises(FileNotFoundError):
        raise my_check_not


def test_compare_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        _compare()
    with pytest.raises(TypeError, match='required positional argument'):
        _compare(1)
    with pytest.raises(TypeError, match='required positional argument'):
        _compare(True)
    with pytest.raises(TypeError, match='required positional argument'):
        _compare('tomato soup is good')
    with pytest.raises(TypeError, match='required positional argument'):
        _compare(1, 1)
    with pytest.raises(TypeError, match='required positional argument'):
        _compare(1, 'tomato soup is good')
    with pytest.raises(TypeError, match='required positional argument'):
        _compare(1 > 2)
    with pytest.raises(TypeError, match='unexpected keyword'):
        _compare(item1=1, operator=gt, item_2=2)
    with pytest.raises(TypeError, match='unexpected keyword'):
        _compare(item_1=1, Operator=gt, item_2=2)
    with pytest.raises(TypeError, match='unexpected keyword'):
        _compare(item_1=1, operator=gt, item2=2)
    with pytest.raises(OperatorError, match='Incorrect operator'):
        _compare(2, 'greater', 3)


def test_compare_positive():
    assert _compare(2, eq, 2)
    assert _compare(2, lt, 3)
    assert _compare(2, le, 2)
    assert _compare(2, le, 2)
    assert _compare(2, le, 3)
    assert _compare(3, gt, 2)
    assert _compare(2, ge, 2)
    assert _compare(3, ge, 2)


def test_compare_negative():
    assert not _compare(2, eq, 2.01)
    assert not _compare(3, lt, 3)
    assert not _compare(3, lt, 2)
    assert not _compare(2.11, le, 2.100001)
    assert not _compare(2.11, le, 2.100001)
    assert not _compare(3, gt, 3)
    assert not _compare(2.11, gt, 2.12)
    assert not _compare(2.11, ge, 2.12)
    assert not _compare(2.1, ge, 2.11)


def test_check_comparison_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        check_comparison()
    with pytest.raises(TypeError, match='required positional argument'):
        check_comparison(1)
    with pytest.raises(TypeError, match='required positional argument'):
        check_comparison(True)
    with pytest.raises(TypeError, match='required positional argument'):
        check_comparison('tomato soup is good')
    with pytest.raises(TypeError, match='required positional argument'):
        check_comparison(1, 1)
    with pytest.raises(TypeError, match='required positional argument'):
        check_comparison(1, 'tomato soup is good')
    with pytest.raises(TypeError, match='required positional argument'):
        check_comparison(1 > 2)
    with pytest.raises(TypeError, match='unexpected keyword'):
        check_comparison(item1=1, operator=gt, item_2=2)
    with pytest.raises(TypeError, match='unexpected keyword'):
        check_comparison(item_1=1, Operator=gt, item_2=2)
    with pytest.raises(TypeError, match='unexpected keyword'):
        check_comparison(item_1=1, operator=gt, item2=2)


def test_check_comparison_positive():
    assert check_comparison(2, eq, 2) is None
    assert check_comparison(2, le, 2) is None
    assert check_comparison(2, ge, 2) is None
    assert check_comparison(3, gt, 2) is None
    assert check_comparison(3, ge, 2) is None
    assert check_comparison('One text', lt, 'one text') is None
    assert check_comparison('One text', lt, 'another text') is None


def test_check_comparison_negative():
    with pytest.raises(ValueError):
        check_comparison(2, lt, 2)
    with pytest.raises(ValueError):
        check_comparison(2, gt, 2)
    with pytest.raises(ValueError):
        check_comparison(3, eq, 2)
    with pytest.raises(ValueError):
        check_comparison(3, lt, 2)
    with pytest.raises(ValueError):
        check_comparison(3, le, 2)
    with pytest.raises(ValueError):
        check_comparison('one text', lt, 'another text')

    with pytest.raises(ComparisonError):
        check_comparison('one text', lt, 'another text',
                         handle_by=ComparisonError)
    with pytest.raises(AssertionError):
        check_comparison('one text', lt, 'another text',
                         handle_by=AssertionError)


def test_clean_message_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        _clean_message()
    with pytest.raises(TypeError, match='unexpected keyword'):
        _clean_message(Message='tomato soup is good')
    with pytest.raises(TypeError, match='string or tuple/list'):
        _clean_message(1)
    with pytest.raises(TypeError, match='string or tuple/list'):
        _clean_message((1, 1))
    with pytest.raises(TypeError, match='string or tuple/list'):
        _clean_message(('tomato soup is good', 1))
    with pytest.raises(TypeError, match='string or tuple/list'):
        _clean_message([1, 1])
    with pytest.raises(TypeError, match='string or tuple/list'):
        _clean_message(['tomato soup is good', 1])
    with pytest.raises(TypeError, match='string or tuple/list'):
        _clean_message({'1': 'tomato soup', '2': 'is good'})
    with pytest.raises(TypeError, match='string or tuple/list'):
        _clean_message((1, 1))


def test_clean_message():
    assert _clean_message('"This is wrong")') == 'This is wrong'
    assert _clean_message(
        '"Incorrect argument (change it).")'
    ) == 'Incorrect argument (change it).'
    assert _clean_message(r'D://') == r'D:/'


def test_parse_error_and_message_from_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        _parse_error_and_message_from()
    with pytest.raises(TypeError, match='unexpected keyword'):
        _parse_error_and_message_from(message='tomato soup is good')
    with pytest.raises(AttributeError, match="no attribute 'split'"):
        _parse_error_and_message_from(True)
    with pytest.raises(AttributeError, match="no attribute 'split'"):
        _parse_error_and_message_from(25)
    with pytest.raises(AttributeError, match="no attribute 'split'"):
        _parse_error_and_message_from([1, 1])
    with pytest.raises(AttributeError, match="no attribute 'split'"):
        _parse_error_and_message_from((1, 1))
    with pytest.raises(AttributeError, match="no attribute 'split'"):
        _parse_error_and_message_from(['TypeError'])


def test_parse_error_and_message_from():
    error_and_message = ('TypeError("Incorrect argument")')
    error, message = _parse_error_and_message_from(error_and_message)
    assert error == 'TypeError'
    assert message == 'Incorrect argument'

    error, message = _parse_error_and_message_from('ValueError')
    assert error == 'ValueError'
    assert message is None

    this_item_is_None = None
    assert _parse_error_and_message_from(this_item_is_None) is None


def test_check_all_ifs_edge_cases():
    with pytest.raises(ValueError, match='at least one condition'):
        check_all_ifs()
    with pytest.raises(TypeError, match='Provide all function calls as'):
        check_all_ifs(1)
    with pytest.raises(TypeError, match='Provide all function calls as'):
        check_all_ifs(True)
    with pytest.raises(TypeError, match='Provide all function calls as'):
        check_all_ifs(1, 1)
    with pytest.raises(TypeError, match='Provide all function calls as'):
        check_all_ifs(1 > 1, 2 > 1)
    with pytest.raises(TypeError, match='Provide all function calls as'):
        check_all_ifs((20 > 10))
    with pytest.raises(TypeError, match='Provide all function calls as'):
        check_all_ifs(check_if(20 > 10)),
    with pytest.raises(TypeError, match='Provide all function calls as'):
        check_all_ifs((check_if, 20 > 10), (check_if(20 > 10)))


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
    assert any(type(value) == AssertionError
               for key, value in multiple_check_2.items())

    multiple_check_3 = check_all_ifs(
        (check_if, 2 > 1),
        (check_if_not, 'a' == 'a', ValueError)
    )
    assert any(type(value) == ValueError
               for key, value in multiple_check_3.items())


def test_check_if_paths_exist_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        check_if_paths_exist()
    with pytest.raises(TypeError, match='unexpected keyword'):
        check_if_paths_exist(path='tomato soup is good')
    with pytest.raises(TypeError, match='Argument paths must be string'):
        check_if_paths_exist(20)
    with pytest.raises(TypeError, match='Argument paths must be string'):
        check_if_paths_exist({})
    with pytest.raises(ValueError):
        check_if_paths_exist(os.listdir('.')[0], execution_mode='buuu')


def test_check_if_paths_exist_positive():
    single_path_to_check = os.listdir('.')[0]
    list_of_paths_to_check = os.listdir('.')
    assert check_if_paths_exist(single_path_to_check) is None
    assert check_if_paths_exist(single_path_to_check,
                                execution_mode='return')

    assert check_if_paths_exist(list_of_paths_to_check) is None
    assert check_if_paths_exist(list_of_paths_to_check,
                                execution_mode='return')


def test_check_if_paths_exist_negative():
    non_existing_path = 'Z:/Op/Oop/'
    with pytest.raises(ValueError):
        check_if_paths_exist(non_existing_path, execution_mode='buuu')
    with pytest.raises(FileNotFoundError):
        check_if_paths_exist(non_existing_path)
    with pytest.raises(FileNotFoundError):
        check_if_paths_exist([non_existing_path] + os.listdir('.'))
    with pytest.raises(IOError):
        check_if_paths_exist(non_existing_path, handle_by=IOError)

    failed_check = check_if_paths_exist(non_existing_path,
                                        execution_mode='return')
    assert failed_check[1] == non_existing_path
    with pytest.raises(FileNotFoundError):
        raise failed_check[0]

    failed_check = check_if_paths_exist([non_existing_path] + os.listdir('.'),
                                        execution_mode='return')
    with pytest.raises(FileNotFoundError):
        raise failed_check[0]
    assert failed_check[1] == [non_existing_path]


def test_raise_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        _raise()
    with pytest.raises(TypeError, match='unexpected keyword'):
        _raise(handle_by=TypeError)
    with pytest.raises(TypeError, match='unexpected keyword'):
        _raise(handle_by=TypeError, MEssage='This was an error')
    with pytest.raises(
            TypeError,
            match='The error argument must be an exception or warning'):
        _raise(20)
    with pytest.raises(
            TypeError,
            match='The error argument must be an exception or warning'):
        _raise('TypeError')
    with pytest.raises(
            TypeError,
            match='The error argument must be an exception or warning'):
        _raise(('TypeError'))
    with pytest.raises(
            TypeError,
            match='The error argument must be an exception or warning'):
        _raise([TypeError])
    with pytest.raises(TypeError, match='message must be string'):
        _raise(error=TypeError, message=20)
    with pytest.raises(TypeError, match='message must be string'):
        _raise(TypeError, ('This was an error', ''))


def test_raise():
    with pytest.raises(ValueError):
        _raise(ValueError)
    with pytest.raises(TypeError):
        _raise(TypeError)
    with pytest.raises(TypeError, match='Incorrect type'):
        _raise(TypeError, 'Incorrect type')


def test_check_argument_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        check_argument()
    with pytest.raises(TypeError, match='required positional argument'):
        check_argument(Argument='x')

    msg = 'check_argument() requires at least one condition to be checked'
    with pytest.raises(ValueError) as msg_error:
        check_argument(10)
    assert str(msg_error.value) == msg
    with pytest.raises(ValueError) as msg_error:
        check_argument(10, message='Error!')
    assert str(msg_error.value) == msg
    with pytest.raises(ValueError) as msg_error:
        check_argument('x', 10, handle_by=TypeError)
    assert str(msg_error.value) == msg

    x = 5


def test_check_argument_instance():
    def foo(x):
        check_argument(x, 'x', expected_instance=str)
        pass
    assert foo('one') is None
    assert foo(('one')) is None
    with pytest.raises(ArgumentValueError):
        foo(4)
    with pytest.raises(ArgumentValueError):
        foo(('one', 'two'))

    assert check_argument(50, 'my_arg', expected_instance=int) is None
    assert check_argument(50, expected_instance=int) is None
    assert check_argument('my_arg', 'one', expected_instance=str) is None
    assert check_argument('my_arg', expected_instance=str) is None

    with pytest.raises(ArgumentValueError, match='my_arg'):
        check_argument(50, 'my_arg', expected_instance=str)
    with pytest.raises(ArgumentValueError, match='my_arg'):
        check_argument('one', 'my_arg', expected_instance=int)
    with pytest.raises(ArgumentValueError, match='argument'):
        check_argument(50, expected_instance=str)
    with pytest.raises(ArgumentValueError, match='argument'):
        check_argument('one', expected_instance=int)


def test_check_argument_choices():
    assert check_argument(5, 'my_arg', expected_choices=range(10),) is None
    assert check_argument(5, expected_choices=range(10)) is None

    def foo(x):
        check_argument(x, expected_choices=('first choice', 'second choice'))
        pass
    assert foo('first choice') is None
    assert foo('second choice') is None
    with pytest.raises(ArgumentValueError, match='not among valid values'):
        foo('no choice')

    def foo(x):
        check_argument(x, 'x', expected_choices=('one', 'two'))
        pass
    assert foo('one') is None
    with pytest.raises(ArgumentValueError,
                       match="x's value, three, is not among valid values"):
        foo('three')

    def foo(x):
        check_argument(x, expected_choices=('one', 'two'))
        pass
    assert foo('one') is None
    with pytest.raises(
            ArgumentValueError,
            match="argument's value, three, is not among valid values"):
        foo('three')


def test_check_argument_length():
    assert check_argument(5, 'my_arg',
                          expected_length=1,
                          assign_length_to_others=True) is None
    assert check_argument(5,
                          expected_length=1,
                          assign_length_to_others=True) is None

    def foo(x):
        check_argument(x, 'x',
                       expected_length=3,
                       assign_length_to_others=True)
        pass
    assert foo([1, 2, 3]) is None
    with pytest.raises(ArgumentValueError):
        foo(1)

    def foo(x):
        check_argument(x, expected_length=3, assign_length_to_others=True)
        pass
    assert foo([1, 2, 3]) is None
    with pytest.raises(ArgumentValueError):
        foo(1)

    def foo(big_x):
        check_argument(big_x, 'big_x',
                       expected_length=3,
                       assign_length_to_others=True)
        pass
    assert foo([1, 2, 3]) is None
    with pytest.raises(ArgumentValueError, match='big_x'):
        foo(1)

    def foo(big_x):
        check_argument(big_x, expected_length=3, assign_length_to_others=True)
        pass
    assert foo([1, 2, 3]) is None
    with pytest.raises(ArgumentValueError, match='argument'):
        foo(1)


def test_check_argument_mix():
    def foo(x):
        check_argument(x, 'x', expected_instance=int, condition=x % 2 == 0)
        pass
    with pytest.raises(TypeError):
        x = 'one'
        check_argument(argument=x,
                       argument_name='x',
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
    assert check_argument(
        argument_name='glm_args',
        argument=glm_args,
        expected_instance=tuple
    ) is None

    glm_args = 1., 'quasi-poisson', 'logit'


def test_return_from_check_if_paths_exist_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        _return_from_check_if_paths_exist()
    with pytest.raises(TypeError, match='required positional argument'):
        _return_from_check_if_paths_exist(
            error=FileNotFoundError)
    with pytest.raises(TypeError, match='required positional argument'):
        _return_from_check_if_paths_exist(
            error=FileNotFoundError,
            message=None)
    with pytest.raises(TypeError, match='unexpected keyword'):
        _return_from_check_if_paths_exist(
            Error=FileNotFoundError,
            message=None,
            paths=[])
    with pytest.raises(TypeError, match='unexpected keyword'):
        _return_from_check_if_paths_exist(
            error=FileNotFoundError,
            Message=None,
            paths=[])
    with pytest.raises(TypeError, match='unexpected keyword'):
        _return_from_check_if_paths_exist(
            error=FileNotFoundError,
            message=None,
            Paths=[])

    with pytest.raises(TypeError, match='must be an exception'):
        _return_from_check_if_paths_exist(20, None, [])
    with pytest.raises(TypeError, match='must be an exception'):
        _return_from_check_if_paths_exist('TypeError', None, [])


def test_return_from_check_if_paths_exist():
    my_return = _return_from_check_if_paths_exist(
        error=FileNotFoundError,
        message=None,
        paths=[])
    assert isinstance(my_return[0], Exception)
    assert my_return[1] == []

    my_return_2 = _return_from_check_if_paths_exist(
        error=FileNotFoundError,
        message='No such file',
        paths='D:/this_dir/this_path.csv')
    assert isinstance(my_return_2[0], Exception)
    assert my_return_2[1] == 'D:/this_dir/this_path.csv'


def test_check_checkit_arguments_edge_cases():
    with pytest.raises(ValueError, match='Provide at least one argument'):
        _check_checkit_arguments()

    with pytest.raises(TypeError, match='unexpected keyword'):
        _check_checkit_arguments(Handle_by=1)
    with pytest.raises(TypeError, match='unexpected keyword'):
        _check_checkit_arguments(Message=1)
    with pytest.raises(TypeError, match='unexpected keyword'):
        _check_checkit_arguments(Condition=1)
    with pytest.raises(TypeError, match='unexpected keyword'):
        _check_checkit_arguments(Operator=1)
    with pytest.raises(TypeError, match='unexpected keyword'):
        _check_checkit_arguments(Assign_length_to_others=1)
    with pytest.raises(TypeError, match='unexpected keyword'):
        _check_checkit_arguments(Execution_mode=1)
    with pytest.raises(TypeError, match='unexpected keyword'):
        _check_checkit_arguments(Expected_instance=1)
    with pytest.raises(TypeError, match='unexpected keyword'):
        _check_checkit_arguments(Expected_length=1)
    with pytest.raises(TypeError, match='unexpected keyword'):
        _check_checkit_arguments(handle_by=ValueError, Message=1)

    with pytest.raises(TypeError,
                       match='handle_by must be an exception') as msg_error:
        _check_checkit_arguments(handle_by=20)

    with pytest.raises(TypeError,
                       match='handle_by must be an exception') as msg_error:
        class NonExceptionClass:
            pass
        _check_checkit_arguments(handle_by=NonExceptionClass)


def test_check_checkit_arguments():

    assert _check_checkit_arguments(handle_by=LengthError) is None
    with pytest.raises(NameError):
        _check_checkit_arguments(handle_by=NonExistingError)
    with pytest.raises(NameError):
        _check_checkit_arguments(handle_by=NonExistingError())
    with pytest.raises(TypeError):
        _check_checkit_arguments(handle_by='NonExistingError')

    with pytest.raises(TypeError, match='must be an exception'):
        _check_checkit_arguments(handle_by=sum)

    with pytest.raises(TypeError):
        _check_checkit_arguments(handle_by=LengthError, message=False)
    assert _check_checkit_arguments(handle_by=LengthError,
                                    message='This is error') is None
    with pytest.raises(TypeError):
        _check_checkit_arguments(handle_by=LengthError, message=25)

    assert _check_checkit_arguments(handle_by=ValueError,
                                    condition='a' == 'a') is None
    assert _check_checkit_arguments(condition='a' == 'a') is None
    assert _check_checkit_arguments(handle_by=ValueError, condition=2 > 1) is None
    assert _check_checkit_arguments(handle_by=ValueError, condition=2 < 1) is None
    assert _check_checkit_arguments(handle_by=ValueError,
                                    condition=2 == '2') is None
    assert _check_checkit_arguments(condition=2 == '2') is None
    with pytest.raises(ValueError):
        _check_checkit_arguments(handle_by=ValueError,
                                 condition='not a comparison')
    with pytest.raises(ValueError):
        _check_checkit_arguments(condition='not a comparison')

    for this_operator in get_possible_operators():
        assert _check_checkit_arguments(operator=this_operator) is None
        with pytest.raises(OperatorError):
            _check_checkit_arguments(operator=this_operator.__name__)

    assert _check_checkit_arguments(assign_length_to_others=True) is None
    assert _check_checkit_arguments(assign_length_to_others=False) is None
    for this_assignment in ('nothing', 22, [1]):
        with pytest.raises(TypeError):
            _check_checkit_arguments(assign_length_to_others=this_assignment)

    assert _check_checkit_arguments(execution_mode='return') is None
    assert _check_checkit_arguments(execution_mode='raise') is None
    for this_mode in ('nothing', 22, [1]):
        with pytest.raises(ValueError):
            _check_checkit_arguments(execution_mode=this_mode)

    for this_length in (0, 3, 5, 7):
        assert _check_checkit_arguments(expected_length=this_length) is None
        assert _check_checkit_arguments(
            expected_length=float(this_length)
        ) is None
    assert _check_checkit_arguments(expected_length=(5)) is None
    for this_length in ('0', [3], LengthError):
        with pytest.raises(TypeError):
            _check_checkit_arguments(expected_length=this_length)

    for this_instance in (str, int, float, bool, tuple, list, Generator):
        assert _check_checkit_arguments(expected_instance=this_instance) is None
    for this_instance in ('str', 25):
        with pytest.raises(TypeError):
            _check_checkit_arguments(expected_instance=this_instance)
    assert _check_checkit_arguments(expected_instance=(str,
                                                       tuple,
                                                       list)) is None
    with pytest.raises(TypeError):
        _check_checkit_arguments(expected_instance=(str, tuple, list, 26))

    assert _check_checkit_arguments(
        expected_instance=(str, tuple, list),
        condition=2 < 2,
        expected_length=3,
        execution_mode='raise',
        assign_length_to_others=True
    ) is None

    with pytest.raises(TypeError):
        _check_checkit_arguments(
            expected_instance=(str, tuple, list),
            condition=2 < 2,
            expected_length=3,
            execution_mode='raise',
            assign_length_to_others='yes'
        )


def test_make_message_edge_cases():
    with pytest.raises(TypeError, match="required positional argument"):
        _make_message()
    with pytest.raises(TypeError, match="required positional argument"):
        _make_message(None)
    with pytest.raises(TypeError, match="required positional argument"):
        _make_message('Provided')
    with pytest.raises(TypeError, match='unexpected keyword'):
        _make_message(message='Provided')
    with pytest.raises(TypeError, match='unexpected keyword'):
        _make_message(message_provided='Provided',
                      Message_otherwise='Otherwise')


def test_make_message():
    assert _make_message(None, 'Otherwise') == 'Otherwise'
    assert _make_message('Provided', 'Otherwise') == 'Provided'
    assert _make_message('Provided', 'Otherwise') == 'Provided'


def test_assert_functions():
    assert assert_if(10 > 5) == check_if(10 > 5)
    with pytest.raises(AssertionError):
        assert_if(10 < 5) and check_if(10 < 5) is None

    assert assert_if_not(10 < 5) == check_if_not(10 < 5)
    with pytest.raises(AssertionError):
        assert_if_not(10 > 5) and check_if_not(10 > 5) is None

    assert assert_instance((10, 10), tuple) == check_instance((10, 10), tuple)
    with pytest.raises(TypeError):
        assert_instance(10, tuple) and check_instance(10, tuple) is None

    assert assert_length('str', 3) == check_length('str', 3)
    assert (
        assert_length(5, 1, assign_length_to_others=True) ==
        check_length(5, 1, assign_length_to_others=True))
    with pytest.raises(TypeError):
        assert_length(5, 3) and check_length(5, 3) is None
    with pytest.raises(LengthError):
        (assert_length(5, 3, assign_length_to_others=True)
         and check_length(5, 3, assign_length_to_others=True) is None)

    existing_file = os.listdir('.')[0]
    assert (check_if_paths_exist(existing_file, execution_mode='return') ==
            assert_paths(existing_file, execution_mode='return'))
    assert (check_if_paths_exist('Q:/E/', execution_mode='return')[1] ==
            assert_paths('Q:/E/', execution_mode='return')[1])
    with pytest.raises(FileNotFoundError):
        assert_paths('Q:/E/') and check_if_paths_exist('Q:/E/') is None
