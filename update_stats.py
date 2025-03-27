import os 
import requests
from collections import defaultdict
from datetime import datetime, timedelta

# GitHub API setup
GITHUB_USERNAME = "IsmailKemmoune"  # Replace with your GitHub username
TOKEN = os.getenv("GITHUB_TOKEN")  # GitHub token (auto-injected by Actions)

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Fetch commit activity (last 7 days)
def get_commit_activity():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/events/public"
    response = requests.get(url, headers=headers)
    events = response.json()
    
    commit_counts = defaultdict(int)
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    
    for event in events:
        if event["type"] == "PushEvent":
            date = datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ").weekday()
            commit_counts[days[date]] += 1
    
    total_commits = sum(commit_counts.values())
    active_days = [day for day, count in commit_counts.items() if count > 0]
    
    # Generate bar (scale to 10 chars for simplicity)
    bar_length = int(total_commits / 5)  # Adjust divisor for scaling
    bar = '█' * min(bar_length, 10) + '░' * (10 - min(bar_length, 10))
    
    return f"**GitHub Activity Stats**  \nLast 7 Days: {bar} {total_commits} commits  \nActive Days: {', '.join(active_days)}"

# Fetch top languages
def get_top_languages():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100"
    repos = requests.get(url, headers=headers).json()
    
    lang_stats = defaultdict(int)
    for repo in repos:
        if repo["language"]:
            lang_stats[repo["language"]] += 1
    
    total = sum(lang_stats.values())
    stats_text = "**Top Languages**  \n"
    
    for lang, count in sorted(lang_stats.items(), key=lambda x: -x[1]):
        percent = count / total * 100
        bar = '█' * int(percent // 10) + '░' * (10 - int(percent // 10))
        stats_text += f"{lang.ljust(12)} {bar} {int(percent)}%  \n"
    
    return stats_text

# Update README
def update_readme():
    stats_section = f"{get_commit_activity()}\n\n{get_top_languages()}"
    
    with open("README.md", "r") as f:
        readme = f.read()
    
    # Replace placeholder
    updated_readme = readme.replace(
        "<!--START_STATS-->", 
        f"<!--START_STATS-->\n{stats_section}\n<!--END_STATS-->"
    )
    
    with open("README.md", "w") as f:
        f.write(updated_readme)

if __name__ == "__main__":
    update_readme()
