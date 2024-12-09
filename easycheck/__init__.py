from .easycheck import (
    # functions
    check_if,
    check_if_not,
    check_type,
    check_if_paths_exist,
    check_length,
    check_if_isclose,
    check_all_ifs,
    check_argument,
    check_comparison,
    catch_check,
    # Exception classes
    ComparisonError,
    ArgumentValueError,
    LengthError,
    NotCloseEnoughError,
    # Testing aliases
    assert_if,
    assert_if_not,
    assert_length,
    assert_if_isclose,
    assert_type,
    assert_paths,
    # Backward-compatibility aliases
    check_instance,
    assert_instance,
)

from operator import eq, le, lt, gt, ge, ne, is_, is_not
