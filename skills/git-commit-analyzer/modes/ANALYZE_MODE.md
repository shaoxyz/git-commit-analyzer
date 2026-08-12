# Deep Analysis Mode

Use this mode when the user asks for architectural depth, business impact, maintenance risk, or a rewrite decision. Do not use it for a simple daily summary.

## Context to Collect

Inspect only what is needed:

- README or product documentation for project purpose;
- linked issues or pull requests for user need and decision history;
- tests for intended behavior and regression protection;
- nearby implementations for architectural consistency;
- blame or earlier commits when the current diff depends on historical constraints.

Use the tools available in the current harness. Parallelize independent read-only checks when supported, but do not require subagents, named roles, or a specific tool API.

## Questions to Answer

### Value

- What concrete user, operational, or developer problem changed?
- What evidence supports that conclusion?
- Would removing the change alter observable behavior?

### Difficulty

- How much repository-specific or domain context was required?
- Was the difficult part implementation volume, diagnosis, trade-offs, migration, or verification?
- Could a capable coding agent reproduce the result from the available requirements and tests?

### Quality and Risk

- Does the change match existing architecture?
- Are important paths tested?
- Does it introduce security, compatibility, performance, or maintenance risk?
- Are generated files, formatting, or mechanical edits inflating the diff?

## Confidence

Label contextual judgments as high, medium, or low confidence.

- High: supported by code plus tests, issue/PR context, or runtime evidence.
- Medium: supported by code and repository documentation.
- Low: inferred from the diff or commit message alone.

If business context is unavailable, use “context insufficient” instead of inventing impact.

## Rewrite Index

Score the contextual difficulty of reproducing the change:

| Score | Meaning |
|---|---|
| 1 | Mechanical change with explicit instructions |
| 2 | Common pattern with limited repository context |
| 3 | Requires meaningful domain or repository knowledge |
| 4 | Requires non-obvious trade-offs, diagnosis, or migration work |
| 5 | Depends on scarce operational knowledge or hard-won evidence |

The index measures task context, not human worth. A low score is not a negative when the change is useful and correct.

## Deep Report Shape

```markdown
## Analysis: <target>

### Evidence-backed summary
<what changed and why it matters>

### Value
- Classification: core / infrastructure / useful improvement / unclear
- Evidence: <code, tests, issue, PR, or runtime evidence>
- Confidence: high / medium / low

### Engineering assessment
- Difficulty source: <diagnosis, domain logic, migration, implementation, verification>
- Rewrite index: <1-5>
- Quality signals: <tests, simplicity, consistency>
- Risks: <specific risks or none found>

### 牛马鉴定
<short playful grade and code-focused roast>

### Next actions
<only actions justified by the evidence>
```

End with the non-performance-evaluation disclaimer from `SKILL.md`.
