import pytest
import sys

from checkit.testing import easy_mock, mock


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

