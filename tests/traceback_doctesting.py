import easycheck
import pytest
import io
from contextlib import redirect_stdout


def test_foo():
    easycheck.assert_if(1 == 2)


def run_tests():
    f = io.StringIO()
    with redirect_stdout(f):
        pytest.main([__file__ + '::test_foo'])
    output = f.getvalue()

    lines = output.strip().splitlines()
    start = 0
    relevant_lines = []
    for line in lines:
        if start:
            relevant_lines.append(line)
            start += 1
        if start == 4:
            break
        if "test_foo" in line: start = 1
        
    relevant_output = "\n".join(relevant_lines)
    return relevant_output


def example_doctest():
    """
    >>> run_tests_output = run_tests()
    >>> print(run_tests_output)  # doctest: +ELLIPSIS
        def test_foo():
    >       easycheck.assert_if(1 == 2)
    E       AssertionError
    """


if __name__ == "__main__":
    print(run_tests())
