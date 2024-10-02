import pytest

def test_skip_simple():
    with pytest.raises(pytest.skip.Exception) as excinfo:
        pytest.skip("xxx")

    # Sprawdzenie ostatniej ramki w tracebacku
    assert excinfo.traceback[-1].frame.code.name == "skip"
    assert excinfo.traceback[-1].ishidden(excinfo)

    # Sprawdzenie przedostatniej ramki w tracebacku
    assert excinfo.traceback[-2].frame.code.name == "test_skip_simple"
    assert not excinfo.traceback[-2].ishidden(excinfo)