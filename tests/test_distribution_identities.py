import math

import numpy as np

from pert import PERT


def test_cdf_and_sf_boundary_behavior():
    dist = PERT(0.0, 5.0, 10.0)

    np.testing.assert_allclose(dist.cdf(0.0), 0.0)
    np.testing.assert_allclose(dist.cdf(10.0), 1.0)
    np.testing.assert_allclose(dist.cdf(-1.0), 0.0)
    np.testing.assert_allclose(dist.cdf(11.0), 1.0)

    np.testing.assert_allclose(dist.sf(0.0), 1.0)
    np.testing.assert_allclose(dist.sf(10.0), 0.0)
    np.testing.assert_allclose(dist.sf(-1.0), 1.0)
    np.testing.assert_allclose(dist.sf(11.0), 0.0)


def test_pdf_clips_outside_support_consistently():
    dist = PERT(0.0, 5.0, 10.0)

    np.testing.assert_allclose(dist.pdf(-1.0), dist.pdf(0.0))
    np.testing.assert_allclose(dist.pdf(11.0), dist.pdf(10.0))


def test_inverse_relationships_for_cdf_ppf_and_sf_isf():
    dist = PERT(0.0, 5.0, 10.0)
    xs = np.array([1.0, 3.0, 5.0, 7.0, 9.0])

    np.testing.assert_allclose(dist.ppf(dist.cdf(xs)), xs, rtol=1e-10, atol=1e-10)
    np.testing.assert_allclose(dist.isf(dist.sf(xs)), xs, rtol=1e-10, atol=1e-10)
    np.testing.assert_allclose(dist.cdf(xs) + dist.sf(xs), np.ones_like(xs), rtol=1e-12, atol=1e-12)


def test_log_methods_match_logs_of_base_methods():
    dist = PERT(0.0, 5.0, 10.0)
    xs = np.array([1.0, 3.0, 5.0, 7.0, 9.0])

    np.testing.assert_allclose(dist.logpdf(xs), np.log(dist.pdf(xs)))
    np.testing.assert_allclose(dist.logcdf(xs), np.log(dist.cdf(xs)))
    np.testing.assert_allclose(dist.logsf(xs), np.log(dist.sf(xs)))


def test_interval_is_ordered_and_within_support():
    dist = PERT(0.0, 5.0, 10.0)
    low, high = dist.interval(0.90)

    assert low <= high
    assert 0.0 <= low <= 10.0
    assert 0.0 <= high <= 10.0


def test_ci_matches_interval_with_equivalent_alpha():
    dist = PERT(0.0, 5.0, 10.0)
    z = 1.96
    alpha = math.erf(z / np.sqrt(2.0))

    np.testing.assert_allclose(dist.ci(z), dist.interval(alpha))


def test_ci_is_ordered_and_within_support():
    dist = PERT(0.0, 5.0, 10.0)
    low, high = dist.ci(1.0)

    assert low <= high
    assert 0.0 <= low <= 10.0
    assert 0.0 <= high <= 10.0
