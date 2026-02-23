# AGENTS.md

This file defines required behavior for coding agents working in this repository.
These instructions apply to the entire repo tree.

## 1) GitFlow Requirements (Mandatory)

- Follow GitFlow branch roles:
  - `main`: production-ready history only.
  - `dev`: integration branch for upcoming work.
  - `feature/*`: branch from `dev`, merge back into `dev`.
  - `release/*`: branch from `dev`, merge into `main` only.
  - `hotfix/*`: branch from `main`, merge into `main` only.
- Never commit directly to `main` or `dev`.
- Use pull requests for all merges.
- Create pull requests as draft PRs by default; do not create regular/open PRs unless explicitly instructed.
- Keep branches scoped to one purpose; avoid mixing unrelated changes.
- Keep commits scoped to one logical change whenever possible.
- Avoid mixing unrelated code, tests, docs, or config updates in a single commit unless they are required for one atomic change.
- Use semantic commit messages (Conventional Commits), for example:
  - `feat: ...`
  - `fix: ...`
  - `refactor: ...`
  - `chore: ...`
  - `ci: ...`
- CI trigger policy:
  - Do not run CI on `feature/*` push events.
  - Run CI on pull requests to `dev`/`main` only.

## 1.1) Semantic Versioning (Mandatory)

- Follow Semantic Versioning (`MAJOR.MINOR.PATCH`) for all release versions.
- Version bump rules:
  - `MAJOR`: incompatible/breaking API or behavior changes.
  - `MINOR`: backward-compatible feature additions.
  - `PATCH`: backward-compatible bug fixes or small internal corrections.
- Do not change version numbers arbitrarily; bump only when release scope warrants it.
- If release impact is unclear, ask the user which SemVer level should be applied.

## 2) Explicit-Instruction-Only Mode (Mandatory)

- Do not edit, create, rename, or delete any file unless the user explicitly asks for that action.
- Do not run any shell/system command unless the user explicitly asks for that command or explicitly asks you to perform an action that clearly requires commands.
- Do not infer permission from context, prior turns, or "best next step".
- If a request is ambiguous, ask a clarifying question before taking any action.
- Default behavior is read-only discussion and planning until explicit user direction is given.

## 3) Safety and Transparency

- Before any change, state exactly what you will do.
- For bug/failure remediation (for example CI/workflow errors), first explain the proposed fix and ask for explicit confirmation before making file edits.
- When changing GitHub Actions/workflow behavior, verify `AGENTS.md` policy text matches the realized workflow triggers and rules; if not aligned, update `AGENTS.md` in the same change.
- After any change, summarize exactly what changed and where.
- If requested action conflicts with these rules, ask for confirmation and explain the conflict.
