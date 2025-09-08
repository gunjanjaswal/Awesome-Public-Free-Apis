#!/usr/bin/env python3
"""
This script fixes the navigation links in the README.md file.
It ensures that the navigation links use the correct anchor format with emoji identifiers.
"""

import re
import os

def read_file(file_path):
    """Read file content."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    """Write content to file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def fix_navigation_links():
    """Fix navigation links in README.md."""
    readme_path = 'README.md'
    
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found.")
        return
    
    # Read the current README content
    readme_content = read_file(readme_path)
    
    # Define the correct navigation bar with proper anchor links and Buy Me a Coffee logo
    correct_nav_bar = "[Browse APIs by Category](#card_index-api-categories---find-the-perfect-api-for-your-project) • [Trending GitHub Repositories](#rocket-trending-github-repositories) • [How to Contribute](#handshake-how-to-contribute-to-this-api-collection) • [Automation Details](#gear-how-our-automated-api-tracking-works) • [License](#page_with_curl-license) • [<img src=\"https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png\" alt=\"Buy Me A Coffee\" height=\"20\" width=\"70\">](https://buymeacoffee.com/gunjanjaswal)"
    
    # Replace any navigation bar with the correct one
    nav_pattern = r'\[Browse APIs by Category\].*?\[License\]\([^)]+\)(?:\s•\s\[[^]]+\]\(https://buymeacoffee\.com/gunjanjaswal\))?'
    updated_content = re.sub(nav_pattern, correct_nav_bar, readme_content, flags=re.DOTALL)
    
    # Fix formatting issues with section headings
    updated_content = re.sub(r'_Last updated: .*?_## ', r'_Last updated: \g<0>_\n\n## ', updated_content)
    
    # Fix anchor links in the README content
    updated_content = updated_content.replace('#-api-categories---find-the-perfect-api-for-your-project', '#card_index-api-categories---find-the-perfect-api-for-your-project')
    updated_content = updated_content.replace('#-trending-github-repositories', '#rocket-trending-github-repositories')
    updated_content = updated_content.replace('#-how-to-contribute-to-this-api-collection', '#handshake-how-to-contribute-to-this-api-collection')
    updated_content = updated_content.replace('#-how-our-automated-api-tracking-works', '#gear-how-our-automated-api-tracking-works')
    updated_content = updated_content.replace('#-license', '#page_with_curl-license')
    
    # Remove any merge conflict markers
    updated_content = re.sub(r'<<<<<<< .*?\n', '', updated_content)
    updated_content = re.sub(r'=======\n', '', updated_content)
    updated_content = re.sub(r'>>>>>>> .*?\n', '', updated_content)
    
    # Write the updated content back to the README
    write_file(readme_path, updated_content)
    print("Navigation links fixed successfully.")

if __name__ == "__main__":
    fix_navigation_links()
