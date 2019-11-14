import numpy as np
from scipy.special import beta, betainc
from scipy.stats import beta as beta_dist
from scipy.stats import norm as norm_dist

Array = np.array

class PERT:
    """ Implementation of the Beta-PERT distribution
    
    A custom implementation of the Beta-PERT distribution (also shorthand
    referred to as the PERT distributon) using `numpy` and `scipy`. Methods
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
    
    def __init__(self, min_val:Array, ml_val:Array, max_val:Array, lamb=4.0):
        if lamb <= 0:
            raise ValueError('lamb parameter should be greater than 0.')
        
        self.a = np.asarray(min_val)
        self.b = np.asarray(ml_val)
        self.c = np.asarray(max_val)
        self.lamb = lamb
        
        self.build()
        
    def build(self):
        """ Calculates core PERT statistics
        
        PERT statistics can be found on [Wikipedia](https://en.wikipedia.org/wiki/PERT_distribution)
        Note that these values have been modified to accomodate for a flexible lambda value (per
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
    def range(self):
        """ Calculates the min-max range
        
        Returns
        -------
        Array:
            Array of range values of max-min.
        """
        return np.asarray(self.c - self.a)
    
    def rvs(self, size=1, random_state=None):
        """ Returns a randompy-sampled value from the PERT
        
        Parameters
        ----------
        size: int (default 1)
            Indicates how many random values should be returned
        random_state: int (default none)
            Seed value for random sample RNG.
            
        Returns
        -------
        Array:
            Randomly sampled values from the PERT dristribution.
        """
        
        rvs_vals = (beta_dist(self.alpha, self.beta).rvs(size=size, random_state=random_state) * self.range) + self.a
        return rvs_vals
    
    def pdf(self, val:Array) -> Array:
        """ Calculates the PDF value for a set of inputs
        
        Parameters
        ----------
        val: numeric or numeric-array
            Values to return the PDF calcualtion on
        
        Returns
        -------
        Array:
            PDF values based on the val parameter
        """
        
        x = ((val - self.a) / self.range).clip(0,1)
        pdf_val = beta_dist.pdf(x, self.alpha, self.beta) / self.range
        return pdf_val
    
    def logpdf(self, val) -> Array:
        """ Calculates the log-PDF value for a set of inputs
        
        Parameters
        ----------
        val: numeric or numeric-array
            Values to return the log-PDF calcualtion on
        
        Returns
        -------
        Array:
            Log-PDF values based on the val parameter
        """
        
        logpdf_val = np.log(self.pdf(val))
        return logpdf_val
    
    def cdf(self, val) -> Array:
        """ Calculates the CDF value for a set of inputs
        
        Parameters
        ----------
        val: numeric or numeric-array
            Values to return the CDF calcualtion on
        
        Returns
        -------
        Array:
            CDF values based on the val parameter
        """
        
        x = ((val - self.a) / self.range).clip(0,1)
        cdf_val = beta_dist.cdf(x, self.alpha, self.beta) / self.range
        return cdf_val
    
    def logcdf(self, val) -> Array:
        """ Calculates the log-CDF value for a set of inputs
        
        Parameters
        ----------
        val: numeric or numeric-array
            Values to return the log-CDF calcualtion on
        
        Returns
        -------
        Array:
            Log-CDF values based on the val parameter
        """
        
        logcdf_val = np.log(self.cdf(val))
        return logcdf_val
    
    def stats(self) -> dict:
        """ Returns basic statistics on the PERT
        
        Returns
        -------
        dict:
            Contains the PERT mean, variance, skewness and kurtosis
        """
        
        stats = {
            'mean': self.mean,
            'var': self.var,
            'skewness': self.skew,
            'kurtosis': self.kurt,
        }
        return stats
    
    def interval(self, alpha:float) -> Array:
        """ Calculates the endpoints of a confidence interval range using alpha
        
        Parameters
        ----------
        alpha: float
            Percent of distribution to be caintained within returned interval.
            Must be between 0.0 and 1.0
            
        Returns
        -------
        Array:
            Array containing the interval range, first element is the low end of
            the range, second element is the high end of the range.
        """
        
        interval = beta_dist.interval(alpha, self.alpha, self.beta)
        interval = np.array([(val * self.range) + self.a for val in interval])
        return interval
    
    def ci(self, z:float) -> Array:
        """ Calculates the endpoints of a confidence interval range using z-score
        
        Parameters
        ----------
        z: float
            Z-score to calibrate the % of distribution interval returned.
            
        Returns
        -------
        Array:
            Array containing the interval range, first element is the low end of
            the range, second element is the high end of the range.
        """
        
        alpha = norm_dist.cdf(z) - norm_dist.cdf(-z)
        ci = self.interval(alpha)
        return ci