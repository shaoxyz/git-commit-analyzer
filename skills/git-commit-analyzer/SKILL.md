---
name: git-commit-analyzer
description: >
  Analyze git repository commits using AI to evaluate actual code contribution value, not just line counts.
  Use when users want to generate intelligent daily/weekly team development reports, understand what work
  was actually done in commits, assess code change complexity and impact, track project progress with
  meaningful insights, or identify high-impact or risky changes. Supports GitHub, GitLab, and local git repositories.
---

# Git Commit Analyzer - 牛马鉴定器 🐂🐴

用 AI 分析 git 提交，鉴定你今天是「夯」还是「拉完了」。

## 核心理念

传统指标（行数、提交数）无法反映真实贡献。本 skill 用 Claude 的代码理解能力，给出一个灵魂拷问的答案：**你今天到底卷没卷？**

评级体系：
- 🔥 **夯** - 神级输出，代码之神降临
- 💎 **顶级** - 硬核贡献，团队支柱
- 👑 **人上人** - 稳定发挥，值得信赖
- 🧍 **NPC** - 打卡上班，波澜不惊
- 💀 **拉完了** - 今天摸鱼实锤

## 脚本位置

安装后脚本位于 skill 目录下：
- 项目级安装: `.claude/skills/git-commit-analyzer/scripts/`
- 全局安装: `~/.claude/skills/git-commit-analyzer/scripts/`

## Quick Start

### 1. Fetch Commits

```bash
# 设置脚本路径 (根据你的安装位置调整)
SKILL_DIR=~/.claude/skills/git-commit-analyzer

# For local repo
python $SKILL_DIR/scripts/fetch_commits.py /path/to/repo --since "1 day ago" -o commits.json

# For GitHub (requires GITHUB_TOKEN env var)
python $SKILL_DIR/scripts/fetch_commits.py --github owner/repo --since "1 day ago" -o commits.json

# For GitLab (requires GITLAB_TOKEN env var)
python $SKILL_DIR/scripts/fetch_commits.py --gitlab project-id --since "1 day ago" -o commits.json
```

### 2. Generate Analysis Prompt

```bash
python $SKILL_DIR/scripts/generate_prompt.py commits.json > prompt.txt
```

Then send `prompt.txt` to Claude and save the JSON response as `analysis.json`.

### 3. Generate Report

```bash
python $SKILL_DIR/scripts/generate_report.py analysis.json
```

Output options:
- Markdown summary for team review (`--format markdown`)
- HTML report (`--format html`)

## Commit Evaluation Framework

For each commit, evaluate these dimensions (1-5 scale):

### Complexity Score (技术深度)
- **1**: 摸鱼级 (typo、配置、自动生成)
- **2**: 简单级 (改个变量名、小 UI 调整)
- **3**: 正常级 (新函数、明确的 bug 修复)
- **4**: 硬核级 (新功能、架构调整)
- **5**: 神仙级 (算法设计、系统级重构)

### Impact Score (影响范围)
- **1**: 自娱自乐 (测试、文档)
- **2**: 小打小闹 (单模块内部)
- **3**: 有点东西 (影响模块接口)
- **4**: 大动干戈 (跨模块、API 变更)
- **5**: 伤筋动骨 (核心基础设施)

## 牛马等级算法

```
effort_score = complexity × impact × type_multiplier

type_multiplier:
  - feature: 1.0
  - bugfix: 1.0 (救火级 bug: 1.3)
  - refactor: 0.9
  - chore: 0.5
  - docs: 0.3
```

### 每日总分 → 牛马等级

| 日总分 | 等级 | 称号 | 颁奖词 |
|--------|------|------|--------|
| ≥ 40 | 🔥 夯 | 代码之神 | 建议申请调薪 |
| 25-39 | 💎 顶级 | 团队支柱 | 老板看了直呼内行 |
| 15-24 | 👑 人上人 | 稳定输出 | 职场中坚力量 |
| 5-14 | 🧍 NPC | 打工人 | 今天也是普通的一天 |
| < 5 | 💀 拉完了 | 带薪摸鱼 | 明天记得努力 |

### 特殊成就徽章

- 🚀 **线上救火队长** - 修复了 P0/P1 级别 bug
- 🏗️ **基建狂魔** - 贡献了基础设施代码
- 📚 **文档侠** - 写了有意义的文档 (难得)
- 🧹 **屎山清洁工** - 清理了技术债务
- 💥 **删库跑路预备役** - 删除代码 > 新增代码 (可能是好事)
- 🎨 **像素眼** - 纯 UI/样式调整
- 🤖 **AI 的形状** - 代码看起来像 AI 写的

## Output Format

```json
{
  "report_date": "2024-01-15",
  "team_summary": {
    "total_commits": 23,
    "team_effort_score": 156,
    "team_grade": "💎 顶级",
    "mvp": "alice",
    "daily_vibe": "今天团队状态不错，产出硬核"
  },
  "leaderboard": [
    {
      "rank": 1,
      "name": "alice",
      "effort_score": 52,
      "grade": "🔥 夯",
      "title": "代码之神",
      "commits": 5,
      "badges": ["🚀 线上救火队长", "🏗️ 基建狂魔"],
      "summary": "今天单挑了整个支付模块重构，还顺手修了两个 P1 bug"
    },
    {
      "rank": 2,
      "name": "bob",
      "effort_score": 28,
      "grade": "💎 顶级",
      "title": "团队支柱",
      "commits": 8,
      "badges": ["📚 文档侠"],
      "summary": "完成了用户中心的前端开发，文档写得比代码还多"
    }
  ],
  "commits": [
    {
      "sha": "abc123",
      "author": "alice",
      "message": "fix: 紧急修复支付回调丢单问题",
      "type": "bugfix",
      "complexity": 4,
      "impact": 5,
      "effort_score": 26,
      "roast": "救火队长出动！这 bug 不修今晚别想睡",
      "badges": ["🚀 线上救火队长"]
    }
  ],
  "daily_roast": "alice 今天一个人把团队平均分拉高了 50%，其他人反思一下"
}
```

## 重要声明 ⚠️

### 这玩意儿测不出来的
- 花了一天 debug 最后只改一行的痛
- 开会、code review、带新人的隐形付出
- 那些尝试了 10 种方案最后失败的探索
- 读懂祖传代码所消耗的脑细胞

### 正确的打开方式
- 当成 **团队娱乐工具**，不是 KPI 考核
- 配合 daily standup 增加气氛
- 发现异常模式（连续摸鱼需要关怀）
- **严禁用于绩效评估** - 否则你会收获一堆刷 commit 的代码

### 老板须知
如果你想用这个来监控员工，建议先体验一下被 AI 评为「拉完了」的感觉。

## Configuration

See `references/config.md` for:
- Repository connection settings
- Analysis parameters customization  
- Report template options
- Integration with CI/CD pipelines
