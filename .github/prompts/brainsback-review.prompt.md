---
mode: agent
description: Run a Socratic review of the current task iteration and save the findings to SOCRATIC_REVIEW.md.
---

Read the agent instructions from `.github/agents/brainsback-reviewer.md` and apply them to the current task iteration.

The **current task folder** is the most recently created folder under `.brainsback/` (highest 7-digit sequence number prefix), or the parent folder of whichever brainsback artifact is currently open in the editor.

From the current task folder, read:
- `TODO.md` — the original strategic plan
- `REPORT.md` — what was actually implemented
- `REACTO.md` — the developer's proof of mastery

Conduct the Socratic review session interactively with the developer:
1. Restate intent from `TODO.md` and `REPORT.md`
2. Cross-check all REACTO-SE sections (R, E, A, C, T, O) for completeness and accuracy
3. Ask probing questions about failure modes, invariants, tests, security/boundaries, and performance — do not give verdicts

When the session is complete, write the full transcript — all questions asked, all developer responses, and any unresolved issues — to `SOCRATIC_REVIEW.md` inside the current task folder.
