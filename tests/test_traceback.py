import pytest
from easycheck.easycheck import check_if, check_if_in_limits

def test_tracebackhide_in_check_if():
    with pytest.raises(AssertionError) as check_if_1:
        check_if(2 < 1)
    assert len(check_if_1.traceback) < 3, "Traceback should be reduced when __tracebackhide__ is used"
    for frame in check_if_1.traceback:
        assert "__tracebackhide__" not in str(frame), \
            "Frames with __tracebackhide__ should not be included in the traceback"
    with pytest.raises(ValueError, match="incorrect value") as check_if_2:
        check_if(2 < 1, handle_with=ValueError, message="incorrect value")
    assert len(check_if_2.traceback) < 3, "Traceback should be reduced when __tracebackhide__ is used"
    for frame in check_if_2.traceback:
        assert "__tracebackhide__" not in str(frame), \
            "Frames with __tracebackhide__ should not be included in the traceback"

def test_tracebackhide_in_check_if_in_limits():
    with pytest.raises(LimitError) as check_limit:
        check_if_in_limits(5, 1, 3)
    assert len(check_limit.traceback) < 3, "Traceback should be reduced when __tracebackhide__ is used"
    for frame in check_limit.traceback:
        assert "__tracebackhide__" not in str(frame), \
            "Frames with __tracebackhide__ should not be included in the traceback"

