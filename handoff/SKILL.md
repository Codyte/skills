---
name: handoff
description: Save a compact handoff of the current session (goal, state, decisions, next steps, key files) so you can /clear and resume cheaply. The SessionStart hook auto-loads it on the next session. Use when switching tasks, before /clear, when context grows large (>150k), or when the user says "handoff", "save state", "/handoff".
---

# /handoff — save session state so `/clear` is free

Long sessions at large context are the #1 cost driver. `/clear` fixes that but loses the thread —
this skill removes that downside: it writes a terse resume cue that the **SessionStart hook auto-loads**
on the next session, so after `/clear` you continue from exactly where you left off.

## Steps

1. Get the target path (keeps skill + hook in sync):
   ```
   python "$HOME/.claude/skills/handoff/load_handoff.py" --path
   ```
   (On Windows the same works via Git Bash; or use the printed absolute path directly.)
2. **Write** that file with the sections below — terse, high-signal, no transcript. Overwrite it
   (idempotent; one handoff per project).
3. Tell the user it's saved and they can now `/clear`; the next session resumes automatically.

## Format (keep under ~80 lines — a resume cue, not a log)

```markdown
# Handoff · <project> · <date>

## Goal
<the current objective in 1-2 lines>

## State
- Done: <what's finished>
- In progress: <what's mid-flight, and exactly where>

## Decisions (and why)
- <decision> — <reason>

## Next steps (ordered)
1. <next concrete action>
2. ...

## Key files
- <path:line> — <what's there>

## Open / blockers
- <questions or blockers, if any>
```

## Notes
- Handoff files live in `~/.claude/handoff/` (per machine), never in the skills repo — session
  state must not pollute versioned skills.
- This does NOT run `/clear` for you (the agent cannot invoke built-in commands). It prepares the
  resume so that when *you* run `/clear`, nothing is lost.
