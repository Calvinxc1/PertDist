# PertDist
[![CI (main)](https://github.com/Calvinxc1/PertDist/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Calvinxc1/PertDist/actions/workflows/ci.yml?query=branch%3Amain)
[![Coverage (main)](https://codecov.io/gh/Calvinxc1/PertDist/branch/main/graph/badge.svg)](https://codecov.io/gh/Calvinxc1/PertDist/tree/main)

`PertDist` is a SciPy-style implementation of the [Beta-PERT distribution](https://en.wikipedia.org/wiki/PERT_distribution).

## Overview
The package exposes a `PERT` class with an API modeled after `scipy.stats` distributions. It supports scalar and array-based parameters and computes both distribution functions and descriptive statistics.

## Authorship And AI Usage
- Functional library code is authored manually.
- AI tooling may be used to assist with unit test authoring and documentation drafting/editing.

## Installation
```bash
pip install pertdist
```

## Python Version
- `Python >= 3.11`

## Quick Start
```python
from pert import PERT

dist = PERT(min_val=10, ml_val=190, max_val=200, lamb=4.0)

samples = dist.rvs(size=10_000, random_state=42)
mean = dist.mean
median = dist.median()
p90 = dist.ppf(0.90)
```

## Implemented API
### Constructor
- `PERT(min_val, ml_val, max_val, lamb=4.0)`

### Properties / Attributes
- `a`, `b`, `c`, `lamb`
- `alpha`, `beta`
- `mean`, `var`, `skew`, `kurt`
- `range` (property)

### Methods
- `median()`
- `rvs(size=1, random_state=None)` where `size` can be `int` or `tuple[int, ...]`
- `pdf(x)`, `logpdf(x)`
- `cdf(x)`, `logcdf(x)`
- `sf(x)`, `logsf(x)`
- `ppf(q)`, `isf(q)`
- `interval(alpha)`
- `ci(z)`
- `stats()`

## Input Validation
The constructor enforces:
- `lamb > 0`
- strict ordering for each element: `min_val < ml_val < max_val`
- no adjacent equal values (`min_val == ml_val` or `ml_val == max_val`)

## Testing
The project includes a pytest suite under `tests/`, including coverage for:
- initialization and validation
- distribution identities and boundary behavior
- sampling behavior and reproducibility
- vectorized inputs/outputs
- `median`, `ci`, and `__repr__`

Run tests with:
```bash
uv run pytest -q
```

## Roadmap
- Add additional SciPy-like analogues:
  - `moment`
  - `entropy`
  - `fit`
  - `expect`
  - `std`

## Version History
See `VersionHistory.md`.

## Contributing
Pull requests are welcome. Branching and contribution style can follow repository conventions.

## License
This project is licensed under the GNU GPL. See `LICENSE`.
