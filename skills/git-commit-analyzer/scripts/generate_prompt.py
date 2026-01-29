#!/usr/bin/env python3
"""
Generate analysis prompt for Claude to evaluate commits.
Can be used standalone or integrated into automated pipelines.
"""

import argparse
import json
import sys

ANALYSIS_PROMPT_TEMPLATE = '''
你是一个「牛马鉴定师」，负责分析 git 提交并给出有趣但公正的评价。

## 今日提交数据
```json
{commits_json}
```

## 评估维度

### 1. 提交类型
分类: feature | bugfix | refactor | chore | docs | test | style

### 2. 复杂度 (1-5)
- 1: 摸鱼级 (typo、配置、自动生成)
- 2: 简单级 (改个变量名、调个参数)
- 3: 正常级 (新函数、明确的 bug 修复)
- 4: 硬核级 (新功能、架构调整)
- 5: 神仙级 (算法设计、系统级重构)

### 3. 影响范围 (1-5)
- 1: 自娱自乐 (测试、文档)
- 2: 小打小闹 (单模块内部)
- 3: 有点东西 (影响模块接口)
- 4: 大动干戈 (跨模块、API 变更)
- 5: 伤筋动骨 (核心基础设施)

### 4. 徽章系统
根据提交特征授予徽章:
- 🚀 线上救火队长 - 修了紧急 bug
- 🏗️ 基建狂魔 - 贡献基础设施
- 📚 文档侠 - 写了文档
- 🧹 屎山清洁工 - 清理技术债
- 💥 删库跑路预备役 - 删代码比写代码多
- 🎨 像素眼 - 纯 UI/样式调整
- 🤖 AI 的形状 - 代码风格疑似 AI 生成

## 牛马等级

effort_score = complexity × impact × type_multiplier
(feature=1.0, bugfix=1.0, refactor=0.9, chore=0.5, docs=0.3)

日总分 → 等级:
- ≥40: 🔥 夯 (代码之神)
- 25-39: 💎 顶级 (团队支柱)
- 15-24: 👑 人上人 (稳定输出)
- 5-14: 🧍 NPC (打工人)
- <5: 💀 拉完了 (带薪摸鱼)

## 输出格式

返回 JSON:

```json
{{
  "report_date": "YYYY-MM-DD",
  "team_summary": {{
    "total_commits": N,
    "team_effort_score": N,
    "team_grade": "等级 emoji + 名称",
    "mvp": "今日 MVP 姓名",
    "daily_vibe": "一句话描述今天团队状态，要有趣"
  }},
  "leaderboard": [
    {{
      "rank": 1,
      "name": "姓名",
      "effort_score": N,
      "grade": "🔥 夯",
      "title": "代码之神",
      "commits": N,
      "badges": ["徽章列表"],
      "summary": "一句话总结此人今日贡献，要有点毒舌但友善"
    }}
  ],
  "commits": [
    {{
      "sha": "短sha",
      "author": "作者",
      "type": "类型",
      "complexity": N,
      "impact": N,
      "effort_score": N,
      "roast": "一句话点评这个提交，可以幽默毒舌",
      "badges": ["获得的徽章"]
    }}
  ],
  "daily_roast": "今日总结毒舌，比如吐槽摸鱼的人或者夸赞卷王"
}}
```

要求:
1. 评分要客观公正，基于实际代码变更
2. 点评要有趣但不伤人，适合团队分享
3. 善用 emoji 增加趣味性
4. daily_roast 要犀利但友善
'''

def generate_prompt(commits_file: str, max_commits: int = 50) -> str:
    """Generate analysis prompt from commits JSON file."""
    
    with open(commits_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    commits = data.get("commits", [])[:max_commits]
    
    # Prepare simplified commits for the prompt (reduce diff size)
    simplified_commits = []
    for c in commits:
        simplified = {
            "sha": c["sha"][:8],
            "author": c["author"]["name"],
            "date": c["date"],
            "message": c["message"],
            "stats": c["stats"],
            "changed_files": c["changed_files"],
            # Truncate diff to reasonable size per commit
            "diff": c.get("diff", "")[:3000] + ("..." if len(c.get("diff", "")) > 3000 else "")
        }
        simplified_commits.append(simplified)
    
    commits_json = json.dumps({
        "source": data.get("source"),
        "period": {"since": data.get("since"), "until": data.get("until")},
        "commits": simplified_commits
    }, indent=2, ensure_ascii=False)
    
    return ANALYSIS_PROMPT_TEMPLATE.format(commits_json=commits_json)

def main():
    parser = argparse.ArgumentParser(description="Generate analysis prompt for commits")
    parser.add_argument("commits_file", help="Path to commits.json")
    parser.add_argument("--max-commits", type=int, default=50, help="Max commits to include")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    
    args = parser.parse_args()
    
    prompt = generate_prompt(args.commits_file, args.max_commits)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(prompt)
        print(f"Prompt written to {args.output}", file=sys.stderr)
    else:
        print(prompt)

if __name__ == "__main__":
    main()
