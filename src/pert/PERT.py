from typing import Optional, overload

import numpy as np
from numpy.typing import NDArray
from scipy.stats import beta as beta_dist
from scipy.stats import norm as norm_dist


class PERT:
    """ Implementation of the Beta-PERT distribution
    
    A custom implementation of the Beta-PERT distribution (also shorthand
    referred to as the PERT distribution) using `numpy` and `scipy`. Methods
    mimic `scipy.stats` classes.
    
    Parameters
    ----------
    min_val: numeric or numeric-array
        The minimum value(s) of the PERT.
    ml_val: numeric or numeric-array
        The most-likely value(s) of the PERT.
    max_val: numeric or numeric-array
        The maximum value(s) of the PERT.
    lamb: float (default 4.0)
        The PERT's lambda parameter, smaller values give a wider probability spread.
        
    Attributes
    ----------
    a: Array
        Contains the PERT minimum values in np.array form.
    b: Array
        Contains the PERT most likely values in np.array form.
    c: Array
        Contains the PERT maximum values in np.array form.
    range: Array
        Contains the PERT max - min range.
    lamb: float
        The PERT lambda parameter. Should be greater than 0.
    alpha: Array
        Contains the PERT alpha values, as a part of the Beta distribution calculation.
    beta: Array
        Contains the PERT beta values, as a part of the Beta distribution calculation.
    mean: Array
        Contains the PERT mean values.
    var: Array
        Contains the PERT variance values.
    skew: Array
        Contains the PERT skewness values.
    kurt: Array
        Contains the PERT kurtosis values.
    """

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

        if np.any(lamb <= 0):
            raise ValueError('lamb parameter should be greater than 0.')
        if np.any(self.b < self.a):
            raise ValueError('min_val parameter should be lower than ml_val.')
        if np.any(self.c < self.b):
            raise ValueError('ml_val parameter should be lower than max_val.')
        # in case any a == b == c. Deals with arrays and floating error
        if np.any(self.a == self.b) or np.any(self.b == self.c):
            raise ValueError('min_val, ml_val and max_val parameter should be different.')

        self.build()


    def build(self) -> None:
        """ Calculates core PERT statistics

        PERT statistics can be found on [Wikipedia](https://en.wikipedia.org/wiki/PERT_distribution)
        Note that these values have been modified to accommodate for a flexible lambda value (per
        modified-PERT on Wikipedia).
        """

        self.alpha = np.asarray(1 + (self.lamb * ((self.b-self.a) / (self.c-self.a))))
        self.beta = np.asarray(1 + (self.lamb * ((self.c-self.b) / (self.c-self.a))))

        self.mean = np.asarray((self.a + (self.lamb*self.b) + self.c) / (2+self.lamb))
        self.var = np.asarray(((self.mean-self.a) * (self.c-self.mean)) / (self.lamb+3))
        self.skew = np.asarray((
            2 * (self.beta - self.alpha) * np.sqrt(self.alpha + self.beta + 1)
        ) / (
            (self.alpha + self.beta + 2) * np.sqrt(self.alpha * self.beta)
        ))
        self.kurt = np.asarray((
            (self.lamb+2) * ((
                ((self.alpha - self.beta)**2) * (self.alpha + self.beta + 1)
            ) + (
                self.alpha * self.beta * (self.alpha + self.beta + 2)
            ))
        ) / (
            self.alpha * self.beta * (self.alpha + self.beta + 2) * (self.alpha + self.beta + 3)
        ))

    @property
    def range(self) -> NDArray:
        """ Calculates the min-max range

        Returns
        -------
        NDArray
            Array of range values of max-min.
        """
        return np.asarray(self.c - self.a)

    def median(self) -> NDArray:
        """ Calculates the median
        
        Returns
        -------
        NDArray
            Array of median values.
        """
        median = (beta_dist(self.alpha, self.beta).median() * self.range) + self.a
        return median

    def rvs(self, size: int = 1, random_state: Optional[int] = None) -> NDArray:
        """ Returns a randomly-sampled value from the PERT
        
        Parameters
        ----------
        size: int (default 1)
            Indicates how many random values should be returned
        random_state: int (default none)
            Seed value for random sample RNG.
            
        Returns
        -------
        NDArray
            Randomly sampled values from the PERT distribution.
        """

        rvs_vals = (
            beta_dist(self.alpha, self.beta).rvs(size=size, random_state=random_state) * self.range
        ) + self.a
        return rvs_vals

    @overload
    def pdf(self, val: float) -> float: ...

    @overload
    def pdf(self, val: NDArray) -> NDArray: ...

    def pdf(self, val: float | NDArray) -> float | NDArray:
        """ Calculates the PDF value for a set of inputs
        
        Parameters
        ----------
        val: numeric or numeric-array
            Values to return the PDF calculation on
        
        Returns
        -------
        float | NDArray
            PDF values based on the val parameter
        """

        x = ((val - self.a) / self.range).clip(0,1)
        pdf_val = beta_dist.pdf(x, self.alpha, self.beta) / self.range
        return pdf_val

    @overload
    def logpdf(self, val: float) -> float: ...

    @overload
    def logpdf(self, val: NDArray) -> NDArray: ...

    def logpdf(self, val: float | NDArray) -> float | NDArray:
        """ Calculates the log-PDF value for a set of inputs
        
        Parameters
        ----------
        val: numeric or numeric-array
            Values to return the log-PDF calculation on
        
        Returns
        -------
        float | NDArray
            Log-PDF values based on the val parameter
        """

        logpdf_val = np.log(self.pdf(val))
        return logpdf_val

    @overload
    def cdf(self, val: float) -> float: ...

    @overload
    def cdf(self, val: NDArray) -> NDArray: ...

    def cdf(self, val: float | NDArray) -> float | NDArray:
        """ Calculates the CDF value for a set of inputs
        
        Parameters
        ----------
        val: numeric or numeric-array
            Values to return the CDF calculation on
        
        Returns
        -------
        float | NDArray
            CDF values based on the val parameter
        """

        x = ((val - self.a) / self.range).clip(0,1)
        cdf_val = beta_dist.cdf(x, self.alpha, self.beta)
        return cdf_val

    @overload
    def sf(self, val: float) -> float: ...

    @overload
    def sf(self, val: NDArray) -> NDArray: ...

    def sf(self, val: float | NDArray) -> float | NDArray:
        """ Calculates the survival function for a set of inputs

        Parameters
        ----------
        val: numeric or numeric-array
            Values to return the survival function calculation on
        
        Returns
        -------
        float | NDArray
            survival function based on the val parameter
        """

        x = ((val - self.a) / self.range).clip(0,1)
        sf_val = beta_dist.sf(x, self.alpha, self.beta)
        return sf_val

    @overload
    def logsf(self, val: float) -> float: ...

    @overload
    def logsf(self, val: NDArray) -> NDArray: ...

    def logsf(self, val: float | NDArray) -> float | NDArray:
        """ Calculates the log of the survival function for a set of inputs
        
        Parameters
        ----------
        val: numeric or numeric-array
            Values to return the log of the survival calculation on
        
        Returns
        -------
        float | NDArray
            log of the survival function based on the val parameter
        """

        x = ((val - self.a) / self.range).clip(0,1)
        logsf_val = beta_dist.logsf(x, self.alpha, self.beta)
        return logsf_val

    @overload
    def ppf(self, val: float) -> float: ...

    @overload
    def ppf(self, val: NDArray) -> NDArray: ...

    def ppf(self, val: float | NDArray) -> float | NDArray:
        """ Calculates the inverse CDF for a set of inputs
        
        Parameters
        ----------
        val: numeric or numeric-array
            Values to return the inverse CDF calculation on the val parameter
        
        Returns
        -------
        float | NDArray
            CDF values based on the val parameter
        """

        ppf_val = beta_dist.ppf(val, self.alpha, self.beta) * self.range + self.a
        return ppf_val

    @overload
    def isf(self, val: float) -> float: ...

    @overload
    def isf(self, val: NDArray) -> NDArray: ...

    def isf(self, val: float | NDArray) -> float | NDArray:
        """ Calculates the inverse survival function for a set of inputs
        
        Parameters
        ----------
        val: numeric or numeric-array
        
            Values to return the inverse survival function calculation on the val parameter
        Returns
        -------
        float | NDArray
            inverse of the survival function values based on the val parameter
        """
        isf_val = beta_dist.isf(val, self.alpha, self.beta) * self.range + self.a
        return isf_val

    @overload
    def logcdf(self, val: float) -> float: ...

    @overload
    def logcdf(self, val: NDArray) -> NDArray: ...

    def logcdf(self, val: float | NDArray) -> float | NDArray:
        """ Calculates the log-CDF value for a set of inputs
        
        Parameters
        ----------
        val: numeric or numeric-array
            Values to return the log-CDF calculation on
        
        Returns
        -------
        float | NDArray
            Log-CDF values based on the val parameter
        """

        logcdf_val = np.log(self.cdf(val))
        return logcdf_val

    def stats(self) -> dict[str, NDArray]:
        """ Returns basic statistics on the PERT
        
        Returns
        -------
        dict[str, NDArray]
            Contains the PERT mean, variance, skewness and kurtosis
        """

        stats = {
            'mean': self.mean,
            'var': self.var,
            'skewness': self.skew,
            'kurtosis': self.kurt,
        }
        return stats

    def interval(self, alpha: float) -> NDArray:
        """ Calculates the endpoints of a confidence interval range using alpha
        
        Parameters
        ----------
        alpha: float
            Percent of distribution to be contained within returned interval.
            Must be between 0.0 and 1.0
            
        Returns
        -------
        NDArray
            Array containing the interval range, first element is the low end of
            the range, second element is the high end of the range.
        """

        beta_interval = beta_dist.interval(alpha, self.alpha, self.beta)
        interval = np.array([(val * self.range) + self.a for val in beta_interval])
        return interval

    def ci(self, z: float) -> NDArray:
        """ Calculates the endpoints of a confidence interval range using z-score
        
        Parameters
        ----------
        z: float
            Z-score to calibrate the % of distribution interval returned.
            
        Returns
        -------
        NDArray
            Array containing the interval range, first element is the low end of
            the range, second element is the high end of the range.
        """

        alpha = norm_dist.cdf(z) - norm_dist.cdf(-z)
        ci = self.interval(alpha)
        return ci

    def __repr__(self):
        return (
            f"{type(self).__name__}(a={self.a}, b={self.b}, c={self.c}, lamb={self.lamb},"
            f" alpha={self.alpha}, beta={self.beta}, mean={self.mean}, var={self.var},"
            f" skew={self.skew}, kurt={self.kurt})"
        )
