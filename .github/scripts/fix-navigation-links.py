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
    
    # Define the correct navigation bar with proper anchor links
    correct_nav_bar = "[Browse APIs by Category](#card_index-api-categories---find-the-perfect-api-for-your-project) • [Trending GitHub Repositories](#rocket-trending-github-repositories) • [How to Contribute](#handshake-how-to-contribute-to-this-api-collection) • [Automation Details](#gear-how-our-automated-api-tracking-works) • [License](#page_with_curl-license) • [☕ Buy Me a Coffee](https://buymeacoffee.com/gunjanjaswal)"
    
    # Find the navigation bar in the README
    nav_pattern = r'\[Browse APIs by Category\].*?\[License\]'
    nav_match = re.search(nav_pattern, readme_content, re.DOTALL)
    
    if not nav_match:
        print("Warning: Navigation bar not found in README.")
        return
    
    # Replace the navigation bar with the correct one
    updated_content = re.sub(
        r'\[Browse APIs by Category\].*?\[License\]\([^)]+\)(?:\s•\s\[☕\sBuy\sMe\sa\sCoffee\]\(https://buymeacoffee\.com/gunjanjaswal\))?',
        correct_nav_bar,
        readme_content,
        flags=re.DOTALL
    )
    
    # Fix formatting issues with section headings
    updated_content = re.sub(r'_Last updated: .*?_## ', r'_Last updated: \g<0>_\n\n## ', updated_content)
    
    # Write the updated content back to the README
    write_file(readme_path, updated_content)
    print("Navigation links fixed successfully.")

if __name__ == "__main__":
    fix_navigation_links()
