from typing import Optional, TypeVar, cast

import numpy as np
from numpy.typing import NDArray
from scipy.stats import beta as beta_dist
from scipy.stats import norm as norm_dist

# Preserve input/output shape for scalar vs vectorized calls.
ScalarOrArrayT = TypeVar("ScalarOrArrayT", float, NDArray)


class PERT:
    """Beta-PERT distribution."""

    a: NDArray
    b: NDArray
    c: NDArray
    lamb: float
    alpha: NDArray
    beta: NDArray
    mean: NDArray
    var: NDArray
    skew: NDArray
    kurt: NDArray

    def __init__(
        self,
        min_val: float | NDArray,
        ml_val: float | NDArray,
        max_val: float | NDArray,
        lamb: float = 4.0,
    ) -> None:
        self.a = np.asarray(min_val)
        self.b = np.asarray(ml_val)
        self.c = np.asarray(max_val)
        self.lamb = lamb

        if not (
            np.isfinite(self.a).all()
            and np.isfinite(self.b).all()
            and np.isfinite(self.c).all()
            and np.isfinite(self.lamb)
        ):
            raise ValueError("Non-finite values present in inputs.")
        if np.any(lamb <= 0):
            raise ValueError("lamb parameter should be greater than 0.")
        if np.any(self.b < self.a):
            raise ValueError("min_val parameter should be lower than ml_val.")
        if np.any(self.c < self.b):
            raise ValueError("ml_val parameter should be lower than max_val.")
        # Reject degenerate ranges.
        if np.any(self.a == self.b) or np.any(self.b == self.c):
            raise ValueError(
                "min_val, ml_val and max_val parameter should be different."
            )

        self.build()

    def build(self) -> None:
        """Compute shape parameters and cached summary stats."""

        self.alpha = np.asarray(
            1 + (self.lamb * ((self.b - self.a) / (self.c - self.a)))
        )
        self.beta = np.asarray(
            1 + (self.lamb * ((self.c - self.b) / (self.c - self.a)))
        )

        self.mean = np.asarray(
            (self.a + (self.lamb * self.b) + self.c) / (2 + self.lamb)
        )
        self.var = np.asarray(
            ((self.mean - self.a) * (self.c - self.mean)) / (self.lamb + 3)
        )
        self.skew = np.asarray(
            (2 * (self.beta - self.alpha) * np.sqrt(self.alpha + self.beta + 1))
            / ((self.alpha + self.beta + 2) * np.sqrt(self.alpha * self.beta))
        )
        self.kurt = np.asarray(
            (
                (self.lamb + 2)
                * (
                    (((self.alpha - self.beta) ** 2) * (self.alpha + self.beta + 1))
                    + (self.alpha * self.beta * (self.alpha + self.beta + 2))
                )
            )
            / (
                self.alpha
                * self.beta
                * (self.alpha + self.beta + 2)
                * (self.alpha + self.beta + 3)
            )
        )

    @property
    def range(self) -> NDArray:
        """Return max-min for each distribution."""
        return np.asarray(self.c - self.a)

    def median(self) -> NDArray:
        """Return the distribution median."""
        median = (beta_dist(self.alpha, self.beta).median() * self.range) + self.a
        return median

    def rvs(
        self, size: int | tuple[int, ...] = 1, random_state: Optional[int] = None
    ) -> NDArray:
        """Sample random values from the distribution."""

        rvs_vals = (
            beta_dist(self.alpha, self.beta).rvs(size=size, random_state=random_state)
            * self.range
        ) + self.a
        return rvs_vals

    def _to_unit_interval(self, val: float | NDArray) -> NDArray:
        """Map `val` to [0, 1] using distribution bounds."""
        return np.asarray((val - self.a) / self.range).clip(0, 1)

    def _from_unit_interval(self, val: float | NDArray) -> NDArray:
        """Map unit-interval values back to distribution scale."""
        return np.asarray(val) * self.range + self.a

    def pdf(self, val: ScalarOrArrayT) -> ScalarOrArrayT:
        """Return PDF values at `val`."""

        x = self._to_unit_interval(val)
        pdf_val = beta_dist.pdf(x, self.alpha, self.beta) / self.range
        return cast(ScalarOrArrayT, pdf_val)

    def logpdf(self, val: ScalarOrArrayT) -> ScalarOrArrayT:
        """Return log-PDF values at `val`."""

        logpdf_val = np.log(self.pdf(val))
        return cast(ScalarOrArrayT, logpdf_val)

    def cdf(self, val: ScalarOrArrayT) -> ScalarOrArrayT:
        """Return CDF values at `val`."""

        x = self._to_unit_interval(val)
        cdf_val = beta_dist.cdf(x, self.alpha, self.beta)
        return cast(ScalarOrArrayT, cdf_val)

    def sf(self, val: ScalarOrArrayT) -> ScalarOrArrayT:
        """Return survival-function values at `val`."""

        x = self._to_unit_interval(val)
        sf_val = beta_dist.sf(x, self.alpha, self.beta)
        return cast(ScalarOrArrayT, sf_val)

    def logsf(self, val: ScalarOrArrayT) -> ScalarOrArrayT:
        """Return log survival-function values at `val`."""

        x = self._to_unit_interval(val)
        logsf_val = beta_dist.logsf(x, self.alpha, self.beta)
        return cast(ScalarOrArrayT, logsf_val)

    def ppf(self, val: ScalarOrArrayT) -> ScalarOrArrayT:
        """Return inverse-CDF (quantile) values for `val`."""

        ppf_val = beta_dist.ppf(val, self.alpha, self.beta)
        return cast(ScalarOrArrayT, self._from_unit_interval(ppf_val))

    def isf(self, val: ScalarOrArrayT) -> ScalarOrArrayT:
        """Return inverse survival-function values for `val`."""

        isf_val = beta_dist.isf(val, self.alpha, self.beta)
        return cast(ScalarOrArrayT, self._from_unit_interval(isf_val))

    def logcdf(self, val: ScalarOrArrayT) -> ScalarOrArrayT:
        """Return log-CDF values at `val`."""

        logcdf_val = np.log(self.cdf(val))
        return cast(ScalarOrArrayT, logcdf_val)

    def stats(self) -> dict[str, NDArray]:
        """Return mean, variance, skewness, and kurtosis."""

        stats = {
            "mean": self.mean,
            "var": self.var,
            "skewness": self.skew,
            "kurtosis": self.kurt,
        }
        return stats

    def interval(self, alpha: float) -> NDArray:
        """Return central interval endpoints for coverage `alpha`."""

        beta_interval = beta_dist.interval(alpha, self.alpha, self.beta)
        interval = np.array([(val * self.range) + self.a for val in beta_interval])
        return interval

    def ci(self, z: float) -> NDArray:
        """Return central interval endpoints for z-score `z`."""

        alpha = norm_dist.cdf(z) - norm_dist.cdf(-z)
        ci = self.interval(alpha)
        return ci

    def __repr__(self):
        return (
            f"{type(self).__name__}(a={self.a}, b={self.b}, c={self.c}, lamb={self.lamb},"
            f" alpha={self.alpha}, beta={self.beta}, mean={self.mean}, var={self.var},"
            f" skew={self.skew}, kurt={self.kurt})"
        )
