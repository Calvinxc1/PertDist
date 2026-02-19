# Version History

## v0.1.4 (Unreleased)
* Expanded automated test coverage across distribution identities, sampling, vectorization, validation edges, median/ci, and repr behavior.
* Refactored initialization tests to a consistent pytest style with parametrized invalid-input cases.
* Updated `PERT.rvs` type hints to allow tuple-shaped `size` inputs (`int | tuple[int, ...]`).
* Updated lockfile versions.
* Updated the GitHub Actions pytest workflow configuration.

## v0.1.3 (2026-02-10)
* Cleanup type hints.
* Add first unit tests.
* Add first automated tests via actions.

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
