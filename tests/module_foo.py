from easycheck import check_if, assert_if
def foo():
    check_if(1 == 2)

def test_foo():
    assert_if(1 == 2)

if __name__ == "__main__":
    foo()
