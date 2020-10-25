import os
import pytest
import sys

from checkit.testing import (easy_mock,
                             mock,
                             assert_if,
                             assert_if_not,
                             assert_instance,
                             assert_length,
                             assert_paths)

from checkit.checks import (check_if,
                            check_if_not,
                            check_instance,
                            check_if_paths_exist,
                            check_length,
                            LengthError)


def test_easy_mock_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        x = easy_mock()
        sys.argv = easy_mock(sys.argv)
    with pytest.raises(TypeError, match='unexpected keyword'):
        sys.argv = easy_mock(Item=sys.argv, returns=[10, 20])
        sys.argv = easy_mock(item=sys.argv, Returns=[10, 20])


def test_easy_mock_for_function():
    def foo(): return 5
    assert foo() == 5

    for to_return in (10, 100, 500, 'a'):
        foo = easy_mock(foo, returns=to_return)
        assert foo() == to_return


def test_easy_mock_for_string():
    string = ('It should be a very long string, much longer '
              'than it actually is, but no one wanted to waste'
              'time on writing this string. Frankly, it was'
              'not about time to waste but about what to write: '
              'Are you so creative to write a very long string '
              'that no one will ever read? That\'s more difficult '
              'than singing a song about how beautiful the blue sky is!'
              )
    string = easy_mock(string, returns='a mock string')
    assert string == 'a mock string'
    string = easy_mock(string, returns='let us change it')
    assert string == 'let us change it'
    string = easy_mock(string, returns='a mock string')
    assert string == 'a mock string'


def test_mock_edge_cases():
    with pytest.raises(TypeError, match='required positional argument'):
        original_x, x = mock()
        original_sys_argv, sys.argv = mock(sys.argv)
    with pytest.raises(TypeError, match='unexpected keyword'):
        original_sys_argv, sys.argv = mock(Item=sys.argv, returns=[10, 20])
        original_sys_argv, sys.argv = mock(item=sys.argv, Returns=[10, 20])


def test_mock_for_function():
    def foo(): return 5
    assert foo() == 5

    original_foo, foo = mock(foo, 500)
    assert foo() == 500
    assert original_foo() == 5

    foo = original_foo
    assert foo() == 5


def test_easy_mock_for_string():
    string = ('It should be a very long string, much longer '
              'than it actually is, but no one wanted to waste'
              'time on writing this string. Frankly, it was'
              'not about time to waste but about what to write: '
              'Are you so creative to write a very long string '
              'that no one will ever read? That\'s more difficult '
              'than singing a song about how beautiful the blue sky is!'
              )
    original_string, string = mock(string, returns='a mock string')
    assert string == 'a mock string'
    assert len(string) < len(original_string)
    string = original_string
    assert string != 'a mock string'


def test_assert_functions():
    assert assert_if(10 > 5) == check_if(10 > 5)
    with pytest.raises(AssertionError):
        assert_if(10 < 5)
        check_if(10 < 5)

    assert assert_if_not(10 < 5) == check_if_not(10 < 5)
    with pytest.raises(AssertionError):
        assert_if_not(10 > 5)
        check_if_not(10 > 5)

    assert assert_instance((10, 10), tuple) == check_instance((10, 10), tuple)
    with pytest.raises(TypeError):
        assert_instance(10, tuple)
        check_instance(10, tuple)

    assert assert_length('str', 3) == check_length('str', 3)
    assert (
        assert_length(5, 1, assign_length_to_numbers=True) ==
        check_length(5, 1, assign_length_to_numbers=True))
    with pytest.raises(TypeError):
        assert_length(5, 3)
        check_length(5, 3)
    with pytest.raises(LengthError):
        assert_length(5, 3, assign_length_to_numbers=True)
        check_length(5, 3, assign_length_to_numbers=True)

    existing_file = os.listdir('.')[0]
    assert (check_if_paths_exist(existing_file, execution_mode='return') ==
            assert_paths(existing_file, execution_mode='return'))
    assert (check_if_paths_exist('Q:/E/', execution_mode='return')[1] ==
            assert_paths('Q:/E/', execution_mode='return')[1])
    with pytest.raises(FileNotFoundError):
        assert_paths('Q:/E/')
        check_if_paths_exist('Q:/E/')
