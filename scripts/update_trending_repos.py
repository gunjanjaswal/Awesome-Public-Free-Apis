#!/usr/bin/env python3
"""
GitHub Trending Repositories Updater

This script fetches trending API-related repositories from GitHub and updates the README.md file
with the latest trending repositories.
"""

import json
import os
import re
import requests
import datetime
from bs4 import BeautifulSoup
import markdown
from typing import Dict, List, Any, Optional

# Constants
README_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')
REQUEST_TIMEOUT = 15  # seconds
MAX_REPOS = 10  # Maximum number of repositories to display
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'


def fetch_trending_repos(language: str = None, time_period: str = 'daily') -> List[Dict[str, Any]]:
    """
    Fetch trending repositories from GitHub.
    
    Args:
        language: Optional programming language filter
        time_period: Time period for trending repos ('daily', 'weekly', or 'monthly')
    
    Returns:
        List of trending repositories
    """
    trending_repos = []
    
    # Construct the URL for GitHub trending
    url = 'https://github.com/trending'
    if language:
        url += f'/{language}'
    if time_period:
        url += f'?since={time_period}'
    
    headers = {'User-Agent': USER_AGENT}
    
    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            print(f"Failed to fetch trending repositories: {response.status_code}")
            return trending_repos
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find repository articles
        repo_articles = soup.select('article.Box-row')
        
        for article in repo_articles:
            try:
                # Extract repository name and owner
                repo_link = article.select_one('h2 a')
                if not repo_link:
                    continue
                
                repo_path = repo_link.get('href', '').strip('/')
                if not repo_path or '/' not in repo_path:
                    continue
                
                owner, repo_name = repo_path.split('/')
                
                # Extract description
                description_elem = article.select_one('p')
                description = description_elem.text.strip() if description_elem else ""
                
                # Extract stars
                stars_elem = article.select_one('a.Link--muted:has(svg[aria-label="star"])')
                stars_text = stars_elem.text.strip() if stars_elem else "0"
                stars = parse_stars(stars_text)
                
                # Extract language
                language_elem = article.select_one('span[itemprop="programmingLanguage"]')
                language = language_elem.text.strip() if language_elem else "Unknown"
                
                # Only include API-related repositories
                if is_api_related(repo_name, description):
                    trending_repos.append({
                        'owner': owner,
                        'name': repo_name,
                        'full_name': f"{owner}/{repo_name}",
                        'description': description,
                        'stars': stars,
                        'language': language,
                        'url': f"https://github.com/{repo_path}"
                    })
                
                # Limit to MAX_REPOS repositories
                if len(trending_repos) >= MAX_REPOS:
                    break
                    
            except Exception as e:
                print(f"Error parsing repository: {e}")
    
    except Exception as e:
        print(f"Error fetching trending repositories: {e}")
    
    return trending_repos


def is_api_related(repo_name: str, description: str) -> bool:
    """
    Check if a repository is API-related based on its name and description.
    
    Args:
        repo_name: Repository name
        description: Repository description
    
    Returns:
        True if the repository is API-related, False otherwise
    """
    # Keywords that indicate API-related repositories
    api_keywords = [
        'api', 'rest', 'graphql', 'http', 'endpoint', 'service', 'microservice',
        'sdk', 'client', 'wrapper', 'interface', 'integration', 'connector',
        'webhook', 'openapi', 'swagger', 'json', 'xml', 'grpc', 'soap'
    ]
    
    repo_name_lower = repo_name.lower()
    description_lower = description.lower() if description else ""
    
    # Check if any keyword is in the repository name or description
    for keyword in api_keywords:
        if keyword in repo_name_lower or keyword in description_lower:
            return True
    
    return False


def parse_stars(stars_text: str) -> int:
    """
    Parse the stars count from the text.
    
    Args:
        stars_text: Text containing the stars count (e.g., "1.2k")
    
    Returns:
        Integer stars count
    """
    try:
        stars_text = stars_text.strip().replace(',', '')
        if 'k' in stars_text.lower():
            return int(float(stars_text.lower().replace('k', '')) * 1000)
        return int(stars_text)
    except ValueError:
        return 0


def update_readme_trending_section(trending_repos: List[Dict[str, Any]]) -> bool:
    """
    Update the trending repositories section in the README.md file.
    
    Args:
        trending_repos: List of trending repositories
    
    Returns:
        True if the README was updated, False otherwise
    """
    try:
        with open(README_FILE, 'r', encoding='utf-8') as file:
            readme_content = file.read()
        
        # Find the trending repositories section
        trending_section_pattern = r'(## :rocket: Trending GitHub Repositories.*?)(?=^## |\Z)'
        trending_section_match = re.search(trending_section_pattern, readme_content, re.DOTALL | re.MULTILINE)
        
        # Find the API categories section markers
        api_categories_start = "<!-- BEGIN API CATEGORIES SECTION - DO NOT REMOVE OR MODIFY THIS COMMENT -->"
        api_categories_end = "<!-- END API CATEGORIES SECTION - DO NOT REMOVE OR MODIFY THIS COMMENT -->"
        
        # Check if API categories section exists
        api_categories_exists = api_categories_start in readme_content and api_categories_end in readme_content
        
        if not trending_section_match:
            print("Trending repositories section not found in README")
            return False
        
        # Create the new trending repositories section
        today = datetime.datetime.now().strftime('%B %d, %Y')
        
        new_trending_section = f"## :rocket: Trending GitHub Repositories\n\n"
        new_trending_section += "This section is automatically updated daily with trending API-related repositories from GitHub. Discover what the community is building and using right now!\n\n"
        new_trending_section += "| Repository | Description | Stars | Language |\n"
        new_trending_section += "| --- | --- | --- | --- |\n"
        
        if trending_repos:
            for repo in trending_repos:
                # Truncate description if too long
                description = repo['description']
                if description and len(description) > 100:
                    description = description[:97] + '...'
                
                # Format stars count
                stars = repo['stars']
                if stars >= 1000:
                    stars_formatted = f"{stars/1000:.1f}k"
                else:
                    stars_formatted = str(stars)
                
                new_trending_section += f"| [{repo['full_name']}]({repo['url']}) | {description or 'No description'} | {stars_formatted} | {repo['language']} |\n"
        else:
            new_trending_section += "| _No API-related trending repositories found today_ | _Check back tomorrow for updates_ | | |\n"
        
        new_trending_section += f"\n_Last updated: {today}_\n"
        
        # Replace the old trending section with the new one
        updated_readme = re.sub(trending_section_pattern, new_trending_section, readme_content, flags=re.DOTALL | re.MULTILINE)
        
        # Write the updated README
        with open(README_FILE, 'w', encoding='utf-8') as file:
            file.write(updated_readme)
        
        print(f"README updated with {len(trending_repos)} trending repositories")
        return True
        
    except Exception as e:
        print(f"Error updating README: {e}")
        return False


def main():
    """Main function to update trending repositories."""
    print("Fetching trending API-related repositories from GitHub...")
    
    # Fetch trending repositories
    trending_repos = fetch_trending_repos()
    
    # If not enough API-related repositories found, try fetching more from different languages
    if len(trending_repos) < 5:
        for language in ['javascript', 'python', 'go', 'java', 'typescript']:
            if len(trending_repos) >= 5:
                break
            
            print(f"Fetching additional trending repositories for {language}...")
            language_repos = fetch_trending_repos(language=language)
            
            # Add repositories that aren't already in the list
            for repo in language_repos:
                if not any(r['full_name'] == repo['full_name'] for r in trending_repos):
                    trending_repos.append(repo)
                    if len(trending_repos) >= MAX_REPOS:
                        break
    
    # Update the README with trending repositories
    if trending_repos:
        update_readme_trending_section(trending_repos)
    else:
        print("No trending API-related repositories found")


if __name__ == "__main__":
    main()
