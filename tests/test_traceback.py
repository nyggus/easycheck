import pytest

def test_skip_simple():
    with pytest.raises(pytest.skip.Exception) as excinfo:
        pytest.skip("xxx")

    # checking the last frame in the traceback
    assert excinfo.traceback[-1].frame.code.name == "skip"
    assert excinfo.traceback[-1].ishidden(excinfo)

    # checking the second-to-last frame in the traceback
    assert excinfo.traceback[-2].frame.code.name == "test_skip_simple"
    assert not excinfo.traceback[-2].ishidden(excinfo)

if __name__ == "__main__":
    pytest.main(["--full-trace"])