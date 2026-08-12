#!/usr/bin/env python3
"""Render commit-analysis JSON as Markdown or a standalone HTML document."""

import argparse
import html
import json
from datetime import datetime, timezone
from pathlib import Path

TEXT = {
    "zh": {
        "title": "🐂🐴 牛马鉴定报告",
        "date": "日期",
        "repo": "仓库",
        "period": "范围",
        "confidence": "置信度",
        "summary": "📊 证据总览",
        "commits": "提交数",
        "score": "有效工作分",
        "noise": "噪声比例",
        "grade": "评级",
        "mvp": "今日 MVP",
        "leaderboard": "🏆 牛马排行榜",
        "details": "📝 提交明细",
        "risks": "⚠️ 风险",
        "missing": "🔎 缺失上下文",
        "disclaimer": "仅供代码复盘与团队娱乐，不得用于绩效评估。",
    },
    "en": {
        "title": "🐂🐴 Commit Analysis Report",
        "date": "Date",
        "repo": "Repository",
        "period": "Period",
        "confidence": "Confidence",
        "summary": "📊 Evidence Summary",
        "commits": "Commits",
        "score": "Real Work Score",
        "noise": "Noise Ratio",
        "grade": "Grade",
        "mvp": "MVP",
        "leaderboard": "🏆 Leaderboard",
        "details": "📝 Commit Details",
        "risks": "⚠️ Risks",
        "missing": "🔎 Missing Context",
        "disclaimer": "For code review and team entertainment only. Not for performance evaluation.",
    },
}


def generate_markdown_report(analysis: dict, lang: str = "zh") -> str:
    text = TEXT[lang]
    period = analysis.get("period", {})
    lines = [
        f"# {text['title']}",
        "",
        f"**{text['date']}**: {analysis.get('report_date', datetime.now(timezone.utc).strftime('%Y-%m-%d'))}",
        f"**{text['repo']}**: {analysis.get('repository', 'N/A')}",
        f"**{text['period']}**: {period.get('since', 'N/A')} → {period.get('until') or 'now'}",
        f"**{text['confidence']}**: {analysis.get('confidence', 'low')}",
        "",
    ]

    summary = analysis.get("team_summary", {})
    lines.extend(
        [
            f"## {text['summary']}",
            "",
            f"| {text['commits']} | {text['score']} | {text['noise']} | {text['grade']} | {text['mvp']} |",
            "|---:|---:|---:|---|---|",
            f"| {summary.get('total_commits', 0)} | {summary.get('real_work_score', 0)} | {summary.get('noise_ratio', 'N/A')} | {summary.get('team_grade', 'N/A')} | {summary.get('mvp', 'N/A')} |",
            "",
        ]
    )
    if summary.get("evidence_summary"):
        lines.extend([f"> {summary['evidence_summary']}", ""])

    leaderboard = analysis.get("leaderboard", [])
    if leaderboard:
        lines.extend([f"## {text['leaderboard']}", ""])
        for entry in leaderboard:
            rank = entry.get("rank", "?")
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, "🏅")
            lines.extend(
                [
                    f"### {medal} #{rank} {entry.get('name', 'Unknown')}",
                    "",
                    f"**{entry.get('grade', '')} · {entry.get('title', '')}** — {entry.get('award', '')}",
                    "",
                    f"Score: **{entry.get('final_score', 0)}** · Commits: {entry.get('commits', 0)} · Context confidence: {entry.get('context_confidence', 'low')}",
                    "",
                ]
            )
            if entry.get("badges"):
                lines.extend([" ".join(entry["badges"]), ""])
            if entry.get("summary"):
                lines.append(f"> {entry['summary']}")
            if entry.get("sharp_review"):
                lines.append(f"> 🔥 {entry['sharp_review']}")
            lines.append("")

    commits = analysis.get("commits", [])
    if commits:
        lines.extend([f"## {text['details']}", ""])
        for commit in commits:
            lines.extend(
                [
                    f"### `{commit.get('sha', 'N/A')[:8]}` · {commit.get('author', 'Unknown')}",
                    "",
                    f"Substance: {commit.get('substance_score', 0)} · Noise: {commit.get('bullshit_score', 0)} · Rewrite index: {commit.get('rewrite_index', 'N/A')}/5",
                    f"Business value: {commit.get('business_value', 'unclear')} ({commit.get('business_value_confidence', 'low')} confidence)",
                    "",
                ]
            )
            if commit.get("badges"):
                lines.extend([" ".join(commit["badges"]), ""])
            if commit.get("roast"):
                lines.append(f"> 💬 {commit['roast']}")
            if commit.get("sharp_review"):
                lines.append(f"> 🔥 {commit['sharp_review']}")
            lines.append("")

    for key, heading in (
        ("risks", text["risks"]),
        ("missing_context", text["missing"]),
    ):
        items = analysis.get(key, [])
        if items:
            lines.extend([f"## {heading}", ""])
            lines.extend(f"- {item}" for item in items)
            lines.append("")

    if analysis.get("daily_roast"):
        lines.extend(["---", "", f"🎤 *{analysis['daily_roast']}*", ""])
    if analysis.get("closing_roast"):
        lines.extend([f"🔥 *{analysis['closing_roast']}*", ""])

    lines.extend(["---", "", f"*{analysis.get('disclaimer') or text['disclaimer']}*"])
    return "\n".join(lines)


def generate_html_report(analysis: dict, lang: str = "zh") -> str:
    markdown = html.escape(generate_markdown_report(analysis, lang))
    title = html.escape(TEXT[lang]["title"])
    html_lang = "zh-CN" if lang == "zh" else "en"
    return f'''<!doctype html>
<html lang="{html_lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    body {{ max-width: 900px; margin: 0 auto; padding: 24px; color: #202124; background: #fafafa; font: 16px/1.65 system-ui, sans-serif; }}
    pre {{ white-space: pre-wrap; overflow-wrap: anywhere; font: inherit; background: white; padding: 28px; border: 1px solid #e5e7eb; border-radius: 16px; box-shadow: 0 8px 30px rgba(0,0,0,.05); }}
  </style>
</head>
<body><pre>{markdown}</pre></body>
</html>'''


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a commit-analysis report")
    parser.add_argument("analysis_file", help="Path to analysis.json")
    parser.add_argument(
        "--format", "-f", choices=["markdown", "html"], default="markdown"
    )
    parser.add_argument("--lang", "-l", choices=["zh", "en"], default="zh")
    parser.add_argument("--output", "-o")
    args = parser.parse_args()

    with open(args.analysis_file, "r", encoding="utf-8") as file:
        analysis = json.load(file)
    content = (
        generate_html_report(analysis, args.lang)
        if args.format == "html"
        else generate_markdown_report(analysis, args.lang)
    )
    suffix = ".html" if args.format == "html" else ".md"
    output = (
        Path(args.output)
        if args.output
        else Path(args.analysis_file).with_name(
            f"{Path(args.analysis_file).stem}_report{suffix}"
        )
    )
    output.write_text(content, encoding="utf-8")
    print(f"Report generated: {output}")


if __name__ == "__main__":
    main()
