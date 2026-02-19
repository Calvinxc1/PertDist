import numpy as np

from pert import PERT


def test_rvs_is_reproducible_with_fixed_random_state():
    dist = PERT(0.0, 5.0, 10.0)

    sample_a = dist.rvs(size=100, random_state=12345)
    sample_b = dist.rvs(size=100, random_state=12345)

    np.testing.assert_allclose(sample_a, sample_b)


def test_rvs_stays_within_min_and_max_bounds():
    dist = PERT(0.0, 5.0, 10.0)
    samples = dist.rvs(size=10000, random_state=7)

    assert np.min(samples) >= dist.a
    assert np.max(samples) <= dist.c


def test_rvs_sample_mean_is_close_to_theoretical_mean():
    dist = PERT(0.0, 5.0, 10.0)
    samples = dist.rvs(size=50000, random_state=99)

    np.testing.assert_allclose(np.mean(samples), dist.mean, atol=0.08)
