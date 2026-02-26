import numpy as np
import pytest

from pert import PERT


@pytest.mark.parametrize("lamb", [0.0, -1.0])
def test_lamb_must_be_greater_than_zero(lamb):
    with pytest.raises(ValueError, match="lamb parameter should be greater than 0"):
        PERT(0.0, 1.0, 2.0, lamb=lamb)


@pytest.mark.parametrize(
    ("min_val", "ml_val", "max_val", "lamb"),
    [
        (np.nan, 1.0, 2.0, 4.0),
        (0.0, np.inf, 2.0, 4.0),
        (0.0, 1.0, np.nan, 4.0),
        (0.0, 1.0, 2.0, np.inf),
    ],
)
def test_non_finite_inputs_raise(min_val, ml_val, max_val, lamb):
    with pytest.raises(ValueError, match="Non-finite values present in inputs."):
        PERT(min_val, ml_val, max_val, lamb=lamb)


def test_array_inputs_raise_when_any_element_violates_ordering():
    with pytest.raises(
        ValueError, match="min_val parameter should be lower than ml_val"
    ):
        PERT(np.array([0.0, 5.0]), np.array([1.0, 4.0]), np.array([2.0, 6.0]))


def test_non_broadcastable_shapes_raise():
    with pytest.raises(ValueError):
        PERT(np.array([0.0, 1.0]), np.array([1.0, 2.0, 3.0]), np.array([2.0, 3.0, 4.0]))
