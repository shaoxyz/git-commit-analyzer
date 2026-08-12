#!/usr/bin/env python3
"""Generate a harness-neutral commit-analysis brief."""

import argparse
import json
import sys
from pathlib import Path

SCHEMA = {
    "report_date": "YYYY-MM-DD",
    "repository": "repository name or path",
    "period": {"since": "requested start", "until": "requested end or null"},
    "confidence": "high | medium | low",
    "team_summary": {
        "total_commits": 0,
        "real_work_score": 0,
        "noise_ratio": "0%",
        "team_grade": "grade",
        "mvp": "author or N/A",
        "evidence_summary": "one evidence-backed sentence",
    },
    "leaderboard": [
        {
            "rank": 1,
            "name": "author",
            "final_score": 0,
            "grade": "grade",
            "title": "playful title",
            "award": "playful award",
            "commits": 0,
            "effective_lines": 0,
            "badges": [],
            "summary": "evidence-backed summary",
            "sharp_review": "short code-focused roast",
            "context_confidence": "high | medium | low",
        }
    ],
    "commits": [
        {
            "sha": "short sha",
            "author": "author",
            "substance_score": 0,
            "bullshit_score": 0,
            "final_score": 0,
            "code_quality": "good | acceptable | poor",
            "rewrite_index": 3,
            "business_value": "core | infrastructure | useful improvement | unclear",
            "business_value_confidence": "high | medium | low",
            "badges": [],
            "roast": "playful code-focused comment",
            "sharp_review": "direct technical comment",
        }
    ],
    "risks": ["specific evidence-backed risk"],
    "missing_context": ["context that would materially change the judgment"],
    "daily_roast": "playful closing line",
    "closing_roast": "direct but non-personal closing line",
    "disclaimer": "仅供代码复盘与团队娱乐，不得用于绩效评估。",
}


INTRO = {
    "zh": """你是“牛马鉴定师”：代码评审要有证据，表达可以有梗。

分析提交所代表的工程工作，不按行数或 commit 数论英雄。吐槽代码和提交模式，不攻击作者，也不评价职业价值。

规则：
- 机器计算的 substance_score 与 bullshit_score 必须原样保留；它们只是启发式信号。
- 区分事实、启发式信号和上下文判断。
- 没有 Issue、PR、测试或业务文档支撑时，业务价值最多给低置信度；无法判断就写 unclear。
- 不得根据代码风格推断作者使用了 AI。
- 重写指数衡量复现任务所需的上下文：1=机械改动，5=依赖稀缺领域或运行证据。它不衡量人的价值。
- 笑点服从事实。低价值但必要的机械工作不应被污名化。
- 仅输出符合给定结构的有效 JSON，不要使用 Markdown 代码围栏。

趣味等级可使用：🔥 夯、💎 顶级、👑 人上人、🧍 NPC、💀 拉完了。分数相近时不要制造虚假差距。
""",
    "en": """You are a commit analyst: evidence first, jokes second.

Evaluate the engineering work represented by commits. Do not treat line count or commit count as contribution. Roast code and commit patterns, never an author's identity, intelligence, career, or worth.

Rules:
- Preserve machine-calculated substance_score and bullshit_score exactly; they are heuristic signals only.
- Separate facts, heuristic signals, and contextual judgments.
- Without issue, PR, test, or product context, business-value confidence must be low; use unclear when needed.
- Never infer AI authorship from coding style.
- Rewrite index measures context required to reproduce the task: 1=mechanical, 5=scarce domain or operational evidence. It does not measure human worth.
- Keep humor subordinate to evidence. Necessary mechanical work is not a character flaw.
- Return valid JSON matching the supplied shape, without Markdown fences.

Playful grades may use: 🔥 Beast, 💎 Elite, 👑 Solid, 🧍 NPC, 💀 Rough day. Do not manufacture separation between similar scores.
""",
}


def load_metrics(commits_file: str) -> dict | None:
    path = Path(commits_file)
    metrics_file = path.with_name(f"{path.stem}_metrics.json")
    if not metrics_file.exists():
        return None
    with metrics_file.open("r", encoding="utf-8") as file:
        return json.load(file)


def generate_prompt(commits_file: str, lang: str = "zh", max_commits: int = 20) -> str:
    with open(commits_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    commits = data.get("commits", [])[:max_commits]
    simplified = []
    for commit in commits:
        diff = commit.get("diff", "")
        simplified.append(
            {
                "sha": commit.get("sha", "")[:8],
                "author": commit.get("author", {}).get("name", "Unknown"),
                "date": commit.get("date"),
                "message": commit.get("message", ""),
                "stats": commit.get("stats", {}),
                "changed_files": commit.get("changed_files", []),
                "diff": diff[:3000] + ("...[truncated]" if len(diff) > 3000 else ""),
            }
        )

    evidence = {
        "source": data.get("source"),
        "period": {"since": data.get("since"), "until": data.get("until")},
        "included_commits": len(simplified),
        "total_collected_commits": len(data.get("commits", [])),
        "metrics": load_metrics(commits_file),
        "commits": simplified,
    }

    return "\n".join(
        [
            INTRO[lang].strip(),
            "",
            "## Evidence" if lang == "en" else "## 证据",
            json.dumps(evidence, indent=2, ensure_ascii=False),
            "",
            "## Required JSON shape" if lang == "en" else "## 必须遵循的 JSON 结构",
            json.dumps(SCHEMA, indent=2, ensure_ascii=False),
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a harness-neutral commit-analysis brief"
    )
    parser.add_argument("commits_file", help="Path to commits.json")
    parser.add_argument("--lang", "-l", choices=["zh", "en"], default="zh")
    parser.add_argument("--max-commits", type=int, default=20)
    parser.add_argument("--output", "-o", help="Output file; defaults to stdout")
    args = parser.parse_args()

    prompt = generate_prompt(args.commits_file, args.lang, args.max_commits)
    if args.output:
        Path(args.output).write_text(prompt, encoding="utf-8")
        print(f"Analysis brief written to {args.output}", file=sys.stderr)
    else:
        print(prompt)


if __name__ == "__main__":
    main()
