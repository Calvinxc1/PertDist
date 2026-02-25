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
- Contribution scope:
  - Community contributors are welcome to propose changes through `feature/* -> dev` pull requests.
  - `release/*` and `hotfix/*` branches and pull requests are core-developer managed.
- Never commit directly to `main` or `dev`.
- Use pull requests for all merges.
- Create pull requests as draft PRs by default; this is a recommended default, not a mandatory enforcement. Developers may open regular/open PRs when they judge it appropriate.
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
- CD trigger policy:
  - Run release publish dry-run checks on pull requests to `main` from `release/*` or `hotfix/*`.
  - Run release/publish workflow only after merged pull requests to `main` from `release/*` or `hotfix/*`.
  - Run release recovery (yank/unyank verification) by manual dispatch only.

## 1.1) Semantic Versioning (Mandatory)

- Follow Semantic Versioning (`MAJOR.MINOR.PATCH`) for all release versions.
- Version bump rules:
  - `MAJOR`: incompatible/breaking API or behavior changes.
  - `MINOR`: backward-compatible feature additions.
  - `PATCH`: backward-compatible bug fixes or small internal corrections.
- Do not change version numbers arbitrarily; bump only when release scope warrants it.
- If release impact is unclear, ask the user which SemVer level should be applied.

## 1.2) Enforcement vs Discretion

- Policies enforced by branch protection and required status checks are mandatory controls.
- Policies not enforced by repository settings or workflows are guidance and may be overridden at developer discretion.
- Developers are expected to apply judgment and prefer the documented defaults unless there is a clear reason to deviate.

## 1.3) AI Usage Scope (Guidance)

- AI tooling may assist with test authoring, documentation drafting/editing, GitHub Actions/workflow authoring and maintenance, and development planning/decision support.
- Functional library code ownership and final responsibility remain with human developers.
- For developers, these are guidelines rather than hard rules; individual developers may override this guidance when they deem it appropriate.

## 2) Explicit-Instruction-Only Mode (Mandatory)

- Do not edit, create, rename, or delete any file unless the user explicitly asks for that action.
- Do not run any shell/system command unless the user explicitly asks for that command or explicitly asks you to perform an action that clearly requires commands.
- Do not infer permission from context, prior turns, or "best next step".
- Treat proposal-style language (for example: "how about", "what if", "should we", "would it make sense") as discussion by default, not execution permission.
- Treat question-form phrasing (for example: "can you", "could you", "is it possible to") as discussion by default, not execution permission.
- Treat declarative requirement statements (for example: "it should...", "the action should...", "this needs to...") as non-executable unless accompanied by a separate explicit execution cue.
- Require a separate explicit execution cue (for example: "implement this", "go ahead and make this change") before making changes after proposal/question discussion.
- For question-form prompts, do not execute edits or commands even if a task is described; require a follow-up explicit execution cue in a separate interaction.
- Before executing any change after proposal/question discussion, send a preflight confirmation message: "Execution confirmation required. No changes made yet."
- After an explicit execution cue is received, execute without requesting another confirmation unless requirements changed materially or became ambiguous.
- If a user message mixes question framing with an implied task, treat it as non-executable until explicit confirmation is received.
- If intent is ambiguous, ask a short confirmation question before making changes.
- If a request is ambiguous, ask a clarifying question before taking any action.
- Default behavior is read-only discussion and planning until explicit user direction is given.

## 3) Safety and Transparency

- Before any change, state exactly what you will do.
- For bug/failure remediation (for example CI/workflow errors), first explain the proposed fix and ask for explicit confirmation before making file edits.
- When changing GitHub Actions/workflow behavior, verify `AGENTS.md` policy text matches the realized workflow triggers and rules; if not aligned, update `AGENTS.md` in the same change.
- `uv.lock` is intentionally developer-local and not tracked in git for this repository. Do not commit it.
- Guardrails may be bypassed only after explicit user verification. This verification must be a separate interaction beyond the original action request, where the user explicitly confirms the bypass.
- Any bypass confirmation request must include a brief overview of the specific guardrail(s) being bypassed.
- After any change, summarize exactly what changed and where.
- If requested action conflicts with these rules, ask for confirmation and explain the conflict.
