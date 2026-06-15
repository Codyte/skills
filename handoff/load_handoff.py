#!/usr/bin/env python3
"""Handoff loader/locator — shared by the /handoff skill and the SessionStart hook.

Two modes:
  python load_handoff.py --path     -> print the handoff file path for the current project (the
                                       /handoff skill writes there, so skill and hook always agree)
  python load_handoff.py            -> HOOK mode: read the SessionStart JSON on stdin, and if a
                                       handoff exists for that project, print it. A SessionStart
                                       hook's stdout is injected as context, so the next session
                                       (after /clear) resumes from the saved state automatically.

Handoff files live under ~/.claude/handoff/<sanitized-project-path>.md — per machine, NOT in the
skills repo, so session state never pollutes the versioned skills.
"""
import sys, os, json, re, pathlib

# Windows consoles default to cp1252; handoff text (accents, em-dashes) would crash on print.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def handoff_file(cwd):
    home = pathlib.Path(os.path.expanduser("~"))
    key = re.sub(r"[^A-Za-z0-9]+", "_", os.path.abspath(cwd)).strip("_") or "root"
    d = home / ".claude" / "handoff"
    d.mkdir(parents=True, exist_ok=True)
    return d / (key + ".md")


def main():
    if "--path" in sys.argv:
        print(handoff_file(os.getcwd()))
        return
    # HOOK mode: cwd comes from the SessionStart payload on stdin (fallback to process cwd).
    cwd = os.getcwd()
    try:
        cwd = json.load(sys.stdin).get("cwd") or cwd
    except Exception:
        pass
    f = handoff_file(cwd)
    if f.exists():
        txt = f.read_text(encoding="utf-8").strip()
        if txt:
            print("# Resuming from saved handoff (written by /handoff). Continue from here:\n")
            print(txt)


if __name__ == "__main__":
    main()
