import decimal
import fractions
import os
import pytest
import warnings
from collections.abc import Generator
from operator import eq, le, lt, gt, ge, ne, is_, is_not
from pathlib import Path
from unittest import mock

from easycheck.easycheck import (
    check_if,
    assert_if,
    check_if_not,
    assert_if_not,
    check_if_in_limits,
    assert_if_in_limits,
    check_type,
    assert_type,
    check_if_isclose,
    assert_if_isclose,
    check_if_paths_exist,
    assert_paths,
    check_length,
    assert_length,
    check_all_ifs,
    check_argument,
    check_comparison,
    catch_check,
    LimitError,
    ComparisonError,
    ArgumentValueError,
    LengthError,
    NotCloseEnoughError,
    get_possible_operators,
    _raise,
)


def test_check_if_edge_cases():
    with pytest.raises(TypeError, match="required positional argument"):
        check_if()
    assert check_if(True) is None
    with pytest.raises(AssertionError):
        check_if(False)
    with pytest.raises(
        TypeError, match="The error argument must be an exception or a warning"
    ):
        check_if(False, 1)
    with pytest.raises(
        TypeError, match="message must be either None or string"
    ):
        check_if(0, ValueError, 1)
    with pytest.raises(TypeError, match="takes from 1 to 3 positional"):
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
    with pytest.raises(ValueError, match="incorrect value"):
        check_if(2 < 1, handle_with=ValueError, message="incorrect value")


def test_switched_off_checks_exceptions():
    with mock.patch.dict(os.environ, {"EASYCHECK_RUN": "0"}):
        assert check_if(2 < 1) is None
        assert check_if_not(1 == 1) is None
        assert check_if_in_limits(1, 3, 5) is None
        assert check_length(10, 3) is None
        assert check_if_isclose(1.12, 1.123, abs_tol=0.0005) is None
        assert check_type(True, (str, complex)) is None
        assert catch_check(check_if, 2 == 2) is None
        assert check_comparison(3, eq, 2) is None
        assert check_if_paths_exist("__file__", execution_mode="buuu") is None
        assert check_if_paths_exist("Z:/Op/Oop") is None
        assert check_argument(50, "my_arg", expected_type=str) is None
        multiple_check = check_all_ifs(
            (check_if, 2 > 1), (check_if, "a" != "a")
        )
        assert multiple_check is None


def test_switched_off_checks_warnings():
    with mock.patch.dict(os.environ, {"EASYCHECK_RUN": "0"}):
        with warnings.catch_warnings(record=True) as issues:
            check_if(2 < 1, Warning)
        check_if_not(1 == 1, Warning)
        check_if_in_limits(1, 3, 5, handle_with=Warning())
        check_length(10, 3, handle_with=Warning)
        check_type(True, (str, complex), handle_with=Warning)
        catch_check(check_if, 2 == 2, handle_with=Warning)
        check_comparison(3, eq, 2, handle_with=Warning)
        check_if_paths_exist(
            "__file__", execution_mode="buuu", handle_with=Warning
        )
        check_if_paths_exist("Z:/Op/Oop", handle_with=Warning)
        check_argument(50, "my_arg", expected_type=str, handle_with=Warning)
        multiple_check = check_all_ifs(
            (check_if, 2 > 1, Warning), (check_if, "a" != "a", Warning)
        )
        multiple_check is None
    assert not issues


def test_check_if_negative_warnings():
    with warnings.catch_warnings(record=True) as w:
        check_if(2 < 1, Warning, "This is a testing warning")
        assert "This is a testing warning" in str(w[-1].message)

    with warnings.catch_warnings(record=True) as w:
        check_if(2 < 1, UserWarning, "This is a testing warning")
        assert issubclass(w[-1].category, Warning)
        assert "This is a testing warning" in str(w[-1].message)


def test_check_if_not_edge_cases():
    with pytest.raises(TypeError, match="required positional argument"):
        check_if_not()
    assert check_if_not(False) is None
    with pytest.raises(AssertionError):
        check_if_not(True)
    with pytest.raises(
        TypeError, match="he error argument must be an exception or a warning"
    ):
        check_if_not(1, 1)
    with pytest.raises(
        TypeError, match="message must be either None or string"
    ):
        check_if_not(1, ValueError, 1)
    with pytest.raises(TypeError, match="takes from 1 to 3 positional"):
        check_if_not(1, 1, 1, 1)


def test_check_if_not_positive():
    assert check_if_not(2 < 1) is None
    assert check_if_not(2 < 1, Warning) is None
    assert check_if_not("a" == "A") is None
    assert check_if_not("a" == "A", Warning) is None


def test_check_if_not_negative():
    with pytest.raises(AssertionError):
        check_if_not(2 > 1)
    with pytest.raises(ValueError):
        check_if_not(2 > 1, handle_with=ValueError)
    with pytest.raises(ValueError, match="incorrect value"):
        check_if_not(2 > 1, handle_with=ValueError, message="incorrect value")


def test_check_if_not_negative_warnings():
    with warnings.catch_warnings(record=True) as w:
        check_if_not(2 > 1, Warning, "This is a testing warning")
        assert "This is a testing warning" in str(w[-1].message)

    with warnings.catch_warnings(record=True) as w:
        check_if_not(2 > 1, UserWarning, "This is a testing warning")
        assert issubclass(w[-1].category, Warning)
        assert "This is a testing warning" in str(w[-1].message)


def test_check_if_in_limits():
    assert check_if_in_limits(3, 1, 5) is None
    assert check_if_in_limits(3, 1, 5, handle_with=Warning) is None
    assert check_if_in_limits(3, 1) is None
    assert check_if_in_limits(3, 1, handle_with=Warning) is None
    assert check_if_in_limits(3, 3, include_equal=True) is None
    assert (
        check_if_in_limits(3, 3, include_equal=True, handle_with=Warning)
        is None
    )
    assert check_if_in_limits(3, 1, include_equal=False) is None
    assert (
        check_if_in_limits(3, 1, include_equal=False, handle_with=Warning)
        is None
    )
    assert check_if_in_limits(3, upper_limit=5) is None
    assert check_if_in_limits(3, upper_limit=5, handle_with=Warning) is None
    assert check_if_in_limits(3, lower_limit=3) is None
    assert check_if_in_limits(3, lower_limit=3, handle_with=Warning) is None
    assert check_if_in_limits(3, upper_limit=3) is None
    assert check_if_in_limits(3, upper_limit=3, handle_with=Warning) is None

    assert check_if_in_limits(0, 0, 0) is None
    assert check_if_in_limits(0, 0, 0, handle_with=Warning) is None
    assert check_if_in_limits(3.0, 1.0, 5.0) is None
    assert check_if_in_limits(3.0, 1.0, 5.0, handle_with=Warning) is None
    assert check_if_in_limits(3.0, 1, 5) is None
    assert check_if_in_limits(3.0, 1, 5, handle_with=Warning) is None
    assert check_if_in_limits(3, 1.0, 5.0) is None
    assert check_if_in_limits(3, 1.0, 5.0, handle_with=Warning) is None
    assert check_if_in_limits(-1, -3, 3) is None
    assert check_if_in_limits(-1, -3, 3, handle_with=Warning) is None
    assert check_if_in_limits(0, -1000.0, 1000.0) is None
    assert check_if_in_limits(0, -1000.0, 1000.0, handle_with=Warning) is None
    assert check_if_in_limits(0.0005, 0.0004, 0.0006) is None
    assert (
        check_if_in_limits(0.0005, 0.0004, 0.0006, handle_with=Warning) is None
    )
    assert check_if_in_limits(1000.0, 1000.0, 1000.0) is None
    assert (
        check_if_in_limits(1000.0, 1000.0, 1000.0, handle_with=Warning) is None
    )


def test_check_if_in_limits_negative():
    with pytest.raises(LimitError):
        check_if_in_limits(1, 3, 5)
    with pytest.raises(LimitError):
        check_if_in_limits(5, 1, 3)
    with pytest.raises(LimitError):
        check_if_in_limits(0, 1, 1000)
    with pytest.raises(LimitError):
        check_if_in_limits(3, 1, 3, include_equal=False)
    with pytest.raises(LimitError):
        check_if_in_limits(3, 3, 5, include_equal=False)
    with pytest.raises(LimitError):
        check_if_in_limits(0, 0, 0, include_equal=False)
    with pytest.raises(LimitError):
        check_if_in_limits(-5, 0, 1000, include_equal=False)
    with pytest.raises(LimitError):
        check_if_in_limits(1.0, 3.0, 5.0)
    with pytest.raises(LimitError):
        check_if_in_limits(0.0000001, 0.0000002, 0.0000003)
    with pytest.raises(LimitError):
        check_if_in_limits(5.0, 1.0, 3.0)
    with pytest.raises(LimitError):
        check_if_in_limits(3.05, 3.05, 5.05, include_equal=False)
    with pytest.raises(LimitError):
        check_if_in_limits(5.00005, 1.2345, 5.00005, include_equal=False)
    with pytest.raises(LimitError):
        check_if_in_limits(0.00, 0.00, 0.00, include_equal=False)
    with pytest.raises(LimitError):
        check_if_in_limits(-1.05, -0.05, 0.05, include_equal=False)
    with pytest.raises(LimitError):
        check_if_in_limits(-1000.00, -999.999, -999.998, include_equal=False)

    with pytest.raises(TypeError):
        check_if_in_limits(None)


def test_check_length_edge_cases():
    with pytest.raises(TypeError, match="required positional argument"):
        check_length("tomato soup is good")
    with pytest.raises(TypeError, match="'int' object is not callable"):
        check_length([1], 1, operator=1)


def test_check_length_positive():
    assert check_length(["string"], 1) is None
    assert check_length(["string"], 1, handle_with=Warning) is None
    assert check_length("string", 6) is None
    assert check_length("string", 6, handle_with=Warning) is None
    assert check_length([1, 2], 2) is None
    assert check_length([1, 2], 2, handle_with=Warning) is None
    assert check_length(range(0, 3), 3) is None
    assert check_length(range(0, 3), 3, handle_with=Warning) is None
    assert check_length(10, 1, assign_length_to_others=True) is None
    assert (
        check_length(10, 1, assign_length_to_others=True, handle_with=Warning)
        is None
    )
    assert (
        check_length(
            decimal.Decimal("3.55634"), 1, assign_length_to_others=True
        )
        is None
    )
    assert (
        check_length(
            fractions.Fraction(3, 55), 1, assign_length_to_others=True
        )
        is None
    )


def test_check_length_negative():
    with pytest.raises(TypeError):
        check_length(len(i for i in range(3)), 3)
    with pytest.raises(TypeError):
        check_length(None)
    with pytest.raises(TypeError, match="object of type 'int' has no len()"):
        check_length(10, 1)
    with pytest.raises(TypeError, match="'decimal.Decimal' has no len()"):
        check_length(
            decimal.Decimal("3.55634"), 1, assign_length_to_others=False
        )
    with pytest.raises(TypeError, match="'Fraction' has no len()"):
        check_length(
            fractions.Fraction(3, 55), 1, assign_length_to_others=False
        )


def test_check_length_negative_warnings():
    with warnings.catch_warnings(record=True) as w:
        check_length(
            [1, 2],
            expected_length=1,
            handle_with=Warning,
            message="This is a testing warning",
        )
        assert "This is a testing warning" in str(w[-1].message)


def test_check_if_isclose_edge_cases():
    with pytest.raises(ValueError, match="tolerances must be non-negative"):
        check_if_isclose(1.1, 1.2, abs_tol=-1)
    with pytest.raises(ValueError, match="tolerances must be non-negative"):
        check_if_isclose(1.1, 1.2, rel_tol=-1)
    with pytest.raises(TypeError, match="must be real number, not str"):
        check_if_isclose(1.1, 1.2, rel_tol=".1")
    with pytest.raises(TypeError, match="must be real number, not str"):
        check_if_isclose(1.1, 1.2, abs_tol=".1")
    with pytest.raises(
        ValueError, match="could not convert string to float: '1,1'"
    ):
        check_if_isclose("1,1", "1.2", abs_tol=".1")
    with pytest.raises(
        TypeError,
        match=("positional-only arguments passed" " as keyword arguments"),
    ):
        check_if_isclose(x="1.1", y="1.2")


def test_check_if_isclose_positive():
    assert check_if_isclose(1.12, 1.12, abs_tol=0.01) is None
    assert check_if_isclose(1.12, 1.123, abs_tol=0.05) is None
    assert check_if_isclose(1.12, 1.123, rel_tol=0.01) is None
    assert check_if_isclose(1.12, 1.123, rel_tol=0.05) is None

    assert check_if_isclose("1.12", 1.12, abs_tol=0.01) is None
    assert check_if_isclose(1.12, "1.12", abs_tol=0.01) is None
    assert check_if_isclose("1.12", "1.12", abs_tol=0.01) is None
    assert check_if_isclose(" 1.12 ", 1.12, abs_tol=0.01) is None
    assert check_if_isclose(" 1.12 ", "\t1.12\n", abs_tol=0.01) is None
    assert (
        check_if_isclose(
            " 1.12 ", "\t     1.12   \n  \n   \n\n\n", abs_tol=0.01
        )
        is None
    )

    assert (
        check_if_isclose(1.12, 1.123, rel_tol=0.05, handle_with=ValueError)
        is None
    )

    # any of the two check (abs_tol or rel_tol) is enough
    # for the test to pass:
    assert check_if_isclose(1.12, 1.123, rel_tol=0.05, abs_tol=0.05) is None

    check_if_isclose(1.12, 1.123, rel_tol=0.000005, abs_tol=0.05)


def test_check_if_isclose_negative():
    with pytest.raises(NotCloseEnoughError):
        check_if_isclose(1.12, 1.123, abs_tol=0.0005)
    with pytest.raises(NotCloseEnoughError):
        check_if_isclose(
            1.12, 1.123, message="Not close", rel_tol=0, abs_tol=0.0005
        )
    with pytest.raises(NotCloseEnoughError):
        check_if_isclose(1.12, 1.123, rel_tol=0.0005)


def test_check_type_edge_cases():
    with pytest.raises(TypeError, match="required positional argument"):
        check_type("tomato soup is good")


def test_check_type_positive():
    assert check_type(["string"], list) is None
    assert check_type(["string"], list, handle_with=Warning) is None
    assert check_type("string", str) is None
    assert check_type("string", str, handle_with=Warning) is None
    assert check_type((1, 2), tuple) is None
    assert check_type((1, 2), tuple, handle_with=Warning) is None
    assert check_type((1, 2), [tuple, list]) is None
    assert check_type((1, 2), [tuple, list], handle_with=Warning) is None
    assert check_type((1, 2), [list, tuple]) is None
    assert check_type((1, 2), {tuple, list}, handle_with=Warning) is None
    assert (
        check_type((1, 2), (tuple, list), message="Neither tuple nor list")
        is None
    )
    assert (
        check_type(
            (1, 2),
            (tuple, list),
            message="Neither tuple nor list",
            handle_with=Warning,
        )
        is None
    )
    assert check_type((i for i in range(3)), Generator) is None
    assert (
        check_type((i for i in range(3)), Generator, handle_with=Warning)
        is None
    )
    assert check_type(None, (int, None)) is None
    assert check_type(None, (int, None), handle_with=Warning) is None
    assert check_type(20, (int, None)) is None
    assert check_type(20, (int, None), handle_with=Warning) is None
    assert check_type(None, None) is None
    assert check_type(None, None, handle_with=Warning) is None


def test_check_type_negative():
    with pytest.raises(TypeError, match="Neither tuple nor list"):
        check_type("souvenir", (tuple, list), message="Neither tuple nor list")
    with pytest.raises(TypeError):
        check_type("souvenir", [tuple, list])
    with pytest.raises(TypeError):
        check_type("souvenir", {tuple, list})
    with pytest.raises(TypeError):
        check_type(True, (str, complex))
    with pytest.raises(TypeError):
        check_type(20.1, (int, None))
    with pytest.raises(TypeError):
        check_type((i for i in range(3)), tuple)
    with pytest.raises(TypeError, match="This is not tuple"):
        check_type((i for i in range(3)), tuple, message="This is not tuple")
    with pytest.raises(TypeError):
        check_type(10, None)
    with pytest.raises(TypeError):
        check_type("string", None)
    with pytest.raises(TypeError):
        check_type((10, 20), None)
    with pytest.raises(TypeError):
        check_type([10, 20], None)


def test_check_type_negative_warnings():
    with warnings.catch_warnings(record=True) as w:
        check_type(
            "souvenir",
            (tuple, list),
            handle_with=Warning,
            message="This is a testing warning",
        )
        assert "This is a testing warning" in str(w[-1].message)

    with warnings.catch_warnings(record=True) as w:
        check_type(
            True,
            [str, complex],
            handle_with=Warning,
            message="This is a testing warning",
        )
        assert "This is a testing warning" in str(w[-1].message)

    with warnings.catch_warnings(record=True) as w:
        check_type(
            20.1,
            (int, None),
            handle_with=Warning,
            message="This is a testing warning",
        )
        assert "This is a testing warning" in str(w[-1].message)


def test_catch_check_edge_cases():
    with pytest.raises(TypeError, match="required positional argument"):
        catch_check(check=check_type)
    with pytest.raises(TypeError, match="easycheck function"):
        catch_check(1)
    with pytest.raises(
        ArgumentValueError, match="acceptable valid easycheck functions"
    ):
        catch_check(sum)


def test_catch_check_if():
    my_check = catch_check(check_if, 2 == 2)
    assert my_check is None

    my_check = catch_check(check_if, 2 == 2, Warning)
    assert my_check is None

    my_check_not = catch_check(check_if, 2 > 2)
    with pytest.raises(AssertionError):
        raise my_check_not

    my_check_not = catch_check(check_if, 2 > 2, UserWarning, "Problem!")
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

    my_check = catch_check(check_if_not, 2 > 2, Warning, "Problem!")
    assert my_check is None

    my_check_not = catch_check(check_if_not, 2 == 2)
    assert isinstance(my_check_not, AssertionError)
    with pytest.raises(AssertionError):
        raise my_check_not

    my_check_not = catch_check(
        check_if_not, 2 == 2, handle_with=Warning, message="Problem!"
    )
    assert isinstance(my_check_not, Warning)


def test_catch_check_if_in_limits():
    my_check = catch_check(check_if_in_limits, 3, 1, 5)
    assert my_check is None

    my_check = catch_check(check_if_in_limits, 3, 1, 5, handle_with=Warning)
    assert my_check is None

    my_check = catch_check(check_if_in_limits, 0, 1, 5, handle_with=Warning)
    assert isinstance(my_check, Warning)

    my_check = catch_check(
        check_if_in_limits,
        0,
        1,
        5,
        handle_with=Warning,
        message="Number out of limits",
    )
    assert isinstance(my_check, Warning)
    assert "Number out of limits" in str(my_check)

    my_check = catch_check(check_if_in_limits, 0, 1, 5)
    assert isinstance(my_check, LimitError)
    with pytest.raises(LimitError):
        raise my_check


def test_catch_check_length():
    my_check = catch_check(check_length, [2, 2], 2)
    assert my_check is None

    my_check = catch_check(
        check_length,
        [2, 2],
        expected_length=2,
        handle_with=Warning,
        message="Length problem",
    )
    assert my_check is None

    my_check_not = catch_check(check_length, [2, 2], 3)
    assert isinstance(my_check_not, LengthError)
    with pytest.raises(LengthError):
        raise my_check_not

    my_check = catch_check(
        check_length,
        [2, 2],
        expected_length=3,
        handle_with=Warning,
        message="Length problem",
    )
    assert isinstance(my_check, Warning)
    assert "Length problem" in str(my_check)


def test_catch_check_type():
    my_check = catch_check(check_type, 25, int)
    assert my_check is None

    my_check = catch_check(check_type, 25, int, Warning, "Instance issue")
    assert my_check is None

    my_check_not = catch_check(
        check_type, 25, float, ValueError, "This is no float!"
    )
    assert isinstance(my_check_not, ValueError)
    with pytest.raises(ValueError, match="This is no float!"):
        raise my_check_not

    my_check = catch_check(check_type, 25, float, Warning, "Instance issue")
    assert isinstance(my_check, Warning)

    my_check = catch_check(check_type, "a", int)
    assert isinstance(my_check, TypeError)
    with pytest.raises(TypeError):
        raise my_check


def test_catch_check_paths_with_return():
    existing_path = os.listdir(".")[0]
    with pytest.raises(ValueError, match='execution_mode="return"'):
        catch_check(
            check_if_paths_exist, paths=existing_path, execution_mode="return"
        )
    with pytest.raises(ValueError, match='execution_mode="return"'):
        catch_check(
            check_if_paths_exist,
            existing_path,
            FileNotFoundError,
            "Path not found",
            "return",
        )


def test_catch_check_paths_one_path():
    existing_path = os.listdir(".")[0]
    my_check = catch_check(check_if_paths_exist, paths=existing_path)
    my_check_path = catch_check(
        check_if_paths_exist, paths=Path(existing_path)
    )
    assert my_check is None
    assert my_check_path is None

    my_check = catch_check(
        check_if_paths_exist,
        paths=existing_path,
        handle_with=Warning,
        message="Path problem",
    )
    assert my_check is None
    my_check_path = catch_check(
        check_if_paths_exist,
        paths=Path(existing_path),
        handle_with=Warning,
        message="Path problem",
    )
    assert my_check_path is None

    non_existing_path = "W:/Op/No_no"
    my_check_not = catch_check(check_if_paths_exist, paths=non_existing_path)
    my_check_not_path = catch_check(
        check_if_paths_exist, paths=Path(non_existing_path)
    )
    assert isinstance(my_check_not, FileNotFoundError)
    with pytest.raises(FileNotFoundError):
        raise my_check_not
    assert isinstance(my_check_not_path, FileNotFoundError)
    with pytest.raises(FileNotFoundError):
        raise my_check_not_path

    my_check_not = catch_check(
        check_if_paths_exist,
        paths=non_existing_path,
        handle_with=Warning,
        message="Path problem",
    )
    assert isinstance(my_check_not, Warning)


def test_catch_check_paths_many_paths():
    existing_paths = os.listdir(".")
    my_check = catch_check(check_if_paths_exist, paths=existing_paths)
    my_check_path = catch_check(
        check_if_paths_exist, paths=[Path(path) for path in existing_paths]
    )
    assert my_check is None
    assert my_check_path is None

    my_check = catch_check(
        check_if_paths_exist,
        paths=existing_paths,
        handle_with=Warning,
        message="Path issue",
    )
    assert my_check is None

    non_existing_paths = ["W:/Op/No_no"] + os.listdir(".")
    my_check_not = catch_check(check_if_paths_exist, paths=non_existing_paths)
    my_check_not_path = catch_check(
        check_if_paths_exist, paths=[Path(path) for path in non_existing_paths]
    )
    assert isinstance(my_check_not, FileNotFoundError)
    with pytest.raises(FileNotFoundError):
        raise my_check_not
    assert isinstance(my_check_not_path, FileNotFoundError)
    with pytest.raises(FileNotFoundError):
        raise my_check_not_path

    my_check_not = catch_check(
        check_if_paths_exist,
        paths=non_existing_paths,
        handle_with=Warning,
        message="Path issue",
    )
    assert isinstance(my_check_not, Warning)


def test_catch_check_if_isclose():
    my_check = catch_check(check_if_isclose, 1.12, 1.12, abs_tol=0.01)
    assert my_check is None

    my_check = catch_check(check_if_isclose, 1.12, 1.123, abs_tol=0.05)
    assert my_check is None

    my_check = catch_check(check_if_isclose, 1.12, 1.123, rel_tol=0.01)
    assert my_check is None

    my_check = catch_check(check_if_isclose, 1.12, 1.123, rel_tol=0.05)
    assert my_check is None

    my_check_not = catch_check(check_if_isclose, 1.12, 1.123, abs_tol=0.0005)
    assert isinstance(my_check_not, NotCloseEnoughError)
    with pytest.raises(NotCloseEnoughError):
        raise my_check_not

    my_check_not = catch_check(
        check_if_isclose,
        1.12,
        1.123,
        message="Not close",
        rel_tol=0,
        abs_tol=0.0005,
    )
    assert isinstance(my_check_not, NotCloseEnoughError)
    with pytest.raises(NotCloseEnoughError):
        raise my_check_not


def test_check_comparison_edge_cases():
    with pytest.raises(TypeError, match="required positional argument"):
        check_comparison(1, 1)
    with pytest.raises(TypeError, match="unexpected keyword"):
        check_comparison(item1=1, operator=gt, item_2=2)
    with pytest.raises(TypeError, match="unexpected keyword"):
        check_comparison(item_1=1, Operator=gt, item_2=2)
    with pytest.raises(TypeError, match="unexpected keyword"):
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
    assert check_comparison("One text", lt, "one text") is None
    assert check_comparison("One text", lt, "one text", Warning) is None
    assert check_comparison("One text", lt, "another text") is None
    assert check_comparison("One text", lt, "another text", Warning) is None
    assert check_comparison("abc", is_, "abc") is None
    assert check_comparison("abc", is_, "abc", Warning) is None
    assert check_comparison("abc", is_not, "xyz") is None
    assert check_comparison("abc", is_not, "xyz", Warning) is None


def test_check_comparison_negative():
    with pytest.raises(ValueError):
        check_comparison(3, eq, 2)
    with warnings.catch_warnings(record=True) as w:
        check_comparison(3, eq, 2, Warning, "This is a testing warning")
        assert "This is a testing warning" in str(w[-1].message)

    with pytest.raises(ValueError):
        check_comparison(2, ne, 2)
    with warnings.catch_warnings(record=True) as w:
        check_comparison(2, ne, 2, Warning, "This is a testing warning")
        assert "This is a testing warning" in str(w[-1].message)

    with pytest.raises(ValueError):
        check_comparison(2, lt, 2)
    with warnings.catch_warnings(record=True) as w:
        check_comparison(2, lt, 2, Warning, "This is a testing warning")
        assert "This is a testing warning" in str(w[-1].message)

    with pytest.raises(ValueError):
        check_comparison(2, gt, 2)
    with warnings.catch_warnings(record=True) as w:
        check_comparison(2, gt, 2, Warning, "This is a testing warning")
        assert "This is a testing warning" in str(w[-1].message)

    with pytest.raises(ValueError):
        check_comparison(3, lt, 2)
    with warnings.catch_warnings(record=True) as w:
        check_comparison(3, lt, 2, Warning, "This is a testing warning")
        assert "This is a testing warning" in str(w[-1].message)

    with pytest.raises(ValueError):
        check_comparison(3, le, 2)
    with warnings.catch_warnings(record=True) as w:
        check_comparison(3, le, 2, Warning, "This is a testing warning")
        assert "This is a testing warning" in str(w[-1].message)

    with pytest.raises(ValueError):
        check_comparison("one text", lt, "another text")
    with warnings.catch_warnings(record=True) as w:
        check_comparison(
            "one text",
            lt,
            "another text",
            Warning,
            "This is a testing warning",
        )
        assert "This is a testing warning" in str(w[-1].message)

    with pytest.raises(ValueError):
        check_comparison("abc", is_, "xyz")
    with warnings.catch_warnings(record=True) as w:
        check_comparison(
            "abc", is_, "xyz", Warning, "This is a testing warning"
        )
        assert "This is a testing warning" in str(w[-1].message)

    with pytest.raises(ValueError):
        check_comparison("abc", is_not, "abc")
    with warnings.catch_warnings(record=True) as w:
        check_comparison(
            "abc", is_not, "abc", Warning, "This is a testing warning"
        )
        assert "This is a testing warning" in str(w[-1].message)

    with pytest.raises(ComparisonError):
        check_comparison(
            "one text", lt, "another text", handle_with=ComparisonError
        )


def test_check_all_ifs_edge_cases():
    with pytest.raises(ValueError, match="at least one condition"):
        check_all_ifs()
    with pytest.raises(TypeError, match="Provide all function calls as"):
        check_all_ifs(1)
    with pytest.raises(TypeError, match="Provide all function calls as"):
        check_all_ifs(True)
    with pytest.raises(TypeError, match="Provide all function calls as"):
        check_all_ifs(1, 1)
    with pytest.raises(TypeError, match="Provide all function calls as"):
        check_all_ifs(1 > 1, 2 > 1)
    with pytest.raises(TypeError, match="Provide all function calls as"):
        check_all_ifs((20 > 10))
    with pytest.raises(TypeError, match="Provide all function calls as"):
        check_all_ifs(check_if(20 > 10)),
    with pytest.raises(TypeError, match="Provide all function calls as"):
        check_all_ifs((check_if, 20 > 10), (check_if(20 > 10)))


def test_check_all_ifs():
    multiple_check_1 = check_all_ifs((check_if, 2 > 1), (check_if, "a" == "a"))
    assert all(multiple_check_1.values())

    multiple_check_2 = check_all_ifs(
        (check_if, 2 > 1), (check_if_not, "a" == "a")
    )
    assert any(
        type(value) == AssertionError for value in multiple_check_2.values()
    )

    multiple_check_3 = check_all_ifs(
        (check_if, 2 > 1), (check_if_not, "a" == "a", ValueError)
    )
    assert any(
        type(value) == ValueError for value in multiple_check_3.values()
    )


def test_check_all_ifs_warnings():
    multiple_check_1 = check_all_ifs(
        (check_if, 2 > 1, Warning), (check_if, "a" == "a", Warning)
    )
    assert all(multiple_check_1.values())

    multiple_check_2 = check_all_ifs(
        (check_if, 2 > 1, Warning), (check_if_not, "a" == "a", Warning)
    )
    assert any(
        isinstance(value, Warning) for value in multiple_check_2.values()
    )


def test_check_if_paths_exist_edge_cases():
    with pytest.raises(TypeError, match="required positional argument"):
        check_if_paths_exist()
    with pytest.raises(TypeError, match="unexpected keyword"):
        check_if_paths_exist(path="tomato soup is good")
    with pytest.raises(TypeError, match="Argument paths must be string"):
        check_if_paths_exist(20)
    with pytest.raises(TypeError, match="Argument paths must be string"):
        check_if_paths_exist(True)
    with pytest.raises(TypeError, match="Argument paths must be string"):
        check_if_paths_exist(["/some/path", 1, 2])
    with pytest.raises(TypeError, match="Argument paths must be string"):
        check_if_paths_exist(["/some/path", Path("/some/path"), False])
    with pytest.raises(ValueError):
        check_if_paths_exist(os.listdir(".")[0], execution_mode="buuu")


def test_check_if_paths_exist_positive():
    single_path_to_check = os.listdir(".")[0]
    list_of_paths_to_check = os.listdir(".")
    assert check_if_paths_exist(single_path_to_check) is None
    assert check_if_paths_exist(single_path_to_check, Warning) is None
    assert check_if_paths_exist(single_path_to_check, execution_mode="return")
    assert check_if_paths_exist(
        single_path_to_check, handle_with=Warning, execution_mode="return"
    )
    assert check_if_paths_exist(Path(single_path_to_check)) is None

    assert check_if_paths_exist(list_of_paths_to_check) is None
    assert check_if_paths_exist(list_of_paths_to_check, Warning) is None
    assert (
        check_if_paths_exist(Path(path) for path in list_of_paths_to_check)
        is None
    )

    check_result = check_if_paths_exist(
        list_of_paths_to_check, execution_mode="return"
    )
    assert len(check_result) == 2
    assert check_result[0] is None
    assert check_result[1] == []

    check_result = check_if_paths_exist(
        list_of_paths_to_check, handle_with=Warning, execution_mode="return"
    )
    assert len(check_result) == 2
    assert check_result[0] is None
    assert check_result[1] == []


def test_check_if_paths_exist_negative():
    non_existing_path = "Z:/Op/Oop"
    with pytest.raises(ValueError):
        check_if_paths_exist(non_existing_path, execution_mode="buuu")
    with pytest.raises(FileNotFoundError):
        check_if_paths_exist(non_existing_path)
    with pytest.raises(FileNotFoundError):
        check_if_paths_exist(Path(non_existing_path))
    with pytest.raises(FileNotFoundError):
        check_if_paths_exist([non_existing_path] + os.listdir("."))
    with pytest.raises(IOError):
        check_if_paths_exist(non_existing_path, handle_with=IOError)

    check_result = check_if_paths_exist(
        non_existing_path, execution_mode="return"
    )
    assert len(check_result) == 2
    assert type(check_result[0]) == FileNotFoundError
    with pytest.raises(FileNotFoundError):
        raise check_result[0]
    assert check_result[1] == [non_existing_path]

    check_result = check_if_paths_exist(
        os.listdir(".") + [non_existing_path], execution_mode="return"
    )
    assert len(check_result) == 2
    assert type(check_result[0]) == FileNotFoundError
    with pytest.raises(FileNotFoundError):
        raise check_result[0]
    assert check_result[1] == [non_existing_path]


def test_check_if_paths_exist_negative_warnings():
    non_existing_path = "Z:/Op/Oop"
    with warnings.catch_warnings(record=True):
        check_if_paths_exist(non_existing_path, Warning, "Path issue")
    with warnings.catch_warnings(record=True):
        check_if_paths_exist(Path(non_existing_path), Warning, "Path issue")
    with warnings.catch_warnings(record=True):
        check_if_paths_exist(
            [non_existing_path] + os.listdir("."), Warning, "Path issue"
        )

    check_result = check_if_paths_exist(
        non_existing_path,
        handle_with=Warning,
        message="Path issue",
        execution_mode="return",
    )
    assert len(check_result) == 2
    assert type(check_result[0]) == Warning
    assert "Path issue" in str(check_result[0])
    assert check_result[1] == [non_existing_path]

    check_result = check_if_paths_exist(
        [non_existing_path] + os.listdir("."),
        handle_with=Warning,
        message="Path issue",
        execution_mode="return",
    )
    assert len(check_result) == 2
    assert type(check_result[0]) == Warning
    assert "Path issue" in str(check_result[0])
    assert check_result[1] == [non_existing_path]


def test_raise_edge_cases():
    with pytest.raises(TypeError, match="required positional argument"):
        _raise()
    with pytest.raises(TypeError, match="unexpected keyword"):
        _raise(handle_with=TypeError)
    with pytest.raises(TypeError, match="unexpected keyword"):
        _raise(handle_with=TypeError, MEssage="This was an error")
    with pytest.raises(
        TypeError, match="The error argument must be an exception or a warning"
    ):
        _raise(20)
    with pytest.raises(
        TypeError, match="The error argument must be an exception or a warning"
    ):
        _raise("TypeError")
    with pytest.raises(
        TypeError, match="The error argument must be an exception or a warning"
    ):
        _raise(["TypeError"])
    with pytest.raises(
        TypeError, match="The error argument must be an exception or a warning"
    ):
        _raise(NotImplemented)
    with pytest.raises(
        TypeError, match="Argument message must be either None or string"
    ):
        _raise(error=TypeError, message=20)
    with pytest.raises(
        TypeError, match="Argument message must be either None or string"
    ):
        _raise(TypeError, ("This was an error", ""))


def test_raise_exception():
    with pytest.raises(ValueError):
        _raise(ValueError)
    with pytest.raises(TypeError):
        _raise(TypeError)
    with pytest.raises(TypeError, match="Incorrect type"):
        _raise(TypeError, "Incorrect type")


def test_raise_warning():
    with warnings.catch_warnings(record=True):
        _raise(Warning)
    with warnings.catch_warnings(record=True):
        _raise(UserWarning)
    with warnings.catch_warnings(record=True):
        _raise(Warning, message="Problem with something")
    with warnings.catch_warnings(record=True):
        _raise(UserWarning, message="Problem with something")


def test_check_argument_edge_cases():
    with pytest.raises(TypeError, match="required positional argument"):
        check_argument(Argument="x")

    msg = "check_argument() requires at least one condition to be checked"
    with pytest.raises(ValueError) as msg_error:
        check_argument(10)
    assert str(msg_error.value) == msg
    with pytest.raises(ValueError) as msg_error:
        check_argument(10, message="Error!")
    assert str(msg_error.value) == msg
    with pytest.raises(ValueError) as msg_error:
        check_argument("x", 10, handle_with=TypeError)
    assert str(msg_error.value) == msg


def test_check_argument_type():
    def foo(x):
        check_argument(x, "x", expected_type=str)
        pass

    assert foo("one") is None
    with pytest.raises(ArgumentValueError):
        foo(4)
    with pytest.raises(ArgumentValueError):
        foo(("one", "two"))

    assert check_argument(50, "my_arg", expected_type=int) is None
    assert check_argument(50, expected_type=int) is None
    assert check_argument("my_arg", "one", expected_type=str) is None
    assert check_argument("my_arg", expected_type=str) is None

    with pytest.raises(ArgumentValueError, match="my_arg"):
        check_argument(50, "my_arg", expected_type=str)
    with pytest.raises(ArgumentValueError, match="my_arg"):
        check_argument("one", "my_arg", expected_type=int)
    with pytest.raises(ArgumentValueError, match="argument"):
        check_argument(50, expected_type=str)
    with pytest.raises(ArgumentValueError, match="argument"):
        check_argument("one", expected_type=int)


def test_check_argument_type_warning():
    def foo(x):
        check_argument(
            x,
            "x",
            expected_type=str,
            handle_with=Warning,
            message="Incorrect argument?",
        )
        pass

    assert foo("one") is None
    with warnings.catch_warnings(record=True) as w:
        foo(4)
        assert "Incorrect argument" in str(w[-1].message)

    assert (
        check_argument(50, "my_arg", expected_type=int, handle_with=Warning)
        is None
    )
    assert check_argument(50, expected_type=int, handle_with=Warning) is None

    with warnings.catch_warnings(record=True) as w:
        check_argument(50, "my_arg", expected_type=str, handle_with=Warning)
        assert "my_arg" in str(w[-1].message)
        assert "Incorrect type" in str(w[-1].message)

    with warnings.catch_warnings(record=True) as w:
        check_argument("one", "my_arg", expected_type=int, handle_with=Warning)
        assert "my_arg" in str(w[-1].message)
        assert "Incorrect type" in str(w[-1].message)

    with warnings.catch_warnings(record=True) as w:
        check_argument(50, expected_type=str, handle_with=Warning)
        assert "Incorrect type of argument" in str(w[-1].message)

    with warnings.catch_warnings(record=True) as w:
        check_argument("one", expected_type=int, handle_with=Warning)
        assert "Incorrect type of argument" in str(w[-1].message)


def test_check_argument_choices():
    assert (
        check_argument(
            5,
            "my_arg",
            expected_choices=range(10),
        )
        is None
    )
    assert check_argument(5, expected_choices=range(10)) is None

    def foo(x):
        check_argument(x, expected_choices=("first choice", "second choice"))
        pass

    assert foo("first choice") is None
    assert foo("second choice") is None
    with pytest.raises(ArgumentValueError, match="not among valid values"):
        foo("no choice")

    def foo(x):
        check_argument(x, "x", expected_choices=("one", "two"))
        pass

    assert foo("one") is None
    with pytest.raises(
        ArgumentValueError, match="x's value, three, is not among valid values"
    ):
        foo("three")

    def foo(x):
        check_argument(x, expected_choices=("one", "two"))
        pass

    assert foo("one") is None
    with pytest.raises(
        ArgumentValueError,
        match="argument's value, three, is not among valid values",
    ):
        foo("three")


def test_check_argument_choices_warnings():
    assert (
        check_argument(
            5, "my_arg", expected_choices=range(10), handle_with=Warning
        )
        is None
    )
    assert (
        check_argument(5, expected_choices=range(10), handle_with=Warning)
        is None
    )

    def foo(x):
        check_argument(
            x,
            expected_choices=("first choice", "second choice"),
            handle_with=Warning,
        )
        pass

    assert foo("first choice") is None
    assert foo("second choice") is None
    with warnings.catch_warnings(record=True) as w:
        foo("no choice")
        assert "no choice" in str(w[-1].message)
        assert "not among valid values" in str(w[-1].message)


def test_check_argument_length():
    assert (
        check_argument(
            5, "my_arg", expected_length=1, assign_length_to_others=True
        )
        is None
    )
    assert (
        check_argument(5, expected_length=1, assign_length_to_others=True)
        is None
    )

    def foo(x):
        check_argument(x, "x", expected_length=3, assign_length_to_others=True)
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
        check_argument(
            big_x, "big_x", expected_length=3, assign_length_to_others=True
        )
        pass

    assert foo([1, 2, 3]) is None
    with pytest.raises(ArgumentValueError, match="big_x"):
        foo(1)

    def foo(big_x):
        check_argument(big_x, expected_length=3, assign_length_to_others=True)
        pass

    assert foo([1, 2, 3]) is None
    with pytest.raises(ArgumentValueError, match="argument"):
        foo(1)


def test_check_argument_length_warnings():
    assert (
        check_argument(
            5,
            "my_arg",
            expected_length=1,
            assign_length_to_others=True,
            handle_with=Warning,
        )
        is None
    )
    assert (
        check_argument(
            5,
            expected_length=1,
            assign_length_to_others=True,
            handle_with=Warning,
        )
        is None
    )

    def foo(x):
        check_argument(
            x,
            "x",
            expected_length=3,
            assign_length_to_others=True,
            handle_with=Warning,
        )
        pass

    assert foo([1, 2, 3]) is None
    with warnings.catch_warnings(record=True) as w:
        foo(1)
        assert "length" in str(w[-1].message)

    def foo(x):
        check_argument(
            x,
            expected_length=3,
            assign_length_to_others=True,
            handle_with=Warning,
        )
        pass

    assert foo([1, 2, 3]) is None
    with warnings.catch_warnings(record=True) as w:
        foo(1)
        assert "length" in str(w[-1].message)


def test_check_argument_mix():
    def foo(x):
        check_argument(x, "x", expected_type=int, condition=x % 2 == 0)
        pass

    with pytest.raises(TypeError):
        x = "one"
        check_argument(
            argument=x,
            argument_name="x",
            expected_type=int,
            condition=x % 2 == 0,
        )
    with pytest.raises(TypeError):
        foo("one")


def test_check_argument_mix_warnings():
    def foo(x):
        check_argument(
            x, "x", expected_type=int, expected_length=3, handle_with=Warning
        )
        pass

    with warnings.catch_warnings(record=True) as w:
        foo("one")
        assert "type" in str(w[-1].message)


def test_assert_functions():
    assert assert_if(10 > 5) == check_if(10 > 5)
    with pytest.raises(AssertionError):
        assert_if(10 < 5) and check_if(10 < 5) is None

    assert assert_if_not(10 < 5) == check_if_not(10 < 5)
    with pytest.raises(AssertionError):
        assert_if_not(10 > 5) and check_if_not(10 > 5) is None

    assert assert_type((10, 10), tuple) == check_type((10, 10), tuple)
    with pytest.raises(TypeError):
        assert_type(10, tuple) and check_type(10, tuple) is None

    assert assert_length("str", 3) == check_length("str", 3)
    assert assert_length(5, 1, assign_length_to_others=True) == check_length(
        5, 1, assign_length_to_others=True
    )
    with pytest.raises(TypeError):
        assert_length(5, 3) and check_length(5, 3) is None
    with pytest.raises(LengthError):
        (
            assert_length(5, 3, assign_length_to_others=True)
            and check_length(5, 3, assign_length_to_others=True) is None
        )

    existing_file = os.listdir(".")[0]
    assert check_if_paths_exist(
        existing_file, execution_mode="return"
    ) == assert_paths(existing_file, execution_mode="return")
    assert (
        check_if_paths_exist("Q:/E/", execution_mode="return")[1]
        == assert_paths("Q:/E/", execution_mode="return")[1]
    )
    with pytest.raises(FileNotFoundError):
        assert_paths("Q:/E/") and check_if_paths_exist("Q:/E/") is None


class ForTestingErrorWithDoc(Exception):
    """This is error for testing purposes."""


class ForTestingErrorWithoutDoc(Exception):
    ...


def test_message_is_None_exception_with_docstring():
    with pytest.raises(AssertionError, match=""):
        check_if(1 == 2, message=None)
    with pytest.raises(AssertionError, match="Error"):
        check_if(1 == 2, message="Error")
    with pytest.raises(AssertionError):
        check_if(1 == 2)
    assert check_if(1 == 1, ForTestingErrorWithDoc) is None
    with pytest.raises(ForTestingErrorWithDoc, match="for testing purposes"):
        check_if(1 == 2, ForTestingErrorWithDoc)


def test_message_is_None_exception_without_docstring():
    assert check_if(1 == 1, ForTestingErrorWithoutDoc) is None
    with pytest.raises(ForTestingErrorWithoutDoc, match="Error! Shout!"):
        check_if(1 == 2, ForTestingErrorWithoutDoc, message="Error! Shout!")
    with pytest.raises(ForTestingErrorWithoutDoc, match=""):
        check_if(1 == 2, ForTestingErrorWithoutDoc)
