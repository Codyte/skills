---
name: onecall
description: Plan shell discovery as dependency layers and run one bounded call per layer, instead of one command per question. Every round-trip re-reads the whole context window, so fewer, fuller calls keep a session fresh for longer. Use whenever you are about to run several greps, reads, git or status commands in a row, explore an unfamiliar area, or when the onecall hook reports an overflow, a near-cap result, or a streak of small single-piece calls. Includes a transcript audit and a reproducible A/B experiment.
---

<!-- ====================== BEGIN NAV INDEX ====================== -->
<!-- NAV INDEX — auto-generated symbol map (refresh via the navindex skill) -->
<!--   L22     196B  onecall — one call per dependency layer -->
<!--   L27     825B  Why -->
<!--   L46     2.6K  The method -->
<!--   L80     911B  The cap -->
<!--   L97     1.2K  Tools -->
<!--   L114    389B  What this does not change -->
<!-- ======================= END NAV INDEX ======================= -->

# onecall — one call per dependency layer

**Invoked with a question?** Before the first call, write the list of pieces and their layers,
then make one labelled call per layer (§ The method).

## Why

Every tool call re-sends the entire context window. Measured on 161 real sessions (13 021
requests, median window 127k tokens):

- A shell call adds **~434 tokens of fixed overhead** to the window (command text, tool wrapper,
  reasoning) on top of its own result. 100 one-item calls carry ~43k tokens of pure overhead.
- A controlled A/B on the same read-only task (4 verbs × 4 questions, 2 runs per arm):

  | Method | Turns | Tokens processed | Time |
  |---|---|---|---|
  | one question per call | 27–28 | 705k–759k | 83–92 s |
  | one call per layer | 3 | 72k–73k | 38–45 s |

  **~10× fewer tokens, 9× fewer turns, half the time, same answer quality.**

Bytes are not the goal; round-trips are. A needed piece costs the same bytes in one batch or in
three calls. Splitting only adds round-trips.

## The method

1. **List before calling.** Write down every question of the step, not just the next one.
2. **Layer by dependency.** Layer 0 needs nothing; layer 1 needs a value from layer 0. **One call
   per layer**, whatever the topic. Unrelated pieces (git, a doc grep, `ls`, a tool version) are
   cheaper together than apart. Join with `;` and a numbered label (`echo "=== 1 ==="`,
   `=== 2.1 ===` for a sub-item), never `&&`: a failing piece must not kill the rest.
3. **Bound every piece by construction.** `head -N | cut -c1-M` makes a piece at most N×M chars;
   keep the sum of N×M under **25 000**. Unknown size: `head -c K`. Failing piece: `2>&1`.
   Slice by stable text markers (`sed -n '/^## Fases/,/^## Next/p'`), never by line numbers,
   which need a previous call to learn. In source files the marker is an anchor plus context:
   `grep -n -A4 'return (f"onecall' hooks/posttool.py | cut -c1-240` fetches the match and its
   body in the same layer, where `grep` for line numbers then `sed -n 'N,Mp'` costs two.
   **Under RTK** (`~/.claude/RTK.md`) the hook rewrites `grep` to `rtk grep`: a `"` inside the
   pattern matches nothing with no error (even via `rtk proxy`), matched lines are elided at 80
   chars, `-h` prints help. `\|` and `-E 'a|b'` work; `command grep` is still rewritten.
   `/usr/bin/grep` bypasses it (raw lines, quotes work). Otherwise write `.` for the `"`. An empty
   grep result is a tooling suspect before it is a finding.
   **Under PowerShell** a flag whose attached value holds spaces (`git log -S"two words"`) can
   reach the program split in two; pass it as one quoted token (`"-Stwo words"`) or run that
   piece under Bash. An empty result there is a quoting suspect too (tia F123: 3 of a worker's 6
   lone `git log -S` calls were quoting retries).
4. **Spend the leftover on the next layer.** Needed pieces came to 8k? The other ~17k carries the
   layer-1 pieces you can already predict, probes for both branches when the next step depends on
   an answer, and a cheap count (`grep -c`, `wc -c`) before any big sample. A speculative piece
   stays in the window for ~42 turns, so it earns its place only if it is likely to save a call.
5. **Split only when forced.** A layer over 25k splits by piece, never by topic; the pieces that
   decide the others go first.
6. **An empty or ambiguous piece gets a verification layer before the answer.** A bounded grep
   that misses is a pattern problem, not a finding. "Not confirmed" is never a final answer when
   one more batch settles it (the only quality miss in the A/B was exactly this).

`25k` is a ceiling, not a target: never pad a call to reach it.

## The cap

Both shell tools persist any result over **30 000 bytes (UTF-8, not chars)** to a file and
return a ~2 KB preview (`<persisted-output> Output too large`). The whole batch is lost from view,
not just the tail. Measured on both Bash and PowerShell: 29 000 ASCII chars inline, 31 000 ASCII
overflow, and 15 500 accented chars (31 000 bytes) overflow too. `cut -c` counts chars, so
text full of accents spends the budget about twice as fast: halve N×M for it.

Every one of the 15 real Bash overflows was a single unbounded piece, never too many pieces:

- `grep` on a file with very long lines, without `cut` (9 of 15, up to 5.5 MB);
- `sed -n 'A,Bp'` over a wide range of a big doc or source file;
- `cat` of a whole file, `python -c` dumping JSON, a table printed with `cut -c1-450`.

Near misses (≥20k) were the same shapes: `cat` of whole CLAUDE.md/SKILL.md/source files and long
`sed` ranges.

## Tools

- **Hook** `hooks/posttool.py` (PostToolUse, `Bash|PowerShell`): silent on normal calls. Speaks
  one line on overflow, on a result over 25k, or after 3 small single-piece calls in a row
  that did not depend on each other (no retry, no token reused from the previous output, no
  action like a commit or build, same user turn, not parallel siblings). Replayed over 11k past
  calls that fires 0.5 times per 100 calls, median 0 per session.
  `python hooks/posttool.py --summary <session_id>` prints the session counters.
- **Calibrate** `python scripts/calibrate.py [--sample N]`: replays the hook over past
  transcripts for a grid of `SMALL`/`STREAK` and prints nudges per session; `--sample` shows
  nudged streaks to judge by eye.
- **Audit** `python scripts/audit.py [--since YYYY-MM-DD] [--per-agent] [~/.claude/projects/<dir>]`: reads
  subagent (orchestrate worker) transcripts too; `--per-agent` adds one row per transcript. Context per round-trip, fixed
  overhead per call, chars/token, overflows and near misses per tool, labelled vs single-piece.
- **A/B** `bash scripts/ab/run.sh <repo>`: runs `task.txt` headless under both methods and
  `python scripts/ab/report.py` compares turns and tokens. Swap `task.txt` to test another task.

## What this does not change

- Commands that must not run concurrently (a single-session API, a build) still run alone.
- A call whose input depends on the previous output is the next layer, not part of this one.
- A loaded session that is one or two steps from closing a gap should take them before a
  handoff: re-deriving warm context in a new session costs more than the extra turns.
