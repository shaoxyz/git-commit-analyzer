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

## Analysis Parameters

### Customizing Type Multipliers

Edit the effort calculation in your workflow:

```python
TYPE_MULTIPLIERS = {
    "feature": 1.0,
    "bugfix": 1.0,
    "refactor": 0.9,
    "chore": 0.5,
    "docs": 0.3,
    "test": 0.7,
    "style": 0.3,
}
```

Adjust based on your team's priorities. For example, if tests are critical:
```python
"test": 1.0,  # Elevate test importance
```

### Complexity/Impact Scale Customization

The default 1-5 scale can be interpreted based on your codebase:

**For microservices:**
- Impact 4 = affects service API
- Impact 5 = affects inter-service communication

**For monolith:**
- Impact 4 = affects multiple modules
- Impact 5 = affects core domain logic

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Daily Commit Analysis

on:
  schedule:
    - cron: '0 9 * * 1-5'  # 9 AM weekdays
  workflow_dispatch:

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Fetch commits
        run: |
          python scripts/fetch_commits.py . \
            --since "1 day ago" \
            --output commits.json
      
      - name: Analyze with Claude
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          # Your analysis integration here
          python scripts/generate_prompt.py commits.json > prompt.txt
          # Call Claude API with prompt.txt
      
      - name: Post to Slack
        # Your notification integration
```

### GitLab CI Example

```yaml
commit-analysis:
  stage: report
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
  script:
    - pip install requests
    - python scripts/fetch_commits.py --gitlab $CI_PROJECT_ID --since "1 day ago"
    - python scripts/generate_prompt.py commits.json | your-claude-integration
```

## Report Templates

### Daily Standup Format

Focus on: what was done, blockers, what's next

### Weekly Summary Format

Focus on: major achievements, trends, team velocity

### Sprint Retrospective Format

Focus on: completed features, tech debt addressed, lessons learned

## Filtering Options

### By Author
```bash
# In your workflow, filter commits JSON by author
jq '.commits | map(select(.author.name == "Alice"))' commits.json
```

### By Path
```bash
# Filter to specific directories
git log --since="1 day ago" -- src/api/
```

### By Type (via commit message convention)
If using conventional commits:
```bash
git log --since="1 day ago" --grep="^feat:"
```
