# Handoff · .agents/skills · 2026-08-04

## Goal
Split the `handoff` skill's memory into two levels — persistent project constraints vs
per-session state — so a constraint can no longer be lost by the copy-forward that carried it.

## State
- HEAD: 0a534f4 (parent) / 7373086 (handoff submodule) — all 4 submodule commits + their parent
  bumps pushed, `main...origin/main` clean.
- Live state: this repo now runs on the new format — `.handoff/standing.md` exists (2 entries,
  migrated) and `active.md` no longer carries the inline section. Boot injects both.
- Done:
  - `standing.md` (level 0): `standing_file()`, `migrate_standing()`, `standing_status()`,
    `STANDING_CAP=30`. Injected at boot ahead of the handoff and independently of it.
  - `--archive` lifts a legacy `## Standing decisions` section out on first run, then nudges to
    prune past the cap — at handoff time, never at boot (a boot warning would cost tokens/turn).
  - `legacy_note()`: one line at boot telling an agent resuming an old-format handoff what to do;
    two branches (no standing.md yet / stale duplicate). Self-extinguishing.
  - `--grep` now searches `standing.md` first, labelled LIVE — it is never archived, so a live
    constraint was the one thing the decision-finder could not find.
  - `boot_breakdown()` accounts standing.md in the boot floor.
  - Docs: SKILL.md (**Two levels** + **Resuming a handoff written in the old format**), README.md.
    Selftest extended (lift idempotency, archive can't eat level 0, grep reaches it, legacy_note
    both branches) — `--selftest` passes.
- In progress: nothing mid-flight.

## Decisions (and why)
- Two files, not one — the gain is the failure mode, not tokens: input cost is identical (same
  bytes injected), output saves only ~300-600 tok/handoff. What changes is that a file nobody
  rewrites cannot be silently reworded or dropped.
- Level 0 is **not** immutable and **not** "injected only once" — a SessionStart hook writes into
  the context, which is re-sent every turn. So it needs a cap (30 lines) and a retire rule, or it
  eats the very saving the skill exists to produce.
- Rejected `--init` / `--install`: `--ensure-hook` already is the install; an `--init` would create
  an empty scaffold that gets injected every turn and invites narrative. Create the file when a
  verdict actually binds.
- Boundary with `~/.claude/.../memory/`: memory = who the user is, cross-project. standing.md =
  constraints on this repo, versioned with it. A fact fitting both goes to memory.
- Corrected a claim the split invalidated ("the archive keeps retired entries") — post-migration a
  retired entry is in git (`git log -p .handoff/standing.md`); only pre-split inline sections are
  in `archive/`. Mattered because that guarantee is what makes pruning safe.

## Next steps (ordered)
1. (optional) Nothing pending on the skill. When another repo with an old-format handoff runs
   `/handoff`, the migration is automatic — no action needed here.
2. (optional) Resolve the ~74 unrelated pre-existing dirty/deleted paths in the parent repo (not
   from this session or the last) — commit, restore, or confirm intentional deletion.
3. (optional) Roll navindex out to repos beyond `C:\Server` / `C:\Server_Dev`.

## Key files
- [handoff/load_handoff.py](handoff/load_handoff.py) — level-0 functions at L108-L173; see its
  NAV INDEX header for the map
- [handoff/SKILL.md](handoff/SKILL.md) — "Two levels" + old-format resume guidance
- `.handoff/standing.md` — this repo's own level 0 (edit in place, never rewrite)

## Open / blockers
None.

## Skills
- navindex

## Effort
low para o passo 1 — não há trabalho pendente na skill; os passos 2 e 3 são triagem git mecânica
e rollout documentado. Suba para medium se mexer em `load_handoff.py` de novo: rode
`--selftest` antes e depois, é o que segura o parser de seções e a migração.
