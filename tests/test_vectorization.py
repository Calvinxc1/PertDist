import numpy as np

from pert import PERT


def test_vectorized_parameters_produce_vectorized_outputs():
    dist = PERT(
        np.array([0.0, 10.0]),
        np.array([5.0, 15.0]),
        np.array([10.0, 20.0]),
    )
    vals = np.array([5.0, 15.0])
    probs = np.array([0.25, 0.75])

    assert dist.pdf(vals).shape == (2,)
    assert dist.cdf(vals).shape == (2,)
    assert dist.ppf(probs).shape == (2,)
    assert dist.interval(0.9).shape == (2, 2)


def test_vectorized_rvs_shape_is_size_by_parameter_shape():
    dist = PERT(
        np.array([0.0, 10.0]),
        np.array([5.0, 15.0]),
        np.array([10.0, 20.0]),
    )
    samples = dist.rvs(size=(200, 2), random_state=123)

    assert samples.shape == (200, 2)
