# Swarm Protocol — file-based, cross-tool

This is the contract every orchestrator and sub-agent follows. It is **filesystem-only** plus the
ability to run `claude -p`, so any tool (Claude Code, Codex, Antigravity, plain scripts) can act as
orchestrator or subordinate. Nothing here depends on a specific tool's internal APIs.

---

## Run directory layout

Everything for one orchestration run lives under `.swarm/<run-id>/` at the project root.

`run-id` = `<UTC-timestamp>-<goal-slug>`, e.g. `20260530-143500-add-memory-search`.

```
.swarm/<run-id>/
  goal.md            # INPUT: the /goal (command text, or contents/path of a plan file)
  master-plan.md     # orchestrator's decomposition: sub-goals, deps, agent→scope map, spawn order
  shared-read.txt    # files all agents may READ but none may WRITE during the run (one path per line)
  agents/
    01-<slug>/
      plan.md        # this agent's action plan (written BEFORE spawn)
      scope.txt      # exact file paths this agent may CREATE/MODIFY (one per line) — exclusive
      status.json    # lifecycle state (see schema)
      result.md      # OUTPUT: concise feedback the orchestrator reads
      usage.json     # OUTPUT: real token usage for this agent (CLI spawn only)
      log.md         # OPTIONAL verbose log; read by orchestrator only when state=error
    02-<slug>/
      ...
  usage-total.json   # OUTPUT: aggregated token usage across all agents
  review.md          # OUTPUT: Phase-4 review result
```

`.swarm/` MUST be gitignored.

---

## File formats

### goal.md
Free text. The user's command verbatim, or the plan-file contents (or an absolute path to it).

### master-plan.md
```markdown
# Goal
<one-line restatement>

## Sub-goals
- SG1 (agent 01): <what> — owns: <files>
- SG2 (agent 02): <what> — owns: <files>
- ...

## Dependencies
SG1 -> SG3        # SG3 starts only after SG1 is done
SG2 (parallel)

## Spawn order / waves
Wave 1: 01, 02    # no deps
Wave 2: 03        # after 01

## Efficiency decision (from the Efficiency engine)
Swarm: yes (4 independent slices)
Orchestrator: opus (large, coupled)
Workers: 01=sonnet (logic), 02=haiku (mechanical), 03=haiku (docs)
Rationale: planning/review complexity is high; only slice 01 needs design judgement.

## Conflict guard
PASS — no path appears in more than one scope.
```

### scope.txt
One repo-relative path per line. These are the **only** files the agent may write. No globs that
overlap another agent's scope. Example:
```
backend/src/routes/memory_search.py
backend/test_memory_search.py
```

### status.json
```json
{
  "agent": "01-memory-route",
  "model": "sonnet",
  "state": "pending",
  "deps": [],
  "started_at": null,
  "finished_at": null
}
```
`state` ∈ `pending` → `running` → `done` | `error`. The agent updates this file itself.

### usage.json  (real tokens — CLI spawn path)
The `usage` block copied verbatim from the agent's `claude -p --output-format json` result,
plus a couple of top-level fields. Written by the orchestrator after the agent finishes.
```json
{
  "agent": "01-memory-route",
  "model": "sonnet",
  "num_turns": 3,
  "input_tokens": 1240,
  "output_tokens": 2310,
  "cache_creation_input_tokens": 45202,
  "cache_read_input_tokens": 18800
}
```
> Tokens only — USD is omitted by preference (`total_cost_usd` exists in the raw JSON if ever needed).
> Native Agent tool path: per-agent accounting is intentionally skipped; leave `usage.json` absent
> and note "native-tool: per-agent tokens not tracked" in `result.md`.

### usage-total.json  (aggregate)
```json
{
  "agents": 3,
  "spawn_path": "cli",
  "input_tokens": 4100,
  "output_tokens": 6730,
  "cache_creation_input_tokens": 135606,
  "cache_read_input_tokens": 51200,
  "total_tokens": 197636,
  "per_agent": ["01-memory-route", "02-tests", "03-docs"]
}
```
`total_tokens` = input + output + cache_creation + cache_read, summed across agents. Tokens only —
no USD.

### result.md  (keep it short — this is what the orchestrator reads)
```markdown
## Result: 01-memory-route — DONE
- Changed: backend/src/routes/memory_search.py (new), backend/test_memory_search.py (new)
- Did: added GET /conversations/{id}/search with tenant filter; 4 unit tests
- Tests: `pytest test_memory_search.py` → 4 passed
- Stayed in scope: yes
- Blockers: none
```
On failure:
```markdown
## Result: 01-memory-route — ERROR
- Reason: <one line>
- See log.md for detail
- Partial changes left in: <files, or "reverted">
```

### review.md
```markdown
# Review — <run-id>
- Scope compliance: PASS/FAIL (any agent that wrote outside scope.txt)
- Integration: <seams checked, e.g. import wiring, shared schemas>
- Build/tests: <commands run + outcomes>
- Codyte gates (if profile active): tenant isolation / audit trail / security review …
- Tokens: total <N> (in <i> / out <o> / cache-create <cc> / cache-read <cr>); see usage-total.json
  - 01-memory-route: <tokens>  · 02-tests: <tokens>  · 03-docs: <tokens>
- Verdict: GOAL COMPLETE / NEEDS FIX
- Follow-ups: <fix agents spawned, or none>
```

---

## Spawn prompt (CLI subordinates)

When the orchestrator is **not** Claude Code, spawn each agent like this. Use
`--output-format json` so the run returns a real `usage` block to capture:

```bash
claude --dangerously-skip-permissions --model <tier> --output-format json -p "
You are sub-agent <NN-slug> in a swarm.
Read your plan:  .swarm/<run-id>/agents/<NN-slug>/plan.md
Read your scope: .swarm/<run-id>/agents/<NN-slug>/scope.txt
Read-only context (do NOT modify): .swarm/<run-id>/shared-read.txt

Rules:
- Modify ONLY files listed in scope.txt. Touching anything else is a failure.
- Set status.json state to 'running' when you start.
- When finished, write result.md (concise) and set status.json state to 'done' (or 'error' + reason).
- Keep result.md short; put verbose detail in log.md.

Execute now.
"
```

**Capturing tokens:** the agent's stdout is a single JSON object. The orchestrator parses its
`usage` block and writes `agents/<NN-slug>/usage.json` (see format above). Use whatever JSON
parser the orchestrator has — do not assume `jq` is installed.

PowerShell (Windows / this environment):
```powershell
$dir = ".swarm/<run-id>/agents/<NN-slug>"
$out = claude --dangerously-skip-permissions --model <tier> --output-format json -p "<spawn prompt>"
$r = $out | ConvertFrom-Json
[pscustomobject]@{
  agent = "<NN-slug>"; model = "<tier>"; num_turns = $r.num_turns
  input_tokens = $r.usage.input_tokens; output_tokens = $r.usage.output_tokens
  cache_creation_input_tokens = $r.usage.cache_creation_input_tokens
  cache_read_input_tokens = $r.usage.cache_read_input_tokens
} | ConvertTo-Json | Set-Content "$dir/usage.json"
```
POSIX with `jq` (if available): `echo "$out" | jq '{num_turns}+.usage' > "$dir/usage.json"`.

When the orchestrator **is** Claude Code, skip the CLI: use the native Agent tool with
`run_in_background: true`, one call per agent, passing the same plan/scope paths and rules in the
prompt. File partition already prevents collisions, so a worktree is optional. **Note:** the native
Agent tool does not return a per-agent `usage` block, so `usage.json` cannot be produced this way —
only the session total is observable (`/cost`). If you need per-agent token accounting, spawn via
the CLI path even inside Claude Code.

---

## Token aggregation (Phase 3 → 4)

After all agents finish, sum every `agents/*/usage.json` into `usage-total.json`:
- add up `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`
- `total_tokens` = the sum of all four, across all agents
- tokens only — do not report USD

Surface the totals (and the per-agent table) in `review.md` so the goal closes with real numbers.

---

## Conflict guard (the rule that prevents crossing)

Before spawning, the orchestrator computes the union of all `scope.txt` files:

1. Collect every path across all agents' `scope.txt`.
2. If any path appears for two or more agents → **the partition is invalid**. Resolve by either:
   - merging those sub-goals into a single agent, or
   - adding a dependency edge so they run sequentially (the later agent gets the earlier's files
     as read-only context, not as its own writable scope).
3. Record `Conflict guard: PASS` in `master-plan.md` only after step 2 yields zero overlaps.

This is what guarantees "sem se cruzarem": parallel agents write disjoint files, so there is
nothing to merge and nothing to conflict.

---

## Orchestrator loop (pseudocode)

```
write goal.md
decompose -> sub-goals, deps
for each sub-goal: write plan.md + scope.txt, choose model tier, status=pending
run conflict guard; if fail -> re-partition
write master-plan.md, shared-read.txt

while any agent not done:
    for each pending agent whose deps are all done:
        spawn (native Agent tool OR claude CLI), status=running
    wait for completions (notifications or poll status.json)
    for each finished agent:
        read result.md (read log.md only if error)
        if CLI spawn: write usage.json from the agent's JSON `usage` block
    if error: re-plan slice / spawn fix agent / escalate

# Phase 4
sum agents/*/usage.json -> usage-total.json   # real per-agent + total tokens
verify each diff ⊆ its scope.txt
check integration seams
run build/tests (+ Codyte gates if profile active)
write review.md (include token totals + per-agent table)
if NEEDS FIX: spawn targeted fix agent and re-review
else: GOAL COMPLETE
```
