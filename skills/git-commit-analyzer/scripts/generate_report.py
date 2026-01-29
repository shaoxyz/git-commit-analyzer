#!/usr/bin/env python3
"""
Generate formatted reports from analysis JSON output.
牛马鉴定报告生成器 🐂🐴
"""

import argparse
import json
from datetime import datetime

GRADES = [
    (40, "🔥 夯", "代码之神", "建议申请调薪"),
    (25, "💎 顶级", "团队支柱", "老板看了直呼内行"),
    (15, "👑 人上人", "稳定输出", "职场中坚力量"),
    (5, "🧍 NPC", "打工人", "今天也是普通的一天"),
    (0, "💀 拉完了", "带薪摸鱼", "明天记得努力"),
]

def get_grade(score: float) -> tuple[str, str, str]:
    """Get grade based on effort score."""
    for threshold, grade, title, comment in GRADES:
        if score >= threshold:
            return grade, title, comment
    return GRADES[-1][1:4]

def generate_markdown_report(analysis: dict) -> str:
    """Generate Markdown report from analysis data."""
    
    lines = []
    
    # Header
    lines.append("# 🐂🐴 今日牛马鉴定报告")
    lines.append("")
    lines.append(f"**日期**: {analysis.get('report_date', datetime.now().strftime('%Y-%m-%d'))}")
    lines.append("")
    
    # Team Summary
    team = analysis.get("team_summary", {})
    if team:
        lines.append("## 📊 团队总览")
        lines.append("")
        lines.append(f"| 指标 | 数值 |")
        lines.append("|------|------|")
        lines.append(f"| 总提交数 | {team.get('total_commits', 0)} |")
        lines.append(f"| 团队总分 | {team.get('team_effort_score', 0)} |")
        lines.append(f"| 团队评级 | {team.get('team_grade', '未评级')} |")
        lines.append(f"| 今日 MVP | {team.get('mvp', '无')} |")
        lines.append("")
        if team.get("daily_vibe"):
            lines.append(f"> {team['daily_vibe']}")
            lines.append("")
    
    # Leaderboard
    leaderboard = analysis.get("leaderboard", [])
    if leaderboard:
        lines.append("## 🏆 牛马排行榜")
        lines.append("")
        
        for entry in leaderboard:
            rank_emoji = {1: "🥇", 2: "🥈", 3: "🥉"}.get(entry.get("rank", 0), "🏅")
            
            lines.append(f"### {rank_emoji} #{entry.get('rank', '?')} {entry.get('name', 'Unknown')}")
            lines.append("")
            lines.append(f"**{entry.get('grade', '')}** | {entry.get('title', '')} | 得分: {entry.get('effort_score', 0)}")
            lines.append("")
            
            badges = entry.get("badges", [])
            if badges:
                lines.append(f"徽章: {' '.join(badges)}")
                lines.append("")
            
            if entry.get("summary"):
                lines.append(f"> {entry['summary']}")
                lines.append("")
    
    # By Contributor (fallback for old format)
    by_contributor = analysis.get("by_contributor", {})
    if by_contributor and not leaderboard:
        lines.append("## 👥 贡献者鉴定")
        lines.append("")
        lines.append("| 牛马 | 提交数 | 得分 | 等级 | 称号 |")
        lines.append("|------|--------|------|------|------|")
        
        sorted_contributors = sorted(
            by_contributor.items(),
            key=lambda x: x[1].get('total_effort_score', 0),
            reverse=True
        )
        
        for name, stats in sorted_contributors:
            score = stats.get('total_effort_score', 0)
            grade, title, _ = get_grade(score)
            lines.append(
                f"| {name} | {stats.get('commits', 0)} | "
                f"{score:.0f} | {grade} | {title} |"
            )
        lines.append("")
    
    # Commit Details
    commits = analysis.get("commits", [])
    if commits:
        lines.append("## 📝 提交明细")
        lines.append("")
        
        for c in commits:
            type_emoji = {
                "feature": "✨",
                "bugfix": "🐛",
                "refactor": "♻️",
                "chore": "🔧",
                "docs": "📚",
                "test": "🧪",
                "style": "💄"
            }.get(c.get("type", ""), "📦")
            
            lines.append(f"#### {type_emoji} `{c.get('sha', 'N/A')[:8]}` by {c.get('author', 'Unknown')}")
            lines.append("")
            lines.append(f"复杂度 {c.get('complexity', 0)}/5 × 影响 {c.get('impact', 0)}/5 = **{c.get('effort_score', 0):.1f}分**")
            lines.append("")
            
            if c.get("roast"):
                lines.append(f"> 💬 {c['roast']}")
                lines.append("")
            elif c.get("analysis"):
                lines.append(f"> {c['analysis']}")
                lines.append("")
            
            badges = c.get("badges", [])
            if badges:
                lines.append(f"🏅 {' '.join(badges)}")
                lines.append("")
    
    # Daily Roast
    if analysis.get("daily_roast"):
        lines.append("---")
        lines.append("")
        lines.append(f"### 🎤 今日毒舌")
        lines.append("")
        lines.append(f"*{analysis['daily_roast']}*")
        lines.append("")
    
    # Footer
    lines.append("---")
    lines.append("")
    lines.append("*本报告由 AI 生成，仅供娱乐，不代表任何绩效评价。如有雷同，纯属巧合。*")
    
    return "\n".join(lines)


def generate_html_report(analysis: dict) -> str:
    """Generate HTML report from analysis data."""
    
    md_content = generate_markdown_report(analysis)
    
    # Simple HTML wrapper with basic styling
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>代码提交分析报告</title>
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
        tr:hover {{ background: #f9f9f9; }}
        blockquote {{ 
            border-left: 4px solid #3498db; 
            margin: 10px 0; 
            padding: 10px 20px; 
            background: #f8f9fa;
        }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        .highlight {{ background: #fff3cd; padding: 10px; border-radius: 5px; }}
        .concern {{ background: #f8d7da; padding: 10px; border-radius: 5px; }}
    </style>
</head>
<body>
    <pre style="white-space: pre-wrap;">{md_content}</pre>
</body>
</html>'''
    
    return html


def main():
    parser = argparse.ArgumentParser(description="Generate report from analysis JSON")
    parser.add_argument("analysis_file", help="Path to analysis.json")
    parser.add_argument("--format", "-f", choices=["markdown", "html"], default="markdown")
    parser.add_argument("--output", "-o", help="Output file path")
    
    args = parser.parse_args()
    
    with open(args.analysis_file, "r", encoding="utf-8") as f:
        analysis = json.load(f)
    
    if args.format == "html":
        content = generate_html_report(analysis)
        ext = ".html"
    else:
        content = generate_markdown_report(analysis)
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
