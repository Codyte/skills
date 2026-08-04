# Handoff · .agents/skills · 2026-08-03

## Goal
Elevate the `navindex` skill to state-of-the-art, then fix repo hygiene it exposed (nested repos
tracked as plain files instead of real submodules) and publish the parent repo publicly.

## State
- HEAD: 283b7e3 (after submodule conversion commit, pushed)
- Live state: parent repo now live at https://github.com/Codyte/skills (public, created this
  session via `gh repo create`). `origin` remote already points there.
- Done:
  - navindex.py: class-member symbol extraction (`.name` via member-indent rule, py+JS/TS), TS
    `interface`/`type`/`enum`/`class`, PS1 `class`, EOL preservation on rewrite (LF stays LF on
    Windows), `--install-hook` (pre-commit auto-refresh via `--auto`, worktree-aware via
    `git rev-parse --git-path hooks`), `scripts/test_navindex.py` (6 asserts, passing).
  - Docs (SKILL.md/README.md/references/internals.md) + evals/evals.json (3→7 cases) updated.
  - Rolled out navindex headers+maps+hook to `C:\Server` (master) and `C:\Server_Dev` (worktree,
    branch_geral) — both committed and pushed on their own remotes.
  - Converted navindex/caveman/handoff/ponytail from "nested .git present but parent tracks file
    contents as plain blobs" to real git submodules: `.gitmodules` + gitlink entries pinned to
    each repo's pushed HEAD. Verified with a local `--recurse-submodules` clone.
  - Created `https://github.com/Codyte/skills` (public) and pushed — this repo's old origin
    (same URL) had been 404ing; recreating it fixed that.
- In progress: nothing mid-flight. Session ended on user Q&A about submodule workflow (VS Code /
  GitHub Desktop / git CLI) — informational only, no further code change pending from it.

## Decisions (and why)
- Pre-commit hook over PostToolUse-on-Edit — one hook, zero per-edit churn, doesn't pollute
  in-progress diffs. Chosen over always-live refresh.
- Regex-based extraction kept (no tree-sitter) — zero-dep is the point of this skill; only 1
  nesting level (class members) added, deeper nesting (closures) intentionally skipped.
- Converted the 4 nested repos to *real* submodules rather than deleting their inner `.git` dirs
  (the cheaper option originally offered) — user picked "formalize as submodule" so each skill
  keeps its own remote/history, clone works with `--recurse-submodules`.
- Did **not** touch ~74 unrelated pre-existing dirty/staged paths in the parent repo (deletions
  from before this session, e.g. `caveman-compress/*`, `theme-factory/*`) — not mine, scoped every
  commit to only the paths this session's work touched.

## Next steps (ordered)
1. (optional) Resolve the ~74 unrelated pre-existing dirty/deleted paths in the parent repo (not
   from this session) — either commit, restore, or confirm intentional deletion. Not blocking.
2. (optional) Roll out navindex to any other active repos beyond `C:\Server` / `C:\Server_Dev`.
3. (optional) Watch for a real codebase hitting the known ceiling — multi-line JS/TS method
   signatures aren't extracted (`ponytail:` comment in navindex.py names this) — only upgrade to
   tree-sitter if that actually bites.

## Key files
- [navindex/scripts/navindex.py](navindex/scripts/navindex.py) — core extractor/builder, see its
  own NAV INDEX header for the symbol map
- [navindex/scripts/test_navindex.py](navindex/scripts/test_navindex.py) — self-check, run before
  any further navindex.py edit
- [.gitmodules](.gitmodules) — the 4 submodule registrations added this session
- `__navi__.md` (repo root) — folder map, regenerate after any structural change here

## Open / blockers
None.

## Skills
- navindex

## Effort
low for step 1 (if picked up) — mechanical git triage (commit/restore/confirm), no design
decision. Everything else is optional follow-up, not a blocker.
