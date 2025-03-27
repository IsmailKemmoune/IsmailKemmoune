import os
import requests
from collections import defaultdict
from datetime import datetime, timedelta

# GitHub API Setup
GITHUB_USERNAME = "IsmailKemmoune"
TOKEN = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {TOKEN}"}

def get_enhanced_stats():
    # Fetch data
    repos = requests.get(f"https://api.github.com/users/{GITHUB_USERNAME}/repos", headers=headers).json()
    events = requests.get(f"https://api.github.com/users/{GITHUB_USERNAME}/events", headers=headers).json()
    
    # Process languages
    lang_stats = defaultdict(int)
    for repo in repos:
        if repo["language"]:
            lang_stats[repo["language"]] += repo["stargazers_count"] + 1  # Weight by stars
    
    # Process activity
    commits_last_week = sum(1 for event in events if event["type"] == "PushEvent")
    starred_repos = len([event for event in events if event["type"] == "WatchEvent"])
    
    # Generate bars (20 chars max)
    def bar(percent):
        filled = '█' * int(percent / 5)
        return f"{filled.ljust(20)} {percent}%"
    
    # Build output
    stats = "### GitHub Analytics  \n\n"
    stats += f"**Weekly Coding Pulse**  \n"
    stats += f"`🌐 Total Dev Time`: {commits_last_week * 45}m  \n"  # Approx 45min per commit
    stats += f"`📌 Project Focus`: {'Web Dev' if 'JavaScript' in lang_stats else 'Other'}  \n"
    stats += f"`🚀 Productivity Streak`: {min(7, commits_last_week // 2)} days  \n\n"
    
    stats += "**Language Radar**  \n"
    for lang, count in sorted(lang_stats.items(), key=lambda x: -x[1]):
        percent = int(count / sum(lang_stats.values()) * 100)
        stats += f"{lang.ljust(12)} {bar(percent)}  \n"
    
    stats += "\n**Highlights**  \n"
    stats += f"`⭐ Starred Repos`: {starred_repos}  \n"
    stats += f"`🤝 PRs Merged`: {len([e for e in events if e.get('payload', {}).get('action') == 'closed' and 'pull_request' in e.get('payload', {})])}  \n"
    stats += f"`🐛 Issues Closed`: {len([e for e in events if e.get('payload', {}).get('action') == 'closed' and 'issue' in e.get('payload', {})]}  \n"
    
    return stats

# Update README
def update_readme():
    with open("README.md", "r") as f:
        readme = f.read()
    
    updated_readme = readme.replace(
        "<!--START_STATS-->", 
        f"<!--START_STATS-->\n{get_enhanced_stats()}\n<!--END_STATS-->"
    )
    
    with open("README.md", "w") as f:
        f.write(updated_readme)

if __name__ == "__main__":
    update_readme()
