# Git Commit Analyzer - 牛马鉴定器 🐂🐴

用 AI 分析 git 提交，鉴定你今天是「夯」还是「拉完了」。

传统指标（行数、提交数）无法反映真实贡献。本工具用 AI 的代码理解能力，给出一个灵魂拷问的答案：**你今天到底卷没卷？**

## 评级体系

| 等级 | 称号 | 颁奖词 |
|------|------|--------|
| 🔥 夯 | 代码之神 | 建议申请调薪 |
| 💎 顶级 | 团队支柱 | 老板看了直呼内行 |
| 👑 人上人 | 稳定输出 | 职场中坚力量 |
| 🧍 NPC | 打工人 | 今天也是普通的一天 |
| 💀 拉完了 | 带薪摸鱼 | 明天记得努力 |

## 安装

### 方式一：通过 skills.sh（推荐）

```bash
npx skills add shaoxyz/git-commit-analyzer
```

### 方式二：手动安装

```bash
git clone https://github.com/shaoxyz/git-commit-analyzer.git
cp -r git-commit-analyzer/skills/git-commit-analyzer ~/.claude/skills/
```

## Quick Start

```bash
# 设置脚本路径
SKILL_DIR=~/.claude/skills/git-commit-analyzer

# 1. 获取提交记录
python $SKILL_DIR/scripts/fetch_commits.py /path/to/repo --since "1 day ago" -o commits.json

# GitHub (需要 GITHUB_TOKEN)
python $SKILL_DIR/scripts/fetch_commits.py --github owner/repo --since "1 day ago" -o commits.json

# 2. 生成分析 prompt
python $SKILL_DIR/scripts/generate_prompt.py commits.json > prompt.txt

# 3. 发给 Claude，保存 JSON 结果为 analysis.json

# 4. 生成报告
python $SKILL_DIR/scripts/generate_report.py analysis.json
```

## 文档

- [完整文档 & 评分算法](./skills/git-commit-analyzer/SKILL.md)
- [配置参考](./skills/git-commit-analyzer/references/config.md)

## 重要声明 ⚠️

这玩意儿测不出来：花一天 debug 最后只改一行的痛、开会/code review/带新人的隐形付出。

**正确打开方式**：当成团队娱乐工具，配合 daily standup 增加气氛。**严禁用于绩效评估**。

## License

[MIT](./LICENSE)
