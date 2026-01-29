#!/usr/bin/env python3
"""
AST-based code analysis using ast-grep (sg).
Multi-language support with pattern-based detection.
"""

import json
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class AstPattern:
    name: str
    pattern: str
    lang: str
    severity: str  # "error", "warning", "info"
    category: str  # "smell", "ai_generated", "antipattern", "security"
    description: str
    bullshit_score: int = 0


LANG_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
    ".c": "c",
    ".cpp": "cpp",
    ".rb": "ruby",
    ".php": "php",
    ".swift": "swift",
    ".kt": "kotlin",
}

# fmt: off
DETECTION_RULES: list[AstPattern] = [
    # === Code Smells ===
    AstPattern(
        name="empty_catch",
        pattern="catch ($ERR) { }",
        lang="javascript,typescript,tsx,java",
        severity="error",
        category="smell",
        description="Empty catch block - swallowing errors is bad",
        bullshit_score=10,
    ),
    AstPattern(
        name="empty_except",
        pattern="except $E: pass",
        lang="python",
        severity="error",
        category="smell",
        description="Empty except block - swallowing errors",
        bullshit_score=10,
    ),
    AstPattern(
        name="console_log",
        pattern="console.log($$$)",
        lang="javascript,typescript,tsx",
        severity="warning",
        category="smell",
        description="console.log left in code",
        bullshit_score=2,
    ),
    AstPattern(
        name="print_debug",
        pattern="print($$$)",
        lang="python",
        severity="info",
        category="smell",
        description="print() statement - might be debug code",
        bullshit_score=1,
    ),
    AstPattern(
        name="debugger_statement",
        pattern="debugger",
        lang="javascript,typescript,tsx",
        severity="error",
        category="smell",
        description="debugger statement left in code",
        bullshit_score=5,
    ),
    AstPattern(
        name="todo_comment",
        pattern="// TODO: $$$",
        lang="javascript,typescript,tsx,java,go,rust,c,cpp",
        severity="info",
        category="smell",
        description="TODO comment - unfinished work",
        bullshit_score=1,
    ),
    
    # === Anti-patterns ===
    AstPattern(
        name="nested_ternary",
        pattern="$A ? $B : $C ? $D : $E",
        lang="javascript,typescript,tsx",
        severity="warning",
        category="antipattern",
        description="Nested ternary - hard to read",
        bullshit_score=3,
    ),
    AstPattern(
        name="any_type",
        pattern=": any",
        lang="typescript,tsx",
        severity="warning",
        category="antipattern",
        description="Using 'any' type defeats TypeScript purpose",
        bullshit_score=5,
    ),
    AstPattern(
        name="ts_ignore",
        pattern="// @ts-ignore",
        lang="typescript,tsx",
        severity="error",
        category="antipattern",
        description="@ts-ignore - suppressing type errors",
        bullshit_score=8,
    ),
    AstPattern(
        name="eslint_disable",
        pattern="// eslint-disable",
        lang="javascript,typescript,tsx",
        severity="warning",
        category="antipattern",
        description="eslint-disable - suppressing lint errors",
        bullshit_score=3,
    ),
    
    # === AI-Generated Code Patterns ===
    AstPattern(
        name="verbose_if_else_return",
        pattern="if ($COND) { return true; } else { return false; }",
        lang="javascript,typescript,tsx,java",
        severity="info",
        category="ai_generated",
        description="Verbose if-else return - could be 'return $COND'",
        bullshit_score=2,
    ),
    AstPattern(
        name="redundant_else",
        pattern="if ($COND) { return $A; } else { $$$B }",
        lang="javascript,typescript,tsx",
        severity="info",
        category="ai_generated",
        description="Redundant else after return",
        bullshit_score=1,
    ),
    
    # === Security ===
    AstPattern(
        name="eval_usage",
        pattern="eval($$$)",
        lang="javascript,typescript,tsx,python",
        severity="error",
        category="security",
        description="eval() is dangerous",
        bullshit_score=15,
    ),
    AstPattern(
        name="innerhtml",
        pattern="$EL.innerHTML = $$$",
        lang="javascript,typescript,tsx",
        severity="error",
        category="security",
        description="innerHTML assignment - XSS risk",
        bullshit_score=10,
    ),
    AstPattern(
        name="hardcoded_secret",
        pattern='$VAR = "$SECRET"',
        lang="python,javascript,typescript",
        severity="error",
        category="security",
        description="Possible hardcoded secret",
        bullshit_score=20,
    ),
]
# fmt: on


def check_ast_grep_installed() -> bool:
    return shutil.which("sg") is not None


def get_lang_from_file(filepath: str) -> str | None:
    ext = Path(filepath).suffix.lower()
    return LANG_MAP.get(ext)


def run_ast_grep(
    pattern: str, lang: str, code: str, filepath: str = "code"
) -> list[dict]:
    """Run ast-grep pattern match on code snippet."""
    if not check_ast_grep_installed():
        return []

    with tempfile.TemporaryDirectory() as tmpdir:
        ext_map = {v: k for k, v in LANG_MAP.items()}
        ext = ext_map.get(lang, ".txt")
        tmp_file = Path(tmpdir) / f"code{ext}"
        tmp_file.write_text(code, encoding="utf-8")

        try:
            result = subprocess.run(
                ["sg", "--pattern", pattern, "--lang", lang, "--json", str(tmp_file)],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0 and result.stdout.strip():
                return json.loads(result.stdout)
        except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
            pass

    return []


def analyze_code_with_ast_grep(code: str, filepath: str) -> dict:
    """Analyze code using ast-grep patterns."""
    lang = get_lang_from_file(filepath)
    if not lang:
        return {"supported": False, "lang": None, "matches": [], "total_bullshit": 0}

    if not check_ast_grep_installed():
        return {
            "supported": True,
            "lang": lang,
            "matches": [],
            "total_bullshit": 0,
            "warning": "ast-grep (sg) not installed - run: npm i -g @ast-grep/cli",
        }

    matches = []
    total_bullshit = 0

    for rule in DETECTION_RULES:
        if lang not in rule.lang.split(","):
            continue

        results = run_ast_grep(rule.pattern, lang, code, filepath)
        for match in results:
            matches.append(
                {
                    "rule": rule.name,
                    "category": rule.category,
                    "severity": rule.severity,
                    "description": rule.description,
                    "line": match.get("range", {}).get("start", {}).get("line", 0),
                    "text": match.get("text", "")[:100],
                }
            )
            total_bullshit += rule.bullshit_score

    return {
        "supported": True,
        "lang": lang,
        "matches": matches,
        "total_bullshit": total_bullshit,
        "issues_by_category": categorize_matches(matches),
    }


def categorize_matches(matches: list[dict]) -> dict:
    """Group matches by category."""
    categories = {}
    for m in matches:
        cat = m["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(m)
    return categories


def analyze_diff_with_ast_grep(diff_files: list[dict]) -> dict:
    """Analyze all files in a diff using ast-grep."""
    all_matches = []
    total_bullshit = 0
    files_analyzed = 0
    unsupported_files = 0

    for file_info in diff_files:
        filepath = file_info.get("path", "")
        added_lines = file_info.get("added", [])

        if not added_lines:
            continue

        code = "\n".join(added_lines)
        result = analyze_code_with_ast_grep(code, filepath)

        if not result.get("supported"):
            unsupported_files += 1
            continue

        files_analyzed += 1
        total_bullshit += result.get("total_bullshit", 0)

        for match in result.get("matches", []):
            match["file"] = filepath
            all_matches.append(match)

    return {
        "files_analyzed": files_analyzed,
        "unsupported_files": unsupported_files,
        "total_matches": len(all_matches),
        "total_bullshit_from_ast": total_bullshit,
        "matches": all_matches,
        "summary": summarize_issues(all_matches),
    }


def summarize_issues(matches: list[dict]) -> dict:
    """Create summary of detected issues."""
    by_severity = {"error": 0, "warning": 0, "info": 0}
    by_category = {"smell": 0, "antipattern": 0, "ai_generated": 0, "security": 0}
    by_rule = {}

    for m in matches:
        by_severity[m.get("severity", "info")] += 1
        by_category[m.get("category", "smell")] += 1
        rule = m.get("rule", "unknown")
        by_rule[rule] = by_rule.get(rule, 0) + 1

    return {
        "by_severity": by_severity,
        "by_category": by_category,
        "by_rule": by_rule,
        "top_issues": sorted(by_rule.items(), key=lambda x: -x[1])[:5],
    }


def get_linus_comments_for_issues(matches: list[dict]) -> list[str]:
    """Generate Linus-style comments for detected issues."""
    comments = []

    issue_comments = {
        "empty_catch": "Empty catch block? Are you fucking kidding me? That's not error handling, that's error hiding.",
        "empty_except": "except: pass? This is not Python, this is a fucking crime against debugging.",
        "console_log": "console.log in production code? What is this, a debugging session from 2010?",
        "debugger_statement": "You left a debugger statement? Were you born yesterday?",
        "any_type": "Using 'any' in TypeScript? Then why the fuck are you using TypeScript at all?",
        "ts_ignore": "@ts-ignore is not a solution, it's admitting defeat.",
        "eval_usage": "eval()? EVAL?! This isn't the 90s. Learn to write proper code.",
        "innerhtml": "innerHTML assignment? Hello XSS my old friend...",
        "nested_ternary": "Nested ternaries? I see you hate the person who maintains this code. Including yourself.",
        "verbose_if_else_return": "if (x) return true else return false? Just return x, you absolute donut.",
    }

    seen_rules = set()
    for m in matches:
        rule = m.get("rule", "")
        if rule in issue_comments and rule not in seen_rules:
            comments.append(issue_comments[rule])
            seen_rules.add(rule)

    return comments


if __name__ == "__main__":
    if check_ast_grep_installed():
        print("✓ ast-grep (sg) is installed")

        test_code = """
function test() {
    try {
        doSomething();
    } catch (e) { }
    
    console.log("debug");
    
    if (x) {
        return true;
    } else {
        return false;
    }
}
"""
        result = analyze_code_with_ast_grep(test_code, "test.ts")
        print(f"\nTest analysis: {json.dumps(result, indent=2)}")
    else:
        print("✗ ast-grep (sg) not installed")
        print("  Install: npm i -g @ast-grep/cli")
        print("  Or: brew install ast-grep")
