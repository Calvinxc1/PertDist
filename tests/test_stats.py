import numpy as np

from pert import PERT


def test_build_statistics_match_expected_for_symmetric_case():
    dist = PERT(0.0, 5.0, 10.0, lamb=4.0)

    np.testing.assert_allclose(dist.alpha, 3.0)
    np.testing.assert_allclose(dist.beta, 3.0)
    np.testing.assert_allclose(dist.mean, 5.0)
    np.testing.assert_allclose(dist.var, 25.0 / 7.0)
    np.testing.assert_allclose(dist.skew, 0.0)
    np.testing.assert_allclose(dist.range, 10.0)


def test_stats_returns_expected_keys_and_values():
    dist = PERT(1.0, 2.0, 4.0, lamb=4.0)
    stats = dist.stats()

    assert set(stats.keys()) == {"mean", "var", "skewness", "kurtosis"}
    np.testing.assert_allclose(stats["mean"], dist.mean)
    np.testing.assert_allclose(stats["var"], dist.var)
    np.testing.assert_allclose(stats["skewness"], dist.skew)
    np.testing.assert_allclose(stats["kurtosis"], dist.kurt)


def test_median_matches_ppf_at_half_probability():
    dist = PERT(1.0, 2.0, 4.0, lamb=4.0)

    np.testing.assert_allclose(dist.median(), dist.ppf(0.5))


def test_median_equals_mean_for_symmetric_case():
    dist = PERT(0.0, 5.0, 10.0, lamb=4.0)

    np.testing.assert_allclose(dist.median(), dist.mean)


def test_repr_includes_core_fields():
    dist = PERT(0.0, 5.0, 10.0, lamb=4.0)
    representation = repr(dist)

    assert representation.startswith("PERT(")
    for field_name in ("a=", "b=", "c=", "lamb=", "alpha=", "beta=", "mean=", "var=", "skew=", "kurt="):
        assert field_name in representation
