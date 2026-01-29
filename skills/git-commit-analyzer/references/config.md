# Configuration Reference

## Environment Variables

### GitHub
```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
```

### GitLab
```bash
export GITLAB_TOKEN="glpat-xxxxxxxxxxxx"
export GITLAB_URL="https://gitlab.com"  # or self-hosted URL
```

## Script Parameters

### fetch_commits.py
```bash
python fetch_commits.py /path/to/repo --since "1 day ago" -o commits.json
python fetch_commits.py --github owner/repo --since "1 week ago"
python fetch_commits.py --gitlab project-id --since "2024-01-01"
```

### analyze_code.py
```bash
python analyze_code.py commits.json -o metrics.json
```

### generate_prompt.py
```bash
python generate_prompt.py commits.json --lang zh > prompt.txt  # Chinese
python generate_prompt.py commits.json --lang en > prompt.txt  # English
python generate_prompt.py commits.json --max-commits 100
```

### generate_report.py
```bash
python generate_report.py analysis.json --lang zh  # Chinese
python generate_report.py analysis.json --lang en  # English
python generate_report.py analysis.json -f html    # HTML format
```

## CI/CD Integration

### GitHub Actions
```yaml
name: Daily Commit Analysis
on:
  schedule:
    - cron: '0 9 * * 1-5'
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - run: |
          python scripts/fetch_commits.py . --since "1 day ago" -o commits.json
          python scripts/analyze_code.py commits.json
          python scripts/generate_prompt.py commits.json --lang en > prompt.txt
```

### GitLab CI
```yaml
commit-analysis:
  stage: report
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
  script:
    - python scripts/fetch_commits.py --gitlab $CI_PROJECT_ID --since "1 day ago"
    - python scripts/analyze_code.py commits.json
    - python scripts/generate_prompt.py commits.json --lang en
```

## Filtering

### By Author
```bash
jq '.commits | map(select(.author.name == "Alice"))' commits.json
```

### By Path
```bash
git log --since="1 day ago" -- src/api/
```
