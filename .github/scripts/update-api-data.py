#!/usr/bin/env python3
"""
This script updates API data in the README.md file.
It fetches trending repositories, API status, and other information.
It also updates all date references in the README.md file.
"""

import os
import re
import json
import datetime
from datetime import timedelta
import requests
from bs4 import BeautifulSoup

def get_trending_repositories(category="api", limit=8):
    """
    Fetch trending GitHub repositories related to APIs.
    """
    try:
        # GitHub trending API URL (using GitHub Search API)
        url = f"https://api.github.com/search/repositories?q={category}+sort:stars&per_page={limit}"
        
        headers = {}
        if "GITHUB_TOKEN" in os.environ:
            headers["Authorization"] = f"token {os.environ['GITHUB_TOKEN']}"
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if "items" not in data:
            print(f"Error fetching trending repositories: {data.get('message', 'Unknown error')}")
            return []
        
        repos = []
        for repo in data["items"]:
            repos.append({
                "name": repo["full_name"],
                "url": repo["html_url"],
                "description": (repo["description"] or "")[:100] + "..." if (repo["description"] or "") and len(repo["description"]) > 100 else (repo["description"] or ""),
                "stars": f"{round(repo['stargazers_count']/1000, 1)}k" if repo["stargazers_count"] >= 1000 else str(repo["stargazers_count"]),
                "language": repo["language"] or "Unknown"
            })
        
        return repos
    except Exception as e:
        print(f"Error fetching trending repositories: {str(e)}")
        return []

def update_trending_repositories_section(readme_content):
    """
    Update the trending repositories section in the README.
    """
    # Get trending API repositories
    api_repos = get_trending_repositories(category="api", limit=6)
    
    # Get general trending repositories related to APIs
    general_repos = get_trending_repositories(category="rest+api", limit=8)
    
    # Current date for the "last updated" text
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    
    # Update API repositories section
    api_repos_md = "\n".join([
        f"| [{repo['name']}]({repo['url']}) | {repo['description']} | {repo['stars']} | {repo['language']} |"
        for repo in api_repos
    ])
    
    api_repos_section = f"""## :rocket: Trending GitHub API Repositories

This section is automatically updated daily with trending API-specific repositories from GitHub. These repositories focus specifically on API development, documentation, and tooling.

| Repository | Description | Stars | Language |
| --- | --- | --- | --- |
{api_repos_md}

_Last updated: {current_date}_
"""
    
    # Update general repositories section
    general_repos_md = "\n".join([
        f"| [{repo['name']}]({repo['url']}) | {repo['description']} | {repo['stars']} | {repo['language']} |"
        for repo in general_repos
    ])
    
    general_repos_section = f"""## :rocket: Trending GitHub Repositories

This section is automatically updated daily with trending API-related repositories from GitHub. Discover what the community is building and using right now!

| Repository | Description | Stars | Language |
| --- | --- | --- | --- |
{general_repos_md}

_Last updated: {current_date}_
"""
    
    # Replace the existing sections with the new content
    pattern_api = r"## :rocket: Trending GitHub API Repositories.*?_Last updated:.*?_"
    pattern_general = r"## :rocket: Trending GitHub Repositories.*?_Last updated:.*?_"
    
    readme_content = re.sub(pattern_api, api_repos_section, readme_content, flags=re.DOTALL)
    readme_content = re.sub(pattern_general, general_repos_section, readme_content, flags=re.DOTALL)
    
    return readme_content

def update_schedule_dates(readme_content):
    """
    Update the API Categories last updated date and the next scheduled dates.
    """
    current_date = datetime.datetime.now()
    current_date_str = current_date.strftime("%B %d, %Y")
    
    # Update API Categories last updated date
    api_categories_pattern = r"_API Categories last updated: .*?_"
    readme_content = re.sub(api_categories_pattern, f"_API Categories last updated: {current_date_str}_", readme_content)
    
    # Calculate next scheduled dates
    # Weekly API Status Checks (every Sunday)
    next_sunday = current_date + timedelta((6 - current_date.weekday()) % 7)
    next_sunday_str = next_sunday.strftime("%B %d, %Y")
    
    # Enhanced API Discovery (every Monday)
    next_monday = current_date + timedelta((7 - current_date.weekday()) % 7)
    next_monday_str = next_monday.strftime("%B %d, %Y")
    
    # Monthly API Discovery (1st of each month)
    if current_date.day == 1:
        next_month = current_date.replace(day=1) + timedelta(days=32)
        next_month = next_month.replace(day=1)
    else:
        next_month = current_date.replace(day=1) + timedelta(days=32)
        next_month = next_month.replace(day=1)
    next_month_str = next_month.strftime("%B %d, %Y")
    
    # Update schedule dates
    weekly_check_pattern = r"Weekly API Status Checks \(Next: .*?\)"
    enhanced_discovery_pattern = r"Enhanced API Discovery \(Next: .*?\)"
    monthly_discovery_pattern = r"Monthly API Discovery \(Next: .*?\)"
    
    readme_content = re.sub(weekly_check_pattern, f"Weekly API Status Checks (Next: {next_sunday_str})", readme_content)
    readme_content = re.sub(enhanced_discovery_pattern, f"Enhanced API Discovery (Next: {next_monday_str})", readme_content)
    readme_content = re.sub(monthly_discovery_pattern, f"Monthly API Discovery (Next: {next_month_str})", readme_content)
    
    return readme_content

def main():
    """Main function to update the README."""
    readme_path = "README.md"
    
    # Read the current README content
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()
    
    # Update trending repositories sections
    updated_content = update_trending_repositories_section(readme_content)
    
    # Update schedule dates
    updated_content = update_schedule_dates(updated_content)
    
    # Write the updated content back to the README
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    print("README updated successfully.")

if __name__ == "__main__":
    main()
