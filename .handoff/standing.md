# Standing decisions — persistent constraints for this project

- `.claude/skills/navindex` (and caveman/handoff/ponytail) are junctions to
  `.agents/skills/<name>` — editing the repo copy IS editing the installed skill; never attempt a
  "sync to installed copy" step, it's a no-op (`cp` fails with "are the same file").
- Nested skill repos (navindex/caveman/handoff/ponytail) are real git submodules now — commits
  made with `cd <sub>` land in the SUBMODULE's own repo, not the parent. After committing inside
  one, always `cd ..` and `git add <sub> && git commit` in the parent to advance its pointer, or
  the parent silently drifts behind.
