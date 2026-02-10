# Version History

## v0.1.2 (2026-01-16)
* Altered input value checks to allow for numbers smaller than `np.isclose` would measure.
* Added a halfway useful `__repr__` to the PERT class.
* Converted to using uv for env and build backend.

## v0.1.0 (2019-11-14)
* First release
* Core functionality implemented, including the following scipy method analogues:
    - rvs
    - pdf
    - logpdf
    - cdf
    - logcdf
    - stats (needs some refinement)
    - interval
