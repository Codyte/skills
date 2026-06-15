# Swarm Orchestrator (v3.0)

**Location:** `~/.claude/skills/codyte-spawn-optimized-agents`

A universal, cross-tool **swarm orchestrator**. You give it a goal; it plans every sub-agent up
front, spawns them in parallel on **disjoint files** (no conflicts by construction), reads back only
concise results, and runs a final review pass — looping until the goal is done.

- **Cross-tool:** any orchestrator that can read/write files and run `claude -p` (Claude Code,
  Codex, Antigravity, scripts) can drive it. Subordinate agents spawn as `claude` for now;
  inside Claude Code the native Agent tool is used instead.
- **Isolation:** file partition — each agent owns an exclusive set of paths. No merge step.
- **No USD model:** accounting is by agent count, model tier, and test results — never invented dollars.
- **Cost levers (measured):** ~84% of CLI-spawn cost is cold-start cache, ~16% output. To spend
  less, prefer the native Agent tool > cheaper model > fewer agents > (last) minimize output.
  See [SKILL.md](SKILL.md#cost-levers-what-actually-moves-the-bill).

## Lifecycle

1. **PLAN** — decompose the goal, partition files, write one `plan.md` + `scope.txt` per agent.
   Run the conflict guard. *No spawning yet.*
2. **SPAWN** — launch agents in parallel (deps respected), each confined to its scope.
3. **COLLECT** — read only each agent's short `result.md`; continue until all sub-goals are done.
4. **REVIEW** — verify scope compliance + integration, run tests, fix, close the goal.

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Full operating model (the 4 phases, model selection, principles) |
| [PROTOCOL.md](PROTOCOL.md) | The file-based cross-tool contract: `.swarm/` layout, formats, spawn prompt, conflict guard |
| [QUICK_INVOKE.md](QUICK_INVOKE.md) | Cheat sheet |
| [profiles/codyte.md](profiles/codyte.md) | Codyte enforcement overlay (auto-loaded for `c:\Server_Dev`) |

## Run state

The swarm writes scratch under `.swarm/<run-id>/` in the project root. Keep `.swarm/` gitignored.

## Codyte mode

When the project root is `c:\Server_Dev`, [profiles/codyte.md](profiles/codyte.md) auto-loads and
adds mandatory review gates: tenant isolation, multi-unit entitlement, n8n webhook contracts, audit
trail, `/security-review` for public routes, and the standard test/smoke suites. The goal cannot
close until those pass. Source of truth for the rules: `c:\Server_Dev\CLAUDE.md`.
