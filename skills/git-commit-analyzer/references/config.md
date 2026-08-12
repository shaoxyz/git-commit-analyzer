# Configuration Reference

`SKILL_ROOT` means the directory containing this skill's `SKILL.md`. Resolve it from the loaded skill location; do not assume `.claude`, `.codex`, or another harness-specific directory.

## Local Repository

Prefer a local checkout because it needs no network credentials and preserves complete Git history.

```bash
python3 "$SKILL_ROOT/scripts/fetch_commits.py" /path/to/repo \
  --since "1 day ago" \
  --until "2026-01-30" \
  -o commits.json
```

The checkout must contain the requested history. Shallow clones may need their history fetched before analysis.

## GitHub

Set `GITHUB_TOKEN` only in the process environment. Never place a token in a prompt, report, repository file, or command output.

```bash
GITHUB_TOKEN=... python3 "$SKILL_ROOT/scripts/fetch_commits.py" \
  --github owner/repo \
  --since "2026-01-01T00:00:00Z" \
  -o commits.json
```

## GitLab

Set `GITLAB_TOKEN`. Set `GITLAB_URL` only for a self-hosted instance.

```bash
GITLAB_TOKEN=... GITLAB_URL=https://gitlab.example.com \
python3 "$SKILL_ROOT/scripts/fetch_commits.py" \
  --gitlab group/project \
  --since "2026-01-01T00:00:00Z" \
  -o commits.json
```

## Analysis and Rendering

```bash
python3 "$SKILL_ROOT/scripts/analyze_code.py" commits.json
python3 "$SKILL_ROOT/scripts/generate_prompt.py" commits.json --lang en -o prompt.md
python3 "$SKILL_ROOT/scripts/generate_report.py" analysis.json --lang en --format html
```

Use `--max-commits` on `generate_prompt.py` to bound model context. Narrow the time range instead of silently dropping relevant commits when completeness matters.

## Filters

Apply author or path filters during Git collection when possible. If post-processing is required, preserve the original `commits.json` and write filtered data to a new scratch file.
