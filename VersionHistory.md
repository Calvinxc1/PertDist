# Version History

## v0.1.5 (2026-02-26)
* Removed push-based execution from `.github/workflows/ci.yml`; CI now runs on pull requests to `dev`/`main` only.
* Fixed release publish dry-run behavior by removing offline publishing and requiring trusted publishing (`id-token: write` and `uv publish --trusted-publishing always --dry-run ...`).
* Updated `AGENTS.md` guardrails to require draft PRs by default, require explicit confirmation before CI/workflow failure-remediation edits, and keep workflow trigger policy text aligned with implemented Actions behavior.
* Added release orchestration, version-integrity, and recovery workflows for merged `release/*`/`hotfix/*` PRs to `main`, including post-release package verification and recovery runbook guidance.
* Extended release PR publish dry-run checks to both `release/*` and `hotfix/*` branches.
* Switched to developer-local `uv.lock` handling by removing lockfile tracking from CI expectations and updating repository policy accordingly.
* Added a non-blocking policy-drift warning workflow that flags possible documentation drift when `AGENTS.md` changes and performs lightweight contributor-doc anchor checks.
* Hardened release recovery issue handling by ensuring the `release` label when possible and falling back to unlabeled advisory issue creation when label setup is unavailable.
* Expanded project documentation and package metadata: improved README contributor/release process guidance, added `CONTRIBUTING.md`, and enriched `pyproject.toml` metadata for package publishing/discoverability.
* Hardened post-release package verification by adding bounded retry/backoff when installing `pertdist==$VERSION` in `.github/workflows/deploy-on-main-merge.yml`, reducing false failures caused by package-index propagation delays.
* Fixed `PERT` finite-input validation to correctly reject non-finite values while remaining safe for vectorized NumPy inputs.
* Added regression coverage for non-finite constructor inputs in `tests/test_validation_edges.py`.
* Removed unused runtime dependency `pydantic` from `pyproject.toml`.

## v0.1.4 (2026-02-19)
* Expanded automated test coverage across distribution identities, sampling, vectorization, validation edges, median/ci, and repr behavior.
* Refactored initialization tests to a consistent pytest style with parametrized invalid-input cases.
* Updated `PERT.rvs` type hints to allow tuple-shaped `size` inputs (`int | tuple[int, ...]`).
* Updated lockfile versions.
* Updated the GitHub Actions pytest workflow configuration.
* Refreshed README and release notes content to match current API, testing coverage, and development workflow.

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
