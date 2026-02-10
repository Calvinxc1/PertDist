import pytest

from pert import PERT

def test_valid_a_b_c():
    min_val, ml_val, max_val = 1, 2, 3
    dist = PERT(min_val, ml_val, max_val)
    assert dist.a == min_val
    assert dist.b == ml_val
    assert dist.c == max_val

def test_invalid_a_b():
    with pytest.raises(ValueError):
        PERT(1, 0, 2)

def test_invalid_b_c():
    with pytest.raises(ValueError):
        PERT(0, 2, 1)

def test_invalid_a_c():
    with pytest.raises(ValueError):
        PERT(2, 3, 0)

def test_equal_a_b_c():
    with pytest.raises(ValueError):
        PERT(2, 2, 2)
