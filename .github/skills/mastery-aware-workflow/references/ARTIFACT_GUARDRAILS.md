# Artifact guardrails

This repository uses **protected artifacts** to prevent Cognitive Bypass:

- `brainsback/TODO.md` (human-only)
- `brainsback/REACTO.md` (human-only)

Rules for agents:

- Never modify either file.
- Never draft paste-ready content intended for either file.
- If asked to fill them, refuse and ask questions instead.
- If a diff modifies them, assume it was made by the human developer.
