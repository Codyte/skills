---
name: codyte-spawn-optimized-agents
version: "3.0.0-swarm"
description: |
  Universal swarm orchestrator. Decomposes a /goal (your command or a plan file) into
  isolated parallel sub-agents, spawns them without conflicts, collects concise feedback,
  and runs a final review pass — repeating until the goal is done.

  Cross-tool by design: any orchestrator that can read/write files and run `claude -p`
  (Claude Code, Codex, Antigravity, …) can drive the swarm. Subordinate agents are
  spawned as `claude` for now. Inside Claude Code the native Agent tool is used instead.

  Isolation is by FILE PARTITION: each sub-agent owns a disjoint set of files (its scope),
  so parallel work never collides — no merge step, no conflicts by construction.

  Lifecycle (always in this order):
  1. PLAN   — decompose the goal, partition files, write one action plan per agent. No spawning yet.
  2. SPAWN  — launch agents in parallel (deps respected), each confined to its file scope.
  3. COLLECT— read only the concise result of each agent (not full logs); continue until goal done.
  4. REVIEW — inspect the combined result for errors, run tests, fix, and close the goal.

  Auto-detects the Codyte repo (c:\Server_Dev) and loads profiles/codyte.md, which adds
  mandatory tenant isolation, multi-unit entitlement, n8n contracts, and audit-trail checks.

  Use when: a goal is large enough to split across parallel workers, you want plan-first /
  review-last discipline, or you need cross-tool agent spawning. Skip for single small edits.
color: purple
metadata:
  version: "3.0.0"
  role: "universal_swarm_orchestrator"
  isolation: "file-partition (disjoint scope per agent)"
  spawn: "auto-detect (native Agent tool in Claude Code; claude CLI otherwise)"
  cross_tool: ["claude-code", "codex", "antigravity", "claude-api"]
  profiles:
    - codyte (auto-loaded for c:\\Server_Dev)
  protocol_spec: "PROTOCOL.md"
  cheatsheet: "QUICK_INVOKE.md"
---

# Universal Swarm Orchestrator

You become the **orchestrator**: you plan the whole job up front, spawn isolated workers in
parallel, read back only their concise results, and review everything at the end. Workers never
touch the same files, so they cannot conflict. You keep going until the `/goal` is complete.

This file is the operating model. The exact on-disk file formats live in [PROTOCOL.md](PROTOCOL.md).
Codyte-specific enforcement lives in [profiles/codyte.md](profiles/codyte.md).

---

## Core principles

1. **Plan before you spawn.** Every sub-agent gets a written action plan *before* anything runs.
   No agent is launched until the full partition is computed and verified conflict-free.
2. **Isolation by file partition.** Each agent owns an exclusive set of paths (`scope.txt`).
   No path may appear in two scopes. Files everyone only reads go in `shared-read.txt`.
   Because writes never overlap, there is no merge step and no conflict.
3. **Efficient feedback.** Agents write a short `result.md` (what changed, files, tests, status,
   blockers). You read that — not their full transcripts. Verbose logs stay in `log.md`, opened
   only on error.
4. **Review last.** When all sub-goals report done, you run a combined review: scope compliance,
   integration between agents' work, build/tests. Errors → spawn a fix agent or loop. Only then
   is the goal closed.
5. **Honest accounting — real tokens, never invented.** Capture actual token usage per agent
   from the `claude -p --output-format json` result (`usage` block: input/output/cache tokens).
   Aggregate into a run total. Do not fabricate figures or savings %. See *Token accounting*.

---

## The four phases

### Phase 1 — PLAN (no spawning)

1. **Capture the goal.** Write the user's `/goal` (a one-liner command, or the contents/path of a
   plan file) into `.swarm/<run-id>/goal.md`.
2. **Decompose** into sub-goals with explicit dependencies. A sub-goal is a unit of work one
   agent can own end to end.
   - **Efficiency gate (Step A):** count independent slices. **1–2 or mostly-serial → do NOT
     swarm**; finish inline in this session and skip Phases 2–4. 3+ truly parallel slices → swarm.
     See *Efficiency engine*.
3. **Partition files.** For each sub-goal, list the exact files it will create or modify into
   `agents/NN-<slug>/scope.txt`. Then run the **conflict guard**:
   - Build a map `path → agent`. If any path is claimed by more than one agent → **STOP**.
     Either merge those sub-goals into one agent, or add a dependency so they run in sequence
     (the second agent inherits the first's output as read-only context).
   - Files read by many but written by none go in `.swarm/<run-id>/shared-read.txt`.
4. **Write one action plan per agent** (`agents/NN-<slug>/plan.md`): objective, the files it owns,
   step-by-step instructions, what "done" looks like, and what it must NOT touch.
5. **Allocate models via the Efficiency engine** (Steps B + C): pick the orchestrator's model by
   goal size, and each worker's model by slice difficulty. Record each worker's tier in `status.json`.
6. **Write `master-plan.md`**: sub-goal list, dependency graph, agent→scope map, spawn order, and
   the **efficiency decision** (swarm yes/no, orchestrator tier, per-worker tiers + one-line rationale).

> Gate: do not enter Phase 2 until every agent has `plan.md` + `scope.txt`, and the conflict
> guard reports zero overlapping paths.

### Phase 2 — SPAWN (parallel, isolated)

Spawn every agent whose dependencies are satisfied, in parallel. Auto-detect the mechanism:

- **Orchestrator is Claude Code (you, here):** use the native **Agent** tool with
  `run_in_background: true`, one call per agent. Pass the agent its `plan.md` path and its
  `scope.txt`. File partition already guarantees no collision, so worktrees are not required;
  use `isolation: "worktree"` only if you deliberately allow two agents to share a file.
- **Orchestrator is another tool (Codex, Antigravity, scripts):** shell out per agent:
  ```
  claude --dangerously-skip-permissions --model <tier> -p "<spawn prompt: read .swarm/<run-id>/agents/NN/plan.md and scope.txt; work ONLY within scope; write result.md and set status.json=done|error when finished>"
  ```

Each agent must: read its `plan.md` + `scope.txt`, work **only** within its scope, set
`status.json.state=running` at start, then write `result.md` and `status.json.state=done`
(or `error` with the reason) at the end. See [PROTOCOL.md](PROTOCOL.md) for exact formats.

**Warm-start every worker — do NOT let it explore cold.** A freshly spawned agent knows nothing
beyond its prompt; left alone it re-greps the repo and burns tokens rediscovering what's already
written down. So the spawn prompt MUST instruct the worker, before any wide search, to read (in
this order, only what exists and is relevant to its scope):
1. the project memory index (`MEMORY.md`) — durable, non-obvious facts and prior fixes;
2. the `__navi__.md` of each folder in its scope — the symbol→line map (one read replaces opening
   N files); regenerate it after structural changes (`python scripts/navindex_main.py <folder> --map-only`);
3. the most recent `docs/pendencias-*.md` — current open work and constraints.
Then: **do not re-explore what those already establish.** This mirrors the human's own
session-bootstrap discipline and is the single biggest token saver for cold workers. (Recalled
memories describe what was true when written — verify a named file/flag still exists before relying on it.)

### Phase 3 — COLLECT (until goal done)

- Poll `status.json` for each agent (in Claude Code, background-agent completions notify you).
- When an agent finishes, read **only** its `result.md`. Do not pull its full log unless its
  state is `error`.
- As dependencies clear, spawn the next wave (back to Phase 2 for those agents).
- Continue until every sub-goal is `done`. If any agent reports `error`, decide: re-plan that
  slice, spawn a fix agent, or escalate to the user.

### Phase 4 — REVIEW (close the goal)

1. **Scope compliance:** verify each agent only changed files in its `scope.txt` (e.g. inspect
   the diff / `git status`). A change outside scope is a defect — flag it.
2. **Integration:** check the seams between agents' work (shared interfaces, imports, contracts).
3. **Build & test:** run the project's checks. In Codyte mode, run the mandatory suites from the
   profile.
4. Write `review.md`: what passed, what failed, follow-ups. If anything failed, loop back with a
   targeted fix agent. Only when review is clean is the `/goal` complete.

---

## Token accounting (real, per-agent + total)

Token counts are captured from the runtime, not estimated — but only the **CLI spawn path**
exposes them per agent:

- **CLI subordinates (`claude -p --output-format json`):** the JSON result carries a `usage`
  block with real `input_tokens`, `output_tokens`, `cache_creation_input_tokens`,
  `cache_read_input_tokens` (plus `num_turns` and `total_cost_usd`). The orchestrator writes this
  to `agents/NN/usage.json` and sums all agents into `usage-total.json`. See [PROTOCOL.md](PROTOCOL.md).
- **Native Agent tool (Claude Code in-process):** the tool result does **not** return a usage
  breakdown, so per-agent token counts are not programmatically available. Only the session total
  is observable (via `/cost`, or OpenTelemetry if enabled).

Tradeoff to be aware of: each `claude -p` cold-starts and reloads the full system prompt/context,
charged as `cache_creation_input_tokens` (tens of thousands of tokens **per spawn**). The native
Agent tool avoids this (warm cache) but gives no per-agent numbers. So:

- Need **precise per-agent token accounting** → spawn via CLI (accept the per-spawn cold-start cost).
- Native Agent tool → per-agent accounting is intentionally skipped (not needed); rely on the
  session total via `/cost`. This is the cheaper default when you don't need a per-agent breakdown.

Report **tokens only** (USD omitted by preference — `total_cost_usd` is present in the same JSON if
ever needed). Never invent values.

## Cost levers (what actually moves the bill)

Measured on real runs: in **CLI-spawn mode the cost is ~84% cold-start cache** (`cache_read` +
`cache_creation` that every `claude -p` pays to reload the system prompt/tools/context) and only
**~16% output**. So minimizing output — the instinct from older "output is 5×" advice — optimizes
the *smallest* slice. Order the levers by real impact:

1. **Avoid the cold-start: use the native Agent tool when the orchestrator is Claude Code.** Each
   `claude -p` re-loads ~450–525k cache tokens *per spawn*. The native tool reuses the warm cache
   and eliminates almost all of it. **Biggest lever by far.** Cost of choosing it: no per-agent
   token breakdown (the documented tradeoff).
2. **Pick the cheapest model that fits.** Measured: Haiku ≈ 3.7× cheaper than Sonnet for
   comparable summarization. Haiku for mechanical agents; Sonnet for real implementation.
3. **Fewer, larger agents.** Every spawn pays the fixed cold-start once — two agents = two
   cold-starts. Don't over-partition a small goal.
4. **Then minimize output.** Real, but the smallest share in spawn mode.

Rule of thumb: per-agent token accounting (CLI) is a *paid feature* — use it when you need
cross-tool isolation or a cost audit; otherwise default to the native tool.

## Efficiency engine (model allocation — MANDATORY, decided in Phase 1)

This is the skill's self-contained decision procedure for spending the least compute on a goal.
Run it in Phase 1, **before partitioning**, and record the outcome in `master-plan.md`. It decides
three things: (A) whether to swarm at all, (B) the orchestrator's model, (C) each worker's model.
Optimize total cost, remembering that in CLI-spawn mode ~84% of the bill is cold-start cache.

### Step A — Swarm, or not?
Count the **independent** sub-goals (slices) and whether they can truly run in parallel.
- **1–2 slices, or slices that mostly serialize → DON'T swarm.** Do it inline in one session
  (Sonnet by default; Opus only if the task is genuinely hard). Spawning would pay cold-start
  overhead that exceeds any parallelism gain. *The cheapest swarm is often no swarm.*
- **3+ genuinely independent slices → swarm.**

### Step B — Orchestrator model (strong by default — one stream, high leverage)
The orchestrator is a **single** token stream whose plan + review multiply across every worker, so
invest here. A planning error wastes N workers; review quality is what makes the swarm trustworthy.
Scale by goal size:

| Goal size (independent slices) | Orchestrator |
|---|---|
| tiny (1–2) | — (inline, no orchestrator) |
| small (3–5) | **Sonnet** |
| medium (5–12) | **Sonnet**, or **Opus** if slices are coupled / scope is ambiguous |
| large (12+, coupled) | **Opus** |

### Step C — Worker model per slice (cheap by default — scale up only for hard slices)
Decide per agent by **where the difficulty lives**:

| Slice nature | Worker |
|---|---|
| mechanical, single-file, spec is exact | **Haiku** |
| real implementation, refactor, tests, logic | **Sonnet** |
| genuinely hard (tricky algorithm/design inside the slice) | **Opus** (rare) |

### The shape, in one line
**Strong brain plans + reviews; cheap hands execute. Opus-over-Haiku, never Haiku-over-Opus.**
Under-investing where decisions fan out and over-investing where they don't is the worst
allocation. A strong worker cannot rescue a weak plan; a strong plan makes cheap workers
productive. The bigger and more coupled the project, the more an Opus orchestrator pays for
itself — because complexity migrates into planning and review, which is the orchestrator's job.

### Cost reality check (apply in this order)
Worker-model downgrade saves ~3.7× on the *reasoning* portion, but the per-spawn cold-start
(~84% of CLI cost) dominates. So rank cost moves: **(1) fewer, larger agents > (2) native Agent
tool over CLI (when you don't need per-agent accounting) > (3) cheaper worker model > (4) less
output.** See *Cost levers*. Picking a cheaper worker while spawning ten tiny CLI agents is
optimizing the wrong thing.

---

## Forbidden autonomous actions (workers AND orchestrator)

Some actions are **never** taken autonomously by a spawned worker or by the orchestrator mid-run —
no matter what the goal says. They are downgraded to a **proposal** written into `review.md`
(section `## Proposed actions requiring human approval`), with the exact command, and left for the
human to run. A goal that demands one of these is **not** "failed" — it completes everything else
and surfaces the gated step.

| Action | Why gated | What the agent does instead |
|---|---|---|
| **Deploy to prod** (`docker compose -p server … up/build`, anything against `c:\Server`/master) | The owner's standing rule: deploy only with explicit confirmation; prod broke 3× from bad deploys | Stage commits on `branch_geral`; write the exact deploy command to `review.md` as a proposal |
| **File deletion** (`rm`, `Remove-Item -Recurse`, `git rm`) | Irreversible; "remove the junk" must be reviewed, not guessed | Produce a **triage list** (candidate → reason), never delete. Mirror the docs-triage pattern |
| **Destructive git** (`reset --hard`, `push --force`, branch delete) | Data loss | Propose; never execute |
| **Destructive SQL** (`DROP`, mass `DELETE`, `ALTER COLUMN`, `TRUNCATE`) | Permanent data loss | Propose with the statement; never execute |
| **Secrets / auth / prod `.env`** (`JWT_SECRET`, `OPENAI_API_KEY`, role/RBAC logic, `users_role_check`) | Can lock out accounts or leak; one such change silently locked the master account out this month | Propose the diff; flag for human + `/security-review` |
| **External publish** (deploy hooks, sending data to third-party services) | Outward-facing, hard to reverse | Propose |

Safe to do autonomously: edit dev files in `c:\Server_Dev`, `git add`/`commit` on `branch_geral`
(never push to prod), `docker build`/local smokes, `py_compile`, run tests, regenerate `__navi__.md`,
write triage/proposal docs.

> If the goal is "clean up / remove junk / refactor + deploy": the swarm does the cleanup-as-**proposal**,
> the refactor + commits for real, and writes the deploy as a proposal. It never deploys or deletes itself.

## Running unattended (overnight) — notification + permissions

When the human will be away (e.g. asleep) and wants the swarm to run for hours:

1. **Notify on stop.** There is no "I'm done" env var; a finished turn is just silence. To get a
   signal, configure a `Stop` hook in `settings.json` (e.g. write a sentinel file / play a sound /
   desktop notify). Also enable Claude Code desktop notifications so a *blocked* agent (waiting on a
   permission) alerts the human instead of hanging silently till morning.
2. **Pre-approve permissions** so workers don't stall on prompts — but ONLY for the *safe*
   operations above. Never pre-approve anything in *Forbidden autonomous actions*; those must stay
   gated so the worst case overnight is "did less", never "deployed/deleted something wrong".
3. **Bound the run.** Set a max wave count / wall-clock budget in `master-plan.md`; if unmet, stop
   and write what remains to `review.md` rather than looping forever (burning tokens).

## Anti-patterns

- ❌ Spawning before all plans are written and the conflict guard passes.
- ❌ Deploying, deleting, or running destructive git/SQL autonomously — see *Forbidden actions*; propose instead.
- ❌ Two agents owning the same file (causes the exact conflict we're avoiding).
- ❌ Reading full agent transcripts when `result.md` would do.
- ❌ Closing the goal without the Phase-4 review and tests.
- ❌ Inventing USD costs or savings percentages — report agent count, model tiers, test results.
- ❌ Cutting output first to save money — in spawn mode that's the smallest lever (~16%); kill
  cold-starts first (prefer the native Agent tool, cheaper models, fewer agents). See *Cost levers*.
- ❌ Spawning many tiny CLI agents for a small goal — each pays a full cold-start; consolidate.
- ❌ In Codyte mode: skipping the profile's mandatory checks (tenant isolation, audit trail, etc.).

---

## Setup note

The swarm writes scratch state under `.swarm/` in the project root. Add `.swarm/` to the project
`.gitignore` so run state (which can reference plans and outputs) is never committed.

---

## Profiles

- **Codyte** ([profiles/codyte.md](profiles/codyte.md)) — auto-load when the project root is
  `c:\Server_Dev`. Adds mandatory tenant isolation, multi-unit entitlement, n8n webhook
  contracts, audit-trail completeness, and security review for public routes. These become
  required Phase-4 review gates.
- **Generic** — any other project. Core lifecycle only; no Codyte constraints.
