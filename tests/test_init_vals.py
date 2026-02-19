import numpy as np
import pytest

from pert import PERT


def test_init_assigns_valid_a_b_c_values():
    min_val, ml_val, max_val = 1.0, 2.0, 3.0
    dist = PERT(min_val, ml_val, max_val)

    np.testing.assert_allclose(dist.a, min_val)
    np.testing.assert_allclose(dist.b, ml_val)
    np.testing.assert_allclose(dist.c, max_val)


@pytest.mark.parametrize(
    ("min_val", "ml_val", "max_val"),
    [
        (1.0, 0.0, 2.0),
        (0.0, 2.0, 1.0),
        (2.0, 3.0, 0.0),
        (2.0, 2.0, 2.0),
    ],
)
def test_init_raises_for_invalid_parameter_ordering(min_val, ml_val, max_val):
    with pytest.raises(ValueError):
        PERT(min_val, ml_val, max_val)
