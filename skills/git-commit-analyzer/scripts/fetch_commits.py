#!/usr/bin/env python3
"""
Fetch git commits from local repository, GitHub, or GitLab.
Outputs structured JSON for AI analysis.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from typing import Optional

def run_git_command(args: list[str], cwd: str) -> str:
    """Execute git command and return output."""
    result = subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Git command failed: {result.stderr}")
    return result.stdout

def fetch_local_commits(repo_path: str, since: str, until: Optional[str] = None) -> list[dict]:
    """Fetch commits from local git repository."""
    
    # Build git log command
    log_format = "--pretty=format:%H|%an|%ae|%aI|%s"
    args = ["log", log_format, f"--since={since}"]
    if until:
        args.append(f"--until={until}")
    
    output = run_git_command(args, repo_path)
    if not output.strip():
        return []
    
    commits = []
    for line in output.strip().split("\n"):
        parts = line.split("|", 4)
        if len(parts) != 5:
            continue
        
        sha, author_name, author_email, date, message = parts
        
        # Get diff for this commit
        diff = run_git_command(["show", sha, "--stat", "--patch"], repo_path)
        
        # Get changed files
        files_output = run_git_command(["show", sha, "--name-status", "--pretty=format:"], repo_path)
        changed_files = []
        for file_line in files_output.strip().split("\n"):
            if file_line.strip():
                parts = file_line.split("\t")
                if len(parts) >= 2:
                    changed_files.append({
                        "status": parts[0],
                        "path": parts[-1]
                    })
        
        # Get line stats
        numstat = run_git_command(["show", sha, "--numstat", "--pretty=format:"], repo_path)
        additions = 0
        deletions = 0
        for stat_line in numstat.strip().split("\n"):
            if stat_line.strip():
                parts = stat_line.split("\t")
                if len(parts) >= 2:
                    try:
                        additions += int(parts[0]) if parts[0] != "-" else 0
                        deletions += int(parts[1]) if parts[1] != "-" else 0
                    except ValueError:
                        pass
        
        commits.append({
            "sha": sha,
            "author": {
                "name": author_name,
                "email": author_email
            },
            "date": date,
            "message": message,
            "diff": diff,
            "changed_files": changed_files,
            "stats": {
                "additions": additions,
                "deletions": deletions,
                "files_changed": len(changed_files)
            }
        })
    
    return commits

def fetch_github_commits(repo: str, since: str, until: Optional[str] = None) -> list[dict]:
    """Fetch commits from GitHub repository using API."""
    import urllib.request
    import urllib.parse
    
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable required for GitHub access")
    
    # Parse since date
    base_url = f"https://api.github.com/repos/{repo}/commits"
    params = {"since": since}
    if until:
        params["until"] = until
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    
    with urllib.request.urlopen(req) as response:
        commits_data = json.loads(response.read().decode())
    
    commits = []
    for commit_info in commits_data:
        sha = commit_info["sha"]
        
        # Fetch detailed commit info with diff
        detail_url = f"https://api.github.com/repos/{repo}/commits/{sha}"
        req = urllib.request.Request(detail_url)
        req.add_header("Authorization", f"token {token}")
        req.add_header("Accept", "application/vnd.github.v3.diff")
        
        with urllib.request.urlopen(req) as response:
            diff = response.read().decode()
        
        # Fetch commit details
        req = urllib.request.Request(detail_url)
        req.add_header("Authorization", f"token {token}")
        req.add_header("Accept", "application/vnd.github.v3+json")
        
        with urllib.request.urlopen(req) as response:
            detail = json.loads(response.read().decode())
        
        commits.append({
            "sha": sha,
            "author": {
                "name": commit_info["commit"]["author"]["name"],
                "email": commit_info["commit"]["author"]["email"]
            },
            "date": commit_info["commit"]["author"]["date"],
            "message": commit_info["commit"]["message"],
            "diff": diff,
            "changed_files": [
                {"status": f["status"], "path": f["filename"]}
                for f in detail.get("files", [])
            ],
            "stats": {
                "additions": detail["stats"]["additions"],
                "deletions": detail["stats"]["deletions"],
                "files_changed": len(detail.get("files", []))
            }
        })
    
    return commits

def fetch_gitlab_commits(project_id: str, since: str, until: Optional[str] = None) -> list[dict]:
    """Fetch commits from GitLab repository using API."""
    import urllib.request
    import urllib.parse
    
    token = os.environ.get("GITLAB_TOKEN")
    gitlab_url = os.environ.get("GITLAB_URL", "https://gitlab.com")
    
    if not token:
        raise ValueError("GITLAB_TOKEN environment variable required for GitLab access")
    
    # URL encode the project ID (could be namespace/project)
    encoded_project = urllib.parse.quote(project_id, safe="")
    
    base_url = f"{gitlab_url}/api/v4/projects/{encoded_project}/repository/commits"
    params = {"since": since}
    if until:
        params["until"] = until
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    req = urllib.request.Request(url)
    req.add_header("PRIVATE-TOKEN", token)
    
    with urllib.request.urlopen(req) as response:
        commits_data = json.loads(response.read().decode())
    
    commits = []
    for commit_info in commits_data:
        sha = commit_info["id"]
        
        # Fetch diff
        diff_url = f"{gitlab_url}/api/v4/projects/{encoded_project}/repository/commits/{sha}/diff"
        req = urllib.request.Request(diff_url)
        req.add_header("PRIVATE-TOKEN", token)
        
        with urllib.request.urlopen(req) as response:
            diff_data = json.loads(response.read().decode())
        
        # Build diff string
        diff_lines = []
        for file_diff in diff_data:
            diff_lines.append(f"--- a/{file_diff.get('old_path', '')}")
            diff_lines.append(f"+++ b/{file_diff.get('new_path', '')}")
            diff_lines.append(file_diff.get("diff", ""))
        diff = "\n".join(diff_lines)
        
        # Calculate stats
        additions = sum(d.get("diff", "").count("\n+") for d in diff_data)
        deletions = sum(d.get("diff", "").count("\n-") for d in diff_data)
        
        commits.append({
            "sha": sha,
            "author": {
                "name": commit_info["author_name"],
                "email": commit_info["author_email"]
            },
            "date": commit_info["authored_date"],
            "message": commit_info["message"],
            "diff": diff,
            "changed_files": [
                {"status": "M", "path": d["new_path"]}
                for d in diff_data
            ],
            "stats": {
                "additions": additions,
                "deletions": deletions,
                "files_changed": len(diff_data)
            }
        })
    
    return commits

def main():
    parser = argparse.ArgumentParser(description="Fetch git commits for AI analysis")
    parser.add_argument("repo_path", nargs="?", help="Local repository path")
    parser.add_argument("--github", help="GitHub repository (owner/repo)")
    parser.add_argument("--gitlab", help="GitLab project ID or path")
    parser.add_argument("--since", required=True, help="Fetch commits since (e.g., '1 day ago', '2024-01-01')")
    parser.add_argument("--until", help="Fetch commits until (optional)")
    parser.add_argument("--output", "-o", default="commits.json", help="Output file path")
    
    args = parser.parse_args()
    
    # Determine source and fetch commits
    if args.github:
        print(f"Fetching commits from GitHub: {args.github}")
        commits = fetch_github_commits(args.github, args.since, args.until)
    elif args.gitlab:
        print(f"Fetching commits from GitLab: {args.gitlab}")
        commits = fetch_gitlab_commits(args.gitlab, args.since, args.until)
    elif args.repo_path:
        print(f"Fetching commits from local repo: {args.repo_path}")
        commits = fetch_local_commits(args.repo_path, args.since, args.until)
    else:
        parser.error("Must specify repo_path, --github, or --gitlab")
    
    # Build output
    output = {
        "fetched_at": datetime.now().isoformat(),
        "source": args.github or args.gitlab or args.repo_path,
        "since": args.since,
        "until": args.until,
        "commit_count": len(commits),
        "commits": commits
    }
    
    # Write output
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Fetched {len(commits)} commits -> {args.output}")

if __name__ == "__main__":
    main()
