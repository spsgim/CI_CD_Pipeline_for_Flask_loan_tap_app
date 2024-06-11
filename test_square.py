# unit test
from square_func import get_square

def test_get_square():
    a=6
    res = get_square(a)
    assert res == 36