# PertDist
[![CI (main)](https://github.com/Calvinxc1/PertDist/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Calvinxc1/PertDist/actions/workflows/ci.yml?query=branch%3Amain)
[![PyPI version](https://img.shields.io/pypi/v/pertdist.svg)](https://pypi.org/project/pertdist/)

`PertDist` is a SciPy-style implementation of the [Beta-PERT distribution](https://en.wikipedia.org/wiki/PERT_distribution).

## Overview
The package exposes a `PERT` class with an API modeled after `scipy.stats` distributions. It supports scalar and array-based parameters and computes both distribution functions and descriptive statistics.

## Installation
```bash
pip install pertdist
```

## Python Version
- `Python >= 3.11`

## Support
- Supported Python: `3.11+`
- Primary package index: [PyPI (`pertdist`)](https://pypi.org/project/pertdist/)

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
The project includes a pytest suite under [`tests/`](tests/), including coverage for:
- initialization and validation
- distribution identities and boundary behavior
- sampling behavior and reproducibility
- vectorized inputs/outputs
- `median`, `ci`, and `__repr__`

Run tests with:
```bash
uv run pytest -q
```

## Development Setup
Install development dependencies:
```bash
uv sync --all-extras --dev
```

Run lint and tests:
```bash
uv run ruff check .
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
See [`VersionHistory.md`](VersionHistory.md).

## Contributing
- Community and core-developer contribution workflow is documented in [`CONTRIBUTING.md`](CONTRIBUTING.md).
- Repository guardrails and policy details are defined in [`AGENTS.md`](AGENTS.md).

## Release Process (High-Level)
- Pull requests from `release/*` and `hotfix/*` into `main` run publish dry-run checks.
- Merged `release/*` / `hotfix/*` PRs to `main` trigger publish, tagging, release metadata, and post-release verification workflows.
- Recovery actions (including yank/unyank verification with runbook guidance) are run manually when needed.

## Reporting Issues
- Bug reports and feature requests: [GitHub Issues](https://github.com/Calvinxc1/PertDist/issues)
- Security-sensitive concerns can be reported privately using GitHub repository security reporting.

## Repository Policy
High-level development policy summary (full details in [`AGENTS.md`](AGENTS.md)):
- GitFlow is used: `feature/* -> dev`, `release/*|hotfix/* -> main`, with PR-based merges.
- Community contributions are welcome through `feature/* -> dev` pull requests; `release/*` and `hotfix/*` flows are core-developer managed.
- CI runs on PRs to `dev` and `main`; release dry-runs run on `release/*`/`hotfix/*` PRs to `main`; release publish runs after merge to `main`.
- Semantic Versioning is required (`MAJOR.MINOR.PATCH`) and versioning must be intentional.
- Some defaults are guidance (for example draft PR by default) and developer discretion is explicitly supported.
- `uv.lock` is developer-local and is not tracked in this repository.
- Functional library code is authored manually.
- AI tooling may assist with test authoring, documentation drafting/editing, GitHub Actions/workflow authoring and maintenance, and development guidance for planning/decision support.

For release notes and historical change context, see [`VersionHistory.md`](VersionHistory.md).

## License
This project is licensed under the GNU GPL. See [`LICENSE`](LICENSE).
