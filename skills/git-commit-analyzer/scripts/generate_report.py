#!/usr/bin/env python3
"""
Generate formatted reports from Claude's analysis JSON output.
Displays both playful corporate style and Linus-style comments together.
"""

import argparse
import json
from datetime import datetime

I18N = {
    "zh": {
        "title": "🐂🐴 牛马鉴定报告",
        "date": "日期",
        "team_vibe": "今日氛围",
        "linus_mood": "Linus 心情",
        "team_summary": "📊 团队总览",
        "total_commits": "总提交数",
        "real_work_score": "实际工作分",
        "bullshit_ratio": "水分比例",
        "team_grade": "团队评级",
        "mvp": "今日 MVP",
        "leaderboard": "🏆 牛马排行榜",
        "rank": "排名",
        "name": "牛马",
        "score": "得分",
        "grade": "等级",
        "person_title": "称号",
        "award": "颁奖词",
        "commits": "提交数",
        "effective_lines": "有效行数",
        "badges": "徽章",
        "ai_survivor": "AI 生存指数",
        "ai_verdict": "AI 审判",
        "commit_details": "📝 提交明细",
        "complexity": "技术深度",
        "impact": "影响范围",
        "substance": "实质分",
        "bullshit": "水分",
        "quality": "质量系数",
        "final": "最终得分",
        "rewrite_index": "重写指数",
        "business_value": "业务价值",
        "wall_of_shame": "🚨 耻辱墙",
        "ai_era_verdict": "🤖 AI 时代审判",
        "most_irreplaceable": "最不可替代",
        "most_replaceable": "最易被替代",
        "team_future": "团队前景",
        "daily_roast": "🎤 今日金句",
        "closing_rant": "🎤 Linus 收尾",
        "disclaimer": "本报告由 AI 生成，仅供娱乐，严禁用于绩效评估。在 AI 时代，代码量不代表贡献，脑子才是。",
    },
    "en": {
        "title": "🐂🐴 Code Commit Report",
        "date": "Date",
        "team_vibe": "Team Vibe",
        "linus_mood": "Linus Mood",
        "team_summary": "📊 Team Summary",
        "total_commits": "Total Commits",
        "real_work_score": "Real Work Score",
        "bullshit_ratio": "Bullshit Ratio",
        "team_grade": "Team Grade",
        "mvp": "Today's MVP",
        "leaderboard": "🏆 Leaderboard",
        "rank": "Rank",
        "name": "Name",
        "score": "Score",
        "grade": "Grade",
        "person_title": "Title",
        "award": "Award",
        "commits": "Commits",
        "effective_lines": "Effective Lines",
        "badges": "Badges",
        "ai_survivor": "AI Survivor Score",
        "ai_verdict": "AI Verdict",
        "commit_details": "📝 Commit Details",
        "complexity": "Complexity",
        "impact": "Impact",
        "substance": "Substance",
        "bullshit": "Bullshit",
        "quality": "Quality",
        "final": "Final Score",
        "rewrite_index": "Rewrite Index",
        "business_value": "Business Value",
        "wall_of_shame": "🚨 Wall of Shame",
        "ai_era_verdict": "🤖 AI Era Verdict",
        "most_irreplaceable": "Most Irreplaceable",
        "most_replaceable": "Most Replaceable",
        "team_future": "Team Future",
        "daily_roast": "🎤 Daily Roast",
        "closing_rant": "🎤 Linus Closing",
        "disclaimer": "This report is AI-generated for entertainment only. Not for performance evaluation. In the AI era, code volume ≠ contribution. Brains matter.",
    },
}


def generate_markdown_report(analysis: dict, lang: str = "zh") -> str:
    t = I18N.get(lang, I18N["en"])
    lines = []

    lines.append(f"# {t['title']}")
    lines.append("")
    lines.append(
        f"**{t['date']}**: {analysis.get('report_date', datetime.now().strftime('%Y-%m-%d'))}"
    )
    if analysis.get("team_vibe"):
        lines.append(f"**{t['team_vibe']}**: {analysis['team_vibe']}")
    if analysis.get("linus_mood"):
        lines.append(f"**{t['linus_mood']}**: {analysis['linus_mood']}")
    lines.append("")

    team = analysis.get("team_summary", {})
    if team:
        lines.append(f"## {t['team_summary']}")
        lines.append("")
        lines.append(
            f"| {'指标' if lang == 'zh' else 'Metric'} | {'数值' if lang == 'zh' else 'Value'} |"
        )
        lines.append("|------|------|")
        lines.append(f"| {t['total_commits']} | {team.get('total_commits', 0)} |")
        lines.append(
            f"| {t['real_work_score']} | {team.get('real_work_score', team.get('team_effort_score', 0))} |"
        )
        lines.append(f"| {t['bullshit_ratio']} | {team.get('bullshit_ratio', 'N/A')} |")
        lines.append(f"| {t['team_grade']} | {team.get('team_grade', 'N/A')} |")
        lines.append(f"| {t['mvp']} | {team.get('mvp', 'N/A')} |")
        lines.append("")

        if team.get("daily_vibe"):
            lines.append(f"> 💬 {team['daily_vibe']}")
            lines.append("")
        if team.get("linus_says"):
            lines.append(f'> 🔥 Linus: *"{team["linus_says"]}"*')
            lines.append("")

    leaderboard = analysis.get("leaderboard", [])
    if leaderboard:
        lines.append(f"## {t['leaderboard']}")
        lines.append("")

        for entry in leaderboard:
            rank = entry.get("rank", "?")
            rank_emoji = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, "🏅")

            lines.append(f"### {rank_emoji} #{rank} {entry.get('name', 'Unknown')}")
            lines.append("")

            grade = entry.get("grade", "")
            title = entry.get("title", "")
            award = entry.get("award", "")
            score = entry.get("final_score", entry.get("effort_score", 0))

            if title and award:
                lines.append(f"**{grade}** | {title} | *{award}*")
            elif title:
                lines.append(f"**{grade}** | {title}")
            else:
                lines.append(f"**{grade}**")
            lines.append("")
            lines.append(
                f"{t['score']}: **{score}** | {t['commits']}: {entry.get('commits', 0)} | {t['effective_lines']}: {entry.get('effective_lines', 0)}"
            )
            lines.append("")

            badges = entry.get("badges", [])
            if badges:
                lines.append(f"**{t['badges']}**: {' '.join(badges)}")
                lines.append("")

            if entry.get("summary"):
                lines.append(f"> 💬 {entry['summary']}")
            if entry.get("linus_review"):
                lines.append(f'> 🔥 Linus: *"{entry["linus_review"]}"*')

            if entry.get("ai_survivor_score") is not None:
                lines.append("")
                lines.append(
                    f"**{t['ai_survivor']}**: {entry['ai_survivor_score']}/100"
                )
                if entry.get("ai_verdict"):
                    lines.append(f"> 🤖 {entry['ai_verdict']}")
                if entry.get("future_advice"):
                    lines.append(f"> 💡 {entry['future_advice']}")

            if (
                entry.get("summary")
                or entry.get("linus_review")
                or entry.get("ai_survivor_score")
            ):
                lines.append("")

    commits = analysis.get("commits", [])
    if commits:
        lines.append(f"## {t['commit_details']}")
        lines.append("")

        for c in commits:
            quality_emoji = {
                "good": "✨",
                "acceptable": "👍",
                "poor": "😐",
                "shit": "💩",
            }.get(c.get("code_quality", ""), "📦")

            lines.append(
                f"### {quality_emoji} `{c.get('sha', 'N/A')[:8]}` - {c.get('author', 'Unknown')}"
            )
            lines.append("")

            rewrite_idx = c.get("rewrite_index")
            biz_value = c.get("business_value")

            if rewrite_idx and biz_value:
                lines.append(
                    f"{t['rewrite_index']}: {rewrite_idx}/5 | {t['business_value']}: {biz_value} | "
                    f"**{t['final']}: {c.get('final_score', 0)}**"
                )
            else:
                complexity = c.get("complexity", "")
                impact = c.get("impact", "")
                if complexity and impact:
                    lines.append(
                        f"{t['complexity']}: {complexity}/5 | {t['impact']}: {impact}/5 | "
                        f"**{t['final']}: {c.get('final_score', c.get('effort_score', 0))}**"
                    )
                else:
                    lines.append(
                        f"{t['substance']}: {c.get('substance_score', 0)} | "
                        f"{t['bullshit']}: {c.get('bullshit_score', 0)} | "
                        f"**{t['final']}: {c.get('final_score', 0)}**"
                    )
            lines.append("")

            if c.get("ai_could_write"):
                lines.append(f"> 🤖 {c['ai_could_write']}")
                lines.append("")

            if c.get("roast"):
                lines.append(f"> 💬 {c['roast']}")
            if c.get("linus_says"):
                lines.append(f'> 🔥 Linus: *"{c["linus_says"]}"*')
            if c.get("roast") or c.get("linus_says"):
                lines.append("")

            badges = c.get("badges", [])
            if badges:
                lines.append(f"🏅 {' '.join(badges)}")
                lines.append("")

    wall = analysis.get("wall_of_shame", [])
    if wall:
        lines.append(f"## {t['wall_of_shame']}")
        lines.append("")
        for item in wall:
            lines.append(f"- {item}")
        lines.append("")

    ai_verdict = analysis.get("ai_era_verdict", {})
    if ai_verdict:
        lines.append(f"## {t['ai_era_verdict']}")
        lines.append("")
        if ai_verdict.get("team_ai_survivor_score") is not None:
            lines.append(
                f"**{t['ai_survivor']}**: {ai_verdict['team_ai_survivor_score']}/100"
            )
        if ai_verdict.get("most_irreplaceable"):
            lines.append(
                f"**{t['most_irreplaceable']}**: {ai_verdict['most_irreplaceable']}"
            )
        if ai_verdict.get("most_replaceable"):
            lines.append(
                f"**{t['most_replaceable']}**: {ai_verdict['most_replaceable']}"
            )
        if ai_verdict.get("team_future"):
            lines.append(f"**{t['team_future']}**: {ai_verdict['team_future']}")
        lines.append("")
        if ai_verdict.get("linus_ai_rant"):
            lines.append(f'> 🔥 Linus: *"{ai_verdict["linus_ai_rant"]}"*')
            lines.append("")

    if analysis.get("daily_roast"):
        lines.append("---")
        lines.append("")
        lines.append(f"## {t['daily_roast']}")
        lines.append("")
        lines.append(f"*{analysis['daily_roast']}*")
        lines.append("")

    if analysis.get("closing_rant"):
        lines.append(f"## {t['closing_rant']}")
        lines.append("")
        lines.append(f"*{analysis['closing_rant']}*")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"*{t['disclaimer']}*")

    return "\n".join(lines)


def generate_html_report(analysis: dict, lang: str = "zh") -> str:
    md_content = generate_markdown_report(analysis, lang)
    html_lang = "zh-CN" if lang == "zh" else "en"
    title = "牛马鉴定报告" if lang == "zh" else "Code Commit Report"

    return f'''<!DOCTYPE html>
<html lang="{html_lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        h3 {{ color: #7f8c8d; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background: #f5f5f5; }}
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 10px 0;
            padding: 10px 20px;
            background: #f8f9fa;
            font-style: italic;
        }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
    </style>
</head>
<body>
    <pre style="white-space: pre-wrap;">{md_content}</pre>
</body>
</html>'''


def main():
    parser = argparse.ArgumentParser(description="Generate report from analysis JSON")
    parser.add_argument("analysis_file", help="Path to analysis.json (Claude output)")
    parser.add_argument(
        "--format", "-f", choices=["markdown", "html"], default="markdown"
    )
    parser.add_argument(
        "--lang", "-l", choices=["zh", "en"], default="zh", help="Output language"
    )
    parser.add_argument("--output", "-o", help="Output file path")

    args = parser.parse_args()

    with open(args.analysis_file, "r", encoding="utf-8") as f:
        analysis = json.load(f)

    if args.format == "html":
        content = generate_html_report(analysis, args.lang)
        ext = ".html"
    else:
        content = generate_markdown_report(analysis, args.lang)
        ext = ".md"

    if args.output:
        output_path = args.output
    else:
        output_path = args.analysis_file.replace(".json", f"_report{ext}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Report generated: {output_path}")


if __name__ == "__main__":
    main()
