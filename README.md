# Git Commit Analyzer - 牛马鉴定器 🐂🐴

用 AI 分析 git 提交，鉴定你今天是「夯」还是「拉完了」。

传统指标（行数、提交数）无法反映真实贡献。本工具用 AI 的代码理解能力，给出灵魂拷问的答案：**你今天到底卷没卷？**

## 评级体系

| 等级 | 称号 | 颁奖词 | Linus 说 |
|------|------|--------|----------|
| 🔥 夯 | 代码之神 | 建议申请调薪 | "Not bad." |
| 💎 顶级 | 团队支柱 | 老板看了直呼内行 | "Acceptable." |
| 👑 人上人 | 稳定输出 | 职场中坚力量 | "It works, I guess." |
| 🧍 NPC | 打工人 | 今天也是普通的一天 | "Do you even know what you're doing?" |
| 💀 拉完了 | 带薪摸鱼 | 明天记得努力 | "What the fuck is this shit?" |

## 安装

```bash
npx skills add shaoxyz/git-commit-analyzer

# ast-grep（可选，启用多语言代码分析）
npm i -g @ast-grep/cli
```

## Quick Start

```bash
SKILL_DIR=~/.claude/skills/git-commit-analyzer

# 获取 → 分析 → Prompt → Claude → 报告
python $SKILL_DIR/scripts/fetch_commits.py /path/to/repo --since "1 day ago" -o commits.json
python $SKILL_DIR/scripts/analyze_code.py commits.json
python $SKILL_DIR/scripts/generate_prompt.py commits.json > prompt.txt
# 发给 Claude，保存结果为 analysis.json
python $SKILL_DIR/scripts/generate_report.py analysis.json
```

## 文档

[完整文档 & 评分算法](./skills/git-commit-analyzer/SKILL.md)

## 重要声明 ⚠️

测不出来：花一天 debug 最后只改一行的痛、code review、带新人。

**当成团队娱乐工具，严禁用于绩效评估。**

## License

[MIT](./LICENSE)
