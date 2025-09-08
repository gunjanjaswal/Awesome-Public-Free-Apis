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
    
    # Define the correct navigation bar with proper anchor links
    correct_nav_bar = "[Browse APIs by Category](#card_index-api-categories---find-the-perfect-api-for-your-project) • [Trending API Repositories](#rocket-trending-github-api-repositories) • [Trending GitHub Repositories](#rocket-trending-github-repositories) • [How to Contribute](#handshake-how-to-contribute-to-this-api-collection) • [Automation Details](#gear-how-our-automated-api-tracking-works) • [License](#page_with_curl-license) • [☕ Buy Me a Coffee](https://buymeacoffee.com/gunjanjaswal)"
    
    # Extract the SEO keywords section
    seo_keywords_pattern = r'(<!-- SEO KEYWORDS.*?</div>)'
    seo_keywords_match = re.search(seo_keywords_pattern, readme_content, re.DOTALL)
    
    if not seo_keywords_match:
        print("Warning: SEO keywords section not found in README.")
        # Create default SEO keywords section if not found
        seo_keywords = """<!-- SEO KEYWORDS - DO NOT REMOVE OR MODIFY THIS SECTION -->
<div align="center">
<details>
<summary>Keywords for Better Discovery</summary>

free apis, public apis, rest apis, api collection, developer tools, web development, api documentation, programming resources, json apis, http apis, api integration, backend development, frontend development, software development, api testing, api reference, open source apis, no authentication apis, free data sources, api directory, api catalog, api list, developer resources, coding resources, api hub, api repository, api database, api endpoints, api services, api toolkit, web services, data apis, third-party apis, external apis, api documentation, api examples, api tutorials, api guides, api implementation, api usage, api consumption, api providers, api registry, api index, api search, api discovery, api marketplace, api ecosystem, api community, api standards, api protocols, api specifications, api best practices, api security, api authentication, api rate limits, api versioning, api monitoring, api analytics, api performance, api reliability, api availability, api scalability

</details>
</div>"""
    else:
        seo_keywords = seo_keywords_match.group(1)
    
    # Update the README content with preserved sections
    # First, replace any navigation bar with the correct one
    nav_pattern = r'\[Browse APIs by Category\].*?\[License\]\([^)]+\)(?:\s•\s\[☕\sBuy\sMe\sa\sCoffee\]\(https://buymeacoffee\.com/gunjanjaswal\))?'
    updated_content = re.sub(nav_pattern, correct_nav_bar, readme_content, flags=re.DOTALL)
    
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
    
    # Remove any merge conflict markers
    updated_content = re.sub(r'<<<<<<< .*?\n', '', updated_content)
    updated_content = re.sub(r'=======\n', '', updated_content)
    updated_content = re.sub(r'>>>>>>> .*?\n', '', updated_content)
    
    # Fix formatting issues with section headings
    updated_content = re.sub(r'_Last updated: .*?_## ', '_Last updated: \g<0>_\n\n## ', updated_content)
    
    # Write the updated content back to the README
    write_file(readme_path, updated_content)
    print("README sections preserved successfully.")

if __name__ == "__main__":
    preserve_readme_sections()
