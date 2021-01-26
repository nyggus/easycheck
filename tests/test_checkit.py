import warnings
import os
import pytest
from collections.abc import Generator
from operator import eq, le, lt, gt, ge, ne, is_, is_not
from checkit.checkit import (check_if, assert_if,
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
                             _raise,
                             _check_checkit_arguments,
                             _make_message,
                             )


def test_check_if_edge_cases():
    with pytest.raises(TypeError, match="required positional argument"):
        check_if()
    with pytest.raises(ValueError, match='The condition does not return'):
        check_if('tomato soup is good')
    with pytest.raises(ValueError, match='The condition does not return'):
        check_if('')
    with pytest.raises(ValueError, match='The condition does not return'):
        check_if(1)
    with pytest.raises(ValueError, match='The condition does not return'):
        check_if(0)
    assert check_if(True) is None
    with pytest.raises(AssertionError):
        check_if(False)
    with pytest.raises(TypeError, match='handle_with must be an exception'):
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
        check_if(2 < 1, handle_with=ValueError)
    with pytest.raises(ValueError, match='incorrect value'):
        check_if(2 < 1, handle_with=ValueError, message='incorrect value')


def test_check_if_negative_warnings():
    with warnings.catch_warnings(record=True) as w:
        check_if(2 < 1, Warning, 'This is a testing warning')
        assert 'This is a testing warning' in str(w[-1].message)

    with warnings.catch_warnings(record=True) as w:
        check_if(2 < 1, UserWarning, 'This is a testing warning')
        assert issubclass(w[-1].category, Warning)
        assert 'This is a testing warning' in str(w[-1].message)


def test_check_if_not_edge_cases():
    with pytest.raises(TypeError, match="required positional argument"):
        check_if_not()
    with pytest.raises(ValueError, match='The condition does not return'):
        check_if_not('tomato soup is good')
    with pytest.raises(ValueError, match='The condition does not return'):
        check_if_not('')
    with pytest.raises(ValueError, match='The condition does not return'):
        check_if_not(1)
    with pytest.raises(ValueError, match='The condition does not return'):
        check_if_not(0)
    assert check_if_not(False) is None
    with pytest.raises(AssertionError):
        check_if_not(True)
    with pytest.raises(TypeError, match='handle_with must be an exception'):
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
        check_if_not(2 > 1, handle_with=ValueError)
    with pytest.raises(ValueError, match='incorrect value'):
        check_if_not(2 > 1, handle_with=ValueError, message='incorrect value')


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
        check_length('tomato soup is good')
    with pytest.raises(OperatorError, match='Incorrect operator'):
        check_length(1, 1, operator=1)
    with pytest.raises(TypeError, match='BaseException type, not str'):
        pytest.raises('tomato soup', 'is good')


def test_check_length_positive():
    assert check_length(['string'], 1) is None
    assert check_length(['string'], 1, handle_with=Warning) is None
    assert check_length('string', 6) is None
    assert check_length('string', 6, handle_with=Warning) is None
    assert check_length([1, 2], 2) is None
    assert check_length([1, 2], 2, handle_with=Warning) is None
    assert check_length(range(0, 3), 3) is None
    assert check_length(range(0, 3), 3, handle_with=Warning) is None
    assert check_length(10, 1, assign_length_to_others=True) is None
    assert check_length(10,
                        1,
                        assign_length_to_others=True,
                        handle_with=Warning) is None


def test_check_length_negative():
    with pytest.raises(TypeError):
        check_length(len(i for i in range(3)), 3)
    with pytest.raises(TypeError):
        check_length(None)
    with pytest.raises(TypeError, match="object of type 'int' has"):
        check_length(10, 1)


def test_check_length_negative_warnings():
    with warnings.catch_warnings(record=True) as w:
        check_length([1, 2],
                     expected_length=1,
                     handle_with=Warning,
                     message='This is a testing warning')
        assert 'This is a testing warning' in str(w[-1].message)


def test_check_instance_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        check_instance('tomato soup is good')


def test_check_instance_positive():
    assert check_instance(['string'], list) is None
    assert check_instance(['string'], list, handle_with=Warning) is None
    assert check_instance('string', str) is None
    assert check_instance('string', str, handle_with=Warning) is None
    assert check_instance((1, 2), tuple) is None
    assert check_instance((1, 2), tuple, handle_with=Warning) is None
    assert check_instance((1, 2), [tuple, list]) is None
    assert check_instance((1, 2), [tuple, list], handle_with=Warning) is None
    assert check_instance((1, 2), [list, tuple]) is None
    assert check_instance((1, 2), {tuple, list}, handle_with=Warning) is None
    assert check_instance(
        (1, 2), (tuple, list),
        message='Neither tuple nor list'
    ) is None
    assert check_instance(
        (1, 2), (tuple, list),
        message='Neither tuple nor list',
        handle_with=Warning
    ) is None
    assert check_instance((i for i in range(3)), Generator) is None
    assert check_instance((i for i in range(3)),
                          Generator,
                          handle_with=Warning) is None
    assert check_instance(None, (int, None)) is None
    assert check_instance(None, (int, None), handle_with=Warning) is None
    assert check_instance(20, (int, None)) is None
    assert check_instance(20, (int, None), handle_with=Warning) is None
    assert check_instance(None, None) is None
    assert check_instance(None, None, handle_with=Warning) is None


def test_check_instance_negative():
    with pytest.raises(TypeError, match='Neither tuple nor list'):
        check_instance('souvenir',
                       (tuple, list),
                       message='Neither tuple nor list')
    with pytest.raises(TypeError):
        check_instance('souvenir', [tuple, list])
    with pytest.raises(TypeError):
        check_instance('souvenir', {tuple, list})
    with pytest.raises(TypeError):
        check_instance(True, (str, complex))
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


def test_check_instance_negative_warnings():
    with warnings.catch_warnings(record=True) as w:
        check_instance(
            'souvenir',
            (tuple, list),
            handle_with=Warning,
            message='This is a testing warning'
        )
        assert 'This is a testing warning' in str(w[-1].message)

    with warnings.catch_warnings(record=True) as w:
        check_instance(
            True,
            [str, complex],
            handle_with=Warning,
            message='This is a testing warning'
        )
        assert 'This is a testing warning' in str(w[-1].message)

    with warnings.catch_warnings(record=True) as w:
        check_instance(
            20.1,
            (int, None),
            handle_with=Warning,
            message='This is a testing warning'
        )
        assert 'This is a testing warning' in str(w[-1].message)


def test_catch_check_edge_cases():
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

    my_check = catch_check(check_if, 2 == 2, Warning)
    assert my_check is None

    my_check_not = catch_check(check_if, 2 > 2)
    with pytest.raises(AssertionError):
        raise my_check_not

    my_check_not = catch_check(check_if, 2 > 2, UserWarning, 'Problem!')
    assert isinstance(my_check_not, Warning)

    my_check_not = catch_check(check_if, 2 > 2, ValueError)
    assert isinstance(my_check_not, ValueError)
    with pytest.raises(ValueError):
        raise my_check_not

    my_check_not = catch_check(check_if, 2 > 2, Warning)
    assert isinstance(my_check_not, Warning)


def test_catch_check_if_not():
    my_check = catch_check(check_if_not, 2 > 2)
    assert my_check is None

    my_check = catch_check(check_if_not, 2 > 2, Warning, 'Problem!')
    assert my_check is None

    my_check_not = catch_check(check_if_not, 2 == 2)
    assert isinstance(my_check_not, AssertionError)
    with pytest.raises(AssertionError):
        raise my_check_not

    my_check_not = catch_check(check_if_not,
                               2 == 2,
                               handle_with=Warning,
                               message='Problem!')
    assert isinstance(my_check_not, Warning)


def test_catch_check_length():
    my_check = catch_check(check_length, [2, 2], 2)
    assert my_check is None

    my_check = catch_check(check_length,
                           [2, 2],
                           expected_length=2,
                           handle_with=Warning,
                           message='Length problem')
    assert my_check is None

    my_check_not = catch_check(check_length, [2, 2], 3)
    assert isinstance(my_check_not, LengthError)
    with pytest.raises(LengthError):
        raise my_check_not

    my_check = catch_check(check_length,
                           [2, 2],
                           expected_length=3,
                           handle_with=Warning,
                           message='Length problem')
    assert isinstance(my_check, Warning)
    assert 'Length problem' in str(my_check)


def test_catch_check_instance():
    my_check = catch_check(check_instance, 25, int)
    assert my_check is None

    my_check = catch_check(check_instance, 25, int, Warning, 'Instance issue')
    assert my_check is None

    my_check_not = catch_check(check_instance,
                               25,
                               float,
                               ValueError,
                               'This is no float!')
    assert isinstance(my_check_not, ValueError)
    with pytest.raises(ValueError, match='This is no float!'):
        raise my_check_not

    my_check = catch_check(check_instance, 25, float,
                           Warning, 'Instance issue')
    assert isinstance(my_check, Warning)

    my_check = catch_check(check_instance, 'a', int)
    assert isinstance(my_check, TypeError)
    with pytest.raises(TypeError):
        raise my_check


def test_catch_check_paths_with_return():
    existing_path = os.listdir('.')[0]
    with pytest.raises(ValueError, match='execution_mode="return"'):
        catch_check(check_if_paths_exist,
                    paths=existing_path,
                    execution_mode='return')
    with pytest.raises(ValueError, match='execution_mode="return"'):
        catch_check(check_if_paths_exist,
                    existing_path,
                    FileNotFoundError,
                    'Path not found',
                    'return')


def test_catch_check_paths_one_path():
    existing_path = os.listdir('.')[0]
    my_check = catch_check(check_if_paths_exist, paths=existing_path)
    assert my_check is None

    my_check = catch_check(check_if_paths_exist,
                           paths=existing_path,
                           handle_with=Warning,
                           message='Path problem')
    assert my_check is None

    non_existing_path = 'W:/Op/No_no'
    my_check_not = catch_check(check_if_paths_exist, paths=non_existing_path)
    assert isinstance(my_check_not, FileNotFoundError)
    with pytest.raises(FileNotFoundError):
        raise my_check_not

    my_check_not = catch_check(check_if_paths_exist,
                               paths=non_existing_path,
                               handle_with=Warning,
                               message='Path problem')
    assert isinstance(my_check_not, Warning)


def test_catch_check_paths_many_paths():
    existing_paths = os.listdir('.')
    my_check = catch_check(check_if_paths_exist, paths=existing_paths)
    assert my_check is None

    my_check = catch_check(check_if_paths_exist,
                           paths=existing_paths,
                           handle_with=Warning,
                           message='Path issue')
    assert my_check is None

    non_existing_paths = ['W:/Op/No_no'] + os.listdir('.')
    my_check_not = catch_check(check_if_paths_exist, paths=non_existing_paths)
    assert isinstance(my_check_not, FileNotFoundError)
    with pytest.raises(FileNotFoundError):
        raise my_check_not

    my_check_not = catch_check(check_if_paths_exist,
                               paths=non_existing_paths,
                               handle_with=Warning,
                               message='Path issue')
    assert isinstance(my_check_not, Warning)


def test_check_comparison_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        check_comparison(1, 1)
    with pytest.raises(TypeError, match='unexpected keyword'):
        check_comparison(item1=1, operator=gt, item_2=2)
    with pytest.raises(TypeError, match='unexpected keyword'):
        check_comparison(item_1=1, Operator=gt, item_2=2)
    with pytest.raises(TypeError, match='unexpected keyword'):
        check_comparison(item_1=1, operator=gt, item2=2)


def test_check_comparison_positive():
    assert check_comparison(2, eq, 2) is None
    assert check_comparison(2, eq, 2, Warning) is None
    assert check_comparison(2, ne, 3) is None
    assert check_comparison(2, ne, 3, Warning) is None
    assert check_comparison(2, le, 2) is None
    assert check_comparison(2, le, 2, Warning) is None
    assert check_comparison(2, ge, 2) is None
    assert check_comparison(2, ge, 2, Warning) is None
    assert check_comparison(3, ge, 2) is None
    assert check_comparison(3, ge, 2, Warning) is None
    assert check_comparison(3, gt, 2) is None
    assert check_comparison(3, gt, 2, Warning) is None
    assert check_comparison('One text', lt, 'one text') is None
    assert check_comparison('One text', lt, 'one text', Warning) is None
    assert check_comparison('One text', lt, 'another text') is None
    assert check_comparison('One text', lt, 'another text', Warning) is None
    assert check_comparison('abc', is_, 'abc') is None
    assert check_comparison('abc', is_, 'abc', Warning) is None
    assert check_comparison('abc', is_not, 'xyz') is None
    assert check_comparison('abc', is_not, 'xyz', Warning) is None


def test_check_comparison_negative():
    with pytest.raises(ValueError):
        check_comparison(3, eq, 2)
    with warnings.catch_warnings(record=True) as w:
        check_comparison(3, eq, 2, Warning, 'This is a testing warning')
        assert 'This is a testing warning' in str(w[-1].message)

    with pytest.raises(ValueError):
        check_comparison(2, ne, 2)
    with warnings.catch_warnings(record=True) as w:
        check_comparison(2, ne, 2, Warning, 'This is a testing warning')
        assert 'This is a testing warning' in str(w[-1].message)

    with pytest.raises(ValueError):
        check_comparison(2, lt, 2)
    with warnings.catch_warnings(record=True) as w:
        check_comparison(2, lt, 2, Warning, 'This is a testing warning')
        assert 'This is a testing warning' in str(w[-1].message)

    with pytest.raises(ValueError):
        check_comparison(2, gt, 2)
    with warnings.catch_warnings(record=True) as w:
        check_comparison(2, gt, 2, Warning, 'This is a testing warning')
        assert 'This is a testing warning' in str(w[-1].message)

    with pytest.raises(ValueError):
        check_comparison(3, lt, 2)
    with warnings.catch_warnings(record=True) as w:
        check_comparison(3, lt, 2, Warning, 'This is a testing warning')
        assert 'This is a testing warning' in str(w[-1].message)

    with pytest.raises(ValueError):
        check_comparison(3, le, 2)
    with warnings.catch_warnings(record=True) as w:
        check_comparison(3, le, 2, Warning, 'This is a testing warning')
        assert 'This is a testing warning' in str(w[-1].message)

    with pytest.raises(ValueError):
        check_comparison('one text', lt, 'another text')
    with warnings.catch_warnings(record=True) as w:
        check_comparison('one text', lt, 'another text',
                         Warning,
                         'This is a testing warning')
        assert 'This is a testing warning' in str(w[-1].message)

    with pytest.raises(ValueError):
        check_comparison('abc', is_, 'xyz')
    with warnings.catch_warnings(record=True) as w:
        check_comparison('abc', is_, 'xyz',
                         Warning,
                         'This is a testing warning')
        assert 'This is a testing warning' in str(w[-1].message)

    with pytest.raises(ValueError):
        check_comparison('abc', is_not, 'abc')
    with warnings.catch_warnings(record=True) as w:
        check_comparison('abc', is_not, 'abc',
                         Warning,
                         'This is a testing warning')
        assert 'This is a testing warning' in str(w[-1].message)

    with pytest.raises(ComparisonError):
        check_comparison('one text', lt, 'another text',
                         handle_with=ComparisonError)


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
    assert all(multiple_check_1.values())

    multiple_check_2 = check_all_ifs(
        (check_if, 2 > 1),
        (check_if_not, 'a' == 'a')
    )
    assert any(type(value) == AssertionError
               for value in multiple_check_2.values())

    multiple_check_3 = check_all_ifs(
        (check_if, 2 > 1),
        (check_if_not, 'a' == 'a', ValueError)
    )
    assert any(type(value) == ValueError
               for value in multiple_check_3.values())


def test_check_all_ifs_warnings():
    multiple_check_1 = check_all_ifs(
        (check_if, 2 > 1, Warning),
        (check_if, 'a' == 'a', Warning)
    )
    assert all(multiple_check_1.values())

    multiple_check_2 = check_all_ifs(
        (check_if, 2 > 1, Warning),
        (check_if_not, 'a' == 'a', Warning)
    )
    assert any(isinstance(value, Warning)
               for value in multiple_check_2.values())


def test_check_if_paths_exist_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        check_if_paths_exist()
    with pytest.raises(TypeError, match='unexpected keyword'):
        check_if_paths_exist(path='tomato soup is good')
    with pytest.raises(TypeError, match='Argument paths must be string'):
        check_if_paths_exist(20)
    with pytest.raises(TypeError, match='Argument paths must be string'):
        check_if_paths_exist(True)
    with pytest.raises(ValueError):
        check_if_paths_exist(os.listdir('.')[0], execution_mode='buuu')


def test_check_if_paths_exist_positive():
    single_path_to_check = os.listdir('.')[0]
    list_of_paths_to_check = os.listdir('.')
    assert check_if_paths_exist(single_path_to_check) is None
    assert check_if_paths_exist(single_path_to_check, Warning) is None
    assert check_if_paths_exist(single_path_to_check,
                                execution_mode='return')
    assert check_if_paths_exist(single_path_to_check,
                                handle_with=Warning,
                                execution_mode='return')

    assert check_if_paths_exist(list_of_paths_to_check) is None
    assert check_if_paths_exist(list_of_paths_to_check, Warning) is None

    check_result = check_if_paths_exist(list_of_paths_to_check,
                                        execution_mode='return')
    assert len(check_result) == 2
    assert check_result[0] is None
    assert check_result[1] == []

    check_result = check_if_paths_exist(list_of_paths_to_check,
                                        handle_with=Warning,
                                        execution_mode='return')
    assert len(check_result) == 2
    assert check_result[0] is None
    assert check_result[1] == []


def test_check_if_paths_exist_negative():
    non_existing_path = 'Z:/Op/Oop/'
    with pytest.raises(ValueError):
        check_if_paths_exist(non_existing_path, execution_mode='buuu')
    with pytest.raises(FileNotFoundError):
        check_if_paths_exist(non_existing_path)
    with pytest.raises(FileNotFoundError):
        check_if_paths_exist([non_existing_path] + os.listdir('.'))
    with pytest.raises(IOError):
        check_if_paths_exist(non_existing_path, handle_with=IOError)

    check_result = check_if_paths_exist(non_existing_path,
                                        execution_mode='return')
    assert len(check_result) == 2
    assert type(check_result[0]) == FileNotFoundError
    with pytest.raises(FileNotFoundError):
        raise check_result[0]
    assert check_result[1] == [non_existing_path]

    check_result = check_if_paths_exist(os.listdir('.') + [non_existing_path],
                                        execution_mode='return')
    assert len(check_result) == 2
    assert type(check_result[0]) == FileNotFoundError
    with pytest.raises(FileNotFoundError):
        raise check_result[0]
    assert check_result[1] == [non_existing_path]


def test_check_if_paths_exist_negative_warnings():
    non_existing_path = 'Z:/Op/Oop/'
    with warnings.catch_warnings(record=True):
        check_if_paths_exist(non_existing_path, Warning, 'Path issue')
    with warnings.catch_warnings(record=True):
        check_if_paths_exist([non_existing_path] + os.listdir('.'),
                             Warning,
                             'Path issue')

    check_result = check_if_paths_exist(non_existing_path,
                                        handle_with=Warning,
                                        message='Path issue',
                                        execution_mode='return')
    assert len(check_result) == 2
    assert type(check_result[0]) == Warning
    assert 'Path issue' in str(check_result[0])
    assert check_result[1] == [non_existing_path]

    check_result = check_if_paths_exist([non_existing_path] + os.listdir('.'),
                                        handle_with=Warning,
                                        message='Path issue',
                                        execution_mode='return')
    assert len(check_result) == 2
    assert type(check_result[0]) == Warning
    assert 'Path issue' in str(check_result[0])
    assert check_result[1] == [non_existing_path]


def test_raise_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        _raise()
    with pytest.raises(TypeError, match='unexpected keyword'):
        _raise(handle_with=TypeError)
    with pytest.raises(TypeError, match='unexpected keyword'):
        _raise(handle_with=TypeError, MEssage='This was an error')
    with pytest.raises(
            TypeError,
            match='The error argument must be an exception or a warning'):
        _raise(20)
    with pytest.raises(
            TypeError,
            match='The error argument must be an exception or a warning'):
        _raise('TypeError')
    with pytest.raises(
            TypeError,
            match='The error argument must be an exception or a warning'):
        _raise(['TypeError'])
    with pytest.raises(
            TypeError,
            match='The error argument must be an exception or a warning'):
        _raise(NotImplemented)
    with pytest.raises(TypeError, match='message must be string'):
        _raise(error=TypeError, message=20)
    with pytest.raises(TypeError, match='message must be string'):
        _raise(TypeError, ('This was an error', ''))


def test_raise_exception():
    with pytest.raises(ValueError):
        _raise(ValueError)
    with pytest.raises(TypeError):
        _raise(TypeError)
    with pytest.raises(TypeError, match='Incorrect type'):
        _raise(TypeError, 'Incorrect type')


def test_raise_warning():
    with warnings.catch_warnings(record=True):
        _raise(Warning)
    with warnings.catch_warnings(record=True):
        _raise(UserWarning)
    with warnings.catch_warnings(record=True):
        _raise(Warning, message='Problem with something')
    with warnings.catch_warnings(record=True):
        _raise(UserWarning, message='Problem with something')


def test_check_argument_edge_cases():
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
        check_argument('x', 10, handle_with=TypeError)
    assert str(msg_error.value) == msg


def test_check_argument_type():
    def foo(x):
        check_argument(x, 'x', expected_type=str)
        pass
    assert foo('one') is None
    with pytest.raises(ArgumentValueError):
        foo(4)
    with pytest.raises(ArgumentValueError):
        foo(('one', 'two'))

    assert check_argument(50, 'my_arg', expected_type=int) is None
    assert check_argument(50, expected_type=int) is None
    assert check_argument('my_arg', 'one', expected_type=str) is None
    assert check_argument('my_arg', expected_type=str) is None

    with pytest.raises(ArgumentValueError, match='my_arg'):
        check_argument(50, 'my_arg', expected_type=str)
    with pytest.raises(ArgumentValueError, match='my_arg'):
        check_argument('one', 'my_arg', expected_type=int)
    with pytest.raises(ArgumentValueError, match='argument'):
        check_argument(50, expected_type=str)
    with pytest.raises(ArgumentValueError, match='argument'):
        check_argument('one', expected_type=int)


def test_check_argument_type_warning():
    def foo(x):
        check_argument(x, 'x',
                       expected_type=str,
                       handle_with=Warning,
                       message='Incorrect argument?')
        pass
    assert foo('one') is None
    with warnings.catch_warnings(record=True) as w:
        foo(4)
        assert 'Incorrect argument' in str(w[-1].message)

    assert check_argument(50, 'my_arg',
                          expected_type=int,
                          handle_with=Warning) is None
    assert check_argument(50,
                          expected_type=int,
                          handle_with=Warning) is None

    with warnings.catch_warnings(record=True) as w:
        check_argument(50, 'my_arg',
                       expected_type=str,
                       handle_with=Warning)
        assert 'my_arg' in str(w[-1].message)
        assert 'Incorrect type' in str(w[-1].message)

    with warnings.catch_warnings(record=True) as w:
        check_argument('one', 'my_arg',
                       expected_type=int,
                       handle_with=Warning)
        assert 'my_arg' in str(w[-1].message)
        assert 'Incorrect type' in str(w[-1].message)

    with warnings.catch_warnings(record=True) as w:
        check_argument(50,
                       expected_type=str,
                       handle_with=Warning)
        assert 'Incorrect type of argument' in str(w[-1].message)

    with warnings.catch_warnings(record=True) as w:
        check_argument('one',
                       expected_type=int,
                       handle_with=Warning)
        assert 'Incorrect type of argument' in str(w[-1].message)


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


def test_check_argument_choices_warnings():
    assert check_argument(5,
                          'my_arg',
                          expected_choices=range(10),
                          handle_with=Warning) is None
    assert check_argument(5,
                          expected_choices=range(10),
                          handle_with=Warning) is None

    def foo(x):
        check_argument(x,
                       expected_choices=('first choice', 'second choice'),
                       handle_with=Warning)
        pass
    assert foo('first choice') is None
    assert foo('second choice') is None
    with warnings.catch_warnings(record=True) as w:
        foo('no choice')
        assert 'no choice' in str(w[-1].message)
        assert 'not among valid values' in str(w[-1].message)


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


def test_check_argument_length_warnings():
    assert check_argument(5, 'my_arg',
                          expected_length=1,
                          assign_length_to_others=True,
                          handle_with=Warning) is None
    assert check_argument(5,
                          expected_length=1,
                          assign_length_to_others=True,
                          handle_with=Warning) is None

    def foo(x):
        check_argument(x, 'x',
                       expected_length=3,
                       assign_length_to_others=True,
                       handle_with=Warning)
        pass
    assert foo([1, 2, 3]) is None
    with warnings.catch_warnings(record=True) as w:
        foo(1)
        assert 'length' in str(w[-1].message)

    def foo(x):
        check_argument(x,
                       expected_length=3,
                       assign_length_to_others=True,
                       handle_with=Warning)
        pass
    assert foo([1, 2, 3]) is None
    with warnings.catch_warnings(record=True) as w:
        foo(1)
        assert 'length' in str(w[-1].message)


def test_check_argument_mix():
    def foo(x):
        check_argument(x, 'x', expected_type=int, condition=x % 2 == 0)
        pass
    with pytest.raises(TypeError):
        x = 'one'
        check_argument(argument=x,
                       argument_name='x',
                       expected_type=int,
                       condition=x % 2 == 0)
    with pytest.raises(TypeError):
        foo('one')


def test_check_argument_mix_warnings():
    def foo(x):
        check_argument(x, 'x',
                       expected_type=int,
                       expected_length=3,
                       handle_with=Warning)
        pass
    with warnings.catch_warnings(record=True) as w:
        foo('one')
        assert 'type' in str(w[-1].message)


def test_check_checkit_arguments_edge_cases():
    with pytest.raises(ValueError, match='Provide at least one argument'):
        _check_checkit_arguments()
    with pytest.raises(TypeError, match='unexpected keyword'):
        _check_checkit_arguments(Handle_with=1)
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
        _check_checkit_arguments(Expected_type=1)
    with pytest.raises(TypeError, match='unexpected keyword'):
        _check_checkit_arguments(Expected_length=1)
    with pytest.raises(TypeError, match='unexpected keyword'):
        _check_checkit_arguments(handle_with=ValueError, Message=1)

    with pytest.raises(TypeError, match='handle_with must be an exception'):
        _check_checkit_arguments(handle_with=20)

    with pytest.raises(TypeError, match='handle_with must be an exception'):
        _check_checkit_arguments(handle_with=NotImplemented)


def test_check_checkit_arguments():
    assert _check_checkit_arguments(handle_with=LengthError) is None
    with pytest.raises(TypeError):
        _check_checkit_arguments(handle_with='NonExistingError')

    with pytest.raises(TypeError, match='must be an exception'):
        _check_checkit_arguments(handle_with=sum)

    with pytest.raises(TypeError):
        _check_checkit_arguments(handle_with=LengthError, message=False)
    assert _check_checkit_arguments(handle_with=LengthError,
                                    message='This is error') is None
    with pytest.raises(TypeError):
        _check_checkit_arguments(handle_with=LengthError, message=25)

    assert _check_checkit_arguments(handle_with=ValueError,
                                    condition='a' == 'a') is None
    assert _check_checkit_arguments(condition='a' == 'a') is None
    assert _check_checkit_arguments(handle_with=ValueError, condition=2 > 1) is None
    assert _check_checkit_arguments(handle_with=ValueError, condition=2 < 1) is None
    assert _check_checkit_arguments(handle_with=ValueError,
                                    condition=2 == '2') is None
    assert _check_checkit_arguments(condition=2 == '2') is None
    with pytest.raises(ValueError):
        _check_checkit_arguments(handle_with=ValueError,
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

    for this_type in (str, int, float, bool, tuple, list, Generator):
        assert _check_checkit_arguments(expected_type=this_type) is None
    for this_type in ('str', 25, True, 1.1):
        with pytest.raises(TypeError):
            _check_checkit_arguments(expected_type=this_type)
    assert _check_checkit_arguments(expected_type=(str, tuple)) is None
    assert _check_checkit_arguments(expected_type=(str, tuple, None)) is None
    assert _check_checkit_arguments(expected_type=[str, tuple]) is None
    assert _check_checkit_arguments(expected_type={str, tuple}) is None
    with pytest.raises(TypeError):
        _check_checkit_arguments(expected_type='boolintstrcomplexlist')
    with pytest.raises(TypeError):
        _check_checkit_arguments(expected_type=(str, tuple, list, 26))

    assert _check_checkit_arguments(
        expected_type=(str, tuple, list),
        condition=2 < 2,
        expected_length=3,
        execution_mode='raise',
        assign_length_to_others=True
    ) is None

    with pytest.raises(TypeError):
        _check_checkit_arguments(
            expected_type=(str, tuple, list),
            condition=2 < 2,
            expected_length=3,
            execution_mode='raise',
            assign_length_to_others='yes'
        )


def test_make_message_edge_cases():
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

