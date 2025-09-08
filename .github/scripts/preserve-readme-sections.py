#!/usr/bin/env python3
"""
This script preserves important sections in the README.md file during automated updates.
It ensures that navigation links and SEO keywords are not removed or modified.
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

def preserve_readme_sections():
    """Preserve important sections in README.md."""
    readme_path = 'README.md'
    
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found.")
        return
    
    # Read the current README content
    readme_content = read_file(readme_path)
    
    # Extract the navigation bar section
    nav_bar_pattern = r'(\[Browse APIs by Category\].*?Buy Me a Coffee\]\(https://buymeacoffee\.com/gunjanjaswal\))'
    nav_bar_match = re.search(nav_bar_pattern, readme_content, re.DOTALL)
    
    if not nav_bar_match:
        print("Warning: Navigation bar not found in README.")
        return
    
    nav_bar = nav_bar_match.group(1)
    
    # Extract the SEO keywords section
    seo_keywords_pattern = r'(<!-- SEO KEYWORDS.*?</div>)'
    seo_keywords_match = re.search(seo_keywords_pattern, readme_content, re.DOTALL)
    
    if not seo_keywords_match:
        print("Warning: SEO keywords section not found in README.")
        return
    
    seo_keywords = seo_keywords_match.group(1)
    
    # Ensure correct anchor links in navigation bar
    nav_bar = nav_bar.replace(
        "#-api-categories---find-the-perfect-api-for-your-project", 
        "#card_index-api-categories---find-the-perfect-api-for-your-project"
    )
    nav_bar = nav_bar.replace(
        "#-trending-github-repositories", 
        "#rocket-trending-github-repositories"
    )
    nav_bar = nav_bar.replace(
        "#-how-to-contribute-to-this-api-collection", 
        "#handshake-how-to-contribute-to-this-api-collection"
    )
    nav_bar = nav_bar.replace(
        "#-how-our-automated-api-tracking-works", 
        "#gear-how-our-automated-api-tracking-works"
    )
    nav_bar = nav_bar.replace(
        "#-license", 
        "#page_with_curl-license"
    )
    
    # Update the README content with preserved sections
    updated_content = readme_content
    
    # Update navigation bar
    updated_content = re.sub(
        r'\[Browse APIs by Category\].*?Buy Me a Coffee\]\(https://buymeacoffee\.com/gunjanjaswal\)',
        nav_bar,
        updated_content,
        flags=re.DOTALL
    )
    
    # Ensure SEO keywords section exists at the end of the file
    if "<!-- SEO KEYWORDS" not in updated_content:
        # Add SEO keywords section before the end of the file
        if updated_content.endswith("\n"):
            updated_content += seo_keywords
        else:
            updated_content += "\n" + seo_keywords
    else:
        # Update existing SEO keywords section
        updated_content = re.sub(
            r'<!-- SEO KEYWORDS.*?</div>',
            seo_keywords,
            updated_content,
            flags=re.DOTALL
        )
    
    # Write the updated content back to the README
    write_file(readme_path, updated_content)
    print("README sections preserved successfully.")

if __name__ == "__main__":
    preserve_readme_sections()
