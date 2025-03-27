import os
import requests
from collections import defaultdict

# GitHub API Setup
GITHUB_USERNAME = "IsmailKemmoune"
TOKEN = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {TOKEN}"}

def get_enhanced_stats():
    # Fetch data
    repos = requests.get(f"https://api.github.com/users/{GITHUB_USERNAME}/repos", headers=headers).json()
    
    # Process languages (filter out Python and C)
    lang_stats = defaultdict(int)
    for repo in repos:
        if repo["language"] and repo["language"] not in ["Python", "C"]:
            lang_stats[repo["language"]] += repo["stargazers_count"] + 1
    
    # Generate aligned bars (15 chars max)
    def bar(percent):
        filled = '█' * int(percent / 6.67)  # Scale to 15 chars for 100%
        return f"{filled.ljust(15)}"
    
    # Build output
    stats = "## GitHub Analytics\n\n"
    stats += "### Weekly Activity\n"
    stats += "- **Total Dev Time:** 180m  \n"
    stats += "- **Project Focus:** Web Dev  \n"
    stats += "- **Productivity Streak:** 2 days  \n\n"
    
    stats += "### Language Usage\n"
    for lang, count in sorted(lang_stats.items(), key=lambda x: -x[1]):
        percent = int(count / sum(lang_stats.values()) * 100)
        stats += f"| {lang.ljust(10)} | {bar(percent)} {percent}% |\n"
    
    return stats

def update_readme():
    with open("README.md", "r") as f:
        readme = f.read()
    
    # Remove old stats completely
    updated_readme = readme.split("<!--START_STATS-->")[0] + \
                   "<!--START_STATS-->\n" + \
                   get_enhanced_stats() + \
                   "\n<!--END_STATS-->" + \
                   readme.split("<!--END_STATS-->")[-1]
    
    with open("README.md", "w") as f:
        f.write(updated_readme)

if __name__ == "__main__":
    update_readme()
