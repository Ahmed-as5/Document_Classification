# Security

## Policy
- Do not commit sensitive or non-redistributable datasets. Commit download scripts and instructions instead.
- Do not commit secrets (API keys, passwords, `.env`).
- Work on a personal branch; no direct pushes to `main`.
- Load `.joblib` model files only from trusted sources: loading them can execute code.

## Input validation (expected behaviour)
- Reject missing, empty, blank or non-string text with 400/422.
- Limit input length.
- Do not log full document text or return stack traces to users.

## Review checklist
- [ ] No secrets in tracked files or git history
- [ ] No restricted data tracked
- [ ] Input validation tested
- [ ] Input length limit present
- [ ] CORS restricted to the frontend origin
- [ ] Frontend does not insert user text with `innerHTML`

## Findings
Review not yet recorded.
