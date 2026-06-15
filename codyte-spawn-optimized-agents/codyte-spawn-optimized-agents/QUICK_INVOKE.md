# Quick Invoke — Swarm Orchestrator

TL;DR: give a goal → orchestrator plans every agent → spawns them in parallel on disjoint files →
reads short results → reviews and closes.

---

## Invoke (inside Claude Code)

Just state the goal after the skill is active:

```
/goal "Add semantic search to the conversation detail endpoint"
```

The orchestrator will: write `.swarm/<run-id>/`, decompose into sub-goals, partition files,
write a `plan.md` per agent, spawn them (native Agent tool, in background), collect each
`result.md`, then review.

## Invoke (from another tool: Codex, Antigravity, scripts)

The orchestrator follows [PROTOCOL.md](PROTOCOL.md) and spawns each sub-agent as:

```bash
claude --dangerously-skip-permissions --model <haiku|sonnet|opus> -p "
You are sub-agent <NN-slug> in a swarm.
Read .swarm/<run-id>/agents/<NN-slug>/plan.md and scope.txt.
Modify ONLY files in scope.txt. Write result.md and set status.json=done when finished.
Execute now."
```

---

## Efficiency engine — who runs which model

**Shape: strong brain plans, cheap hands execute. Opus-over-Haiku, never the reverse.**

First decide **swarm or not**: 1–2 independent slices (or mostly serial) → don't swarm, do it
inline. 3+ truly parallel → swarm.

**Orchestrator** (one stream, high leverage — scale by goal size):

| Goal size (slices) | Orchestrator |
|---|---|
| tiny (1–2) | — inline, no orchestrator |
| small (3–5) | sonnet |
| medium (5–12) | sonnet, or opus if coupled/ambiguous |
| large (12+, coupled) | opus |

**Workers** (cheap by default — by slice difficulty):

| Slice | Worker |
|---|---|
| mechanical, single-file, exact spec | haiku |
| real implementation / tests / logic | sonnet |
| genuinely hard algorithm/design | opus (rare) |

Cost order that matters most: fewer/larger agents > native tool over CLI > cheaper worker > less output.

---

## The one rule that prevents conflicts

Every agent owns a **disjoint** set of files (`scope.txt`). Before spawning, the orchestrator runs
the **conflict guard**: no path may appear in two scopes. If it does → merge the agents or sequence
them. Parallel agents therefore never write the same file → no merge, no conflict.

---

## What you get back

```
.swarm/<run-id>/master-plan.md       # the plan
.swarm/<run-id>/agents/NN/result.md  # per-agent concise feedback
.swarm/<run-id>/agents/NN/usage.json # per-agent REAL token counts (CLI spawn)
.swarm/<run-id>/usage-total.json     # aggregated tokens across all agents
.swarm/<run-id>/review.md            # final review: scope, integration, tests, tokens, verdict
```

Goal is complete only when `review.md` says GOAL COMPLETE.

## Token accounting

Real per-agent + total token counts come from `claude -p --output-format json` (the `usage`
block: input / output / cache-creation / cache-read). The orchestrator writes `usage.json` per
agent and sums into `usage-total.json`.

- Native Agent tool path (in-process Claude Code) does **not** expose per-agent tokens — only the
  session total via `/cost`. For precise per-agent numbers, spawn via the CLI path.
- Caveat: every `claude -p` cold-starts and reloads context (~tens of thousands of
  `cache_creation` tokens **per spawn**). That's the real cost of cross-tool/CLI isolation.

## Cost levers (measured — order by impact)

In CLI-spawn mode ~84% of the bill is cold-start cache and only ~16% is output. So to spend less:

1. **Use the native Agent tool** (Claude Code) — kills the per-spawn cold-start. Biggest win.
2. **Cheaper model** — Haiku ≈ 3.7× cheaper than Sonnet for comparable work.
3. **Fewer, larger agents** — each spawn pays the cold-start once; don't over-split.
4. **Then** minimize output — smallest lever in spawn mode.

CLI per-agent accounting is a paid feature; use it for cross-tool isolation or a cost audit, else
default to the native tool.

---

## Codyte projects (c:\Server_Dev)

[profiles/codyte.md](profiles/codyte.md) auto-loads and adds mandatory review gates: tenant
isolation, multi-unit entitlement, n8n contracts, audit trail, `/security-review` for public
routes, and the standard test suites. The goal can't close until those pass.

## More

- [SKILL.md](SKILL.md) — full operating model
- [PROTOCOL.md](PROTOCOL.md) — exact file formats + spawn contract
- [profiles/codyte.md](profiles/codyte.md) — Codyte enforcement overlay
