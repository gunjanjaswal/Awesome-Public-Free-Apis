#!/usr/bin/env python3
"""
This script updates API data in the README.md file.
It fetches trending repositories, API status, and other information.
"""

import os
import re
import json
import datetime
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

def main():
    """Main function to update the README."""
    readme_path = "README.md"
    
    # Read the current README content
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()
    
    # Update trending repositories sections
    updated_content = update_trending_repositories_section(readme_content)
    
    # Write the updated content back to the README
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    print("README updated successfully.")

if __name__ == "__main__":
    main()
