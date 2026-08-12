---
name: git-commit-analyzer
description: Analyze Git commits with deterministic metrics and contextual AI review, then produce a concise or playful contribution report. Use when asked to review recent commits, summarize engineering work, compare contribution patterns, inspect commit quality, or generate a 牛马鉴定报告 from a local repository, GitHub repository, or GitLab project.
---

# Git Commit Analyzer

Analyze the work represented by commits, not the raw amount of code. Keep the evidence serious and the delivery fun.

## Defaults

- Use the current Git repository when no repository is specified.
- Use the last day when no time range is specified.
- Match the user's language.
- Return a concise Markdown summary unless the user asks for JSON, HTML, or a saved artifact.
- Use playful “牛马鉴定器” copy by default. Use neutral copy when the context is formal or the user asks for it.

## Workflow

1. Resolve the repository, time range, authors, language, and output format from the request.
2. Treat the directory containing this `SKILL.md` as `SKILL_ROOT`. Do not assume a harness-specific install path.
3. Prefer a local checkout. Use a remote API only when the user requests it or no checkout is available.
4. Create intermediate files in a temporary or workspace scratch directory, not inside the analyzed repository.
5. Collect commits:

   ```bash
   python3 "$SKILL_ROOT/scripts/fetch_commits.py" /path/to/repo --since "1 day ago" -o commits.json
   ```

   For GitHub or GitLab examples and required environment variables, read [references/config.md](references/config.md).

6. If no commits are returned, say so and stop. Do not manufacture a ranking.
7. Calculate deterministic metrics:

   ```bash
   python3 "$SKILL_ROOT/scripts/analyze_code.py" commits.json
   ```

8. Generate the task-specific analysis brief:

   ```bash
   python3 "$SKILL_ROOT/scripts/generate_prompt.py" commits.json --lang zh -o prompt.md
   ```

9. Use `prompt.md`, `commits.json`, and `commits_metrics.json` as evidence. Inspect relevant repository context when business value or architectural impact cannot be established from a diff alone.
10. Produce valid analysis JSON following the schema in the generated brief. Preserve machine-calculated values exactly.
11. When a file report is requested, render it:

    ```bash
    python3 "$SKILL_ROOT/scripts/generate_report.py" analysis.json --lang zh --format markdown
    ```

12. Verify that the report exists, opens, and agrees with the analyzed commit count and time range.

## Review Rules

- Separate observed facts, heuristic signals, and contextual judgments.
- Do not equate lines changed, commit count, or generated-code volume with contribution value.
- Treat `substance_score` and `bullshit_score` as heuristics, not truth.
- Do not infer that code was AI-generated from style alone. Report only concrete generated-file markers or repetition signals.
- Do not guess revenue impact, incident severity, or user value. Mark the business-value judgment as low confidence when context is missing.
- Roast the code or commit pattern, not a person's identity, intelligence, career, or worth.
- Never present this report as a performance evaluation or use it to recommend employment action.
- Avoid sending private diffs, author emails, credentials, or proprietary code to an external service without authorization.

## Output

Lead with:

- repository and time range;
- commit count and authors covered;
- the strongest contribution signal;
- the largest quality or maintenance risk;
- confidence and missing context.

Then add the playful grade, badges, and roast. Keep jokes subordinate to the evidence.

For deeper architecture and business-context review, read [modes/ANALYZE_MODE.md](modes/ANALYZE_MODE.md).

End every report with: “仅供代码复盘与团队娱乐，不得用于绩效评估。”
