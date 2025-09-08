#!/usr/bin/env python3
"""
Rebuild README with all categories

This script rebuilds the README.md file by extracting all categories from the original file
and creating a clean, properly formatted version with all categories included.
"""

import os
import re
import datetime
from collections import OrderedDict

# Constants
README_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')
TEMP_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md.new')

def extract_header(content):
    """Extract the header section from the README content."""
    header_end = content.find("## 📋 API Categories")
    return content[:header_end]

def extract_categories_list(content):
    """Extract the categories list from the README content."""
    categories_start = content.find("**Available Categories:**")
    if categories_start == -1:
        return ""
    
    categories_start = categories_start + len("**Available Categories:**")
    categories_end = content.find("<a id=", categories_start)
    
    if categories_end == -1:
        return ""
    
    return content[categories_start:categories_end]

def extract_footer(content):
    """Extract the footer section from the README content."""
    trending_repos_start = content.find("## 🚀 Trending GitHub API Repositories")
    
    if trending_repos_start == -1:
        return ""
    
    return content[trending_repos_start:]

def extract_category_sections(content):
    """Extract all category sections from the README content."""
    # Find all category sections using regex
    category_pattern = r'<a id="([^"]+)"></a>\s*###\s+([^\n]+)\s*([^\n]*)\s*\|[^\|]*\|[^\|]*\|[^\|]*\|[^\|]*\|[^\|]*\|'
    category_sections = {}
    
    # First, find all anchor IDs
    anchor_pattern = r'<a id="([^"]+)"></a>'
    anchors = re.findall(anchor_pattern, content)
    
    # For each anchor, extract the complete section until the next anchor or divider
    for i, anchor in enumerate(anchors):
        anchor_start = content.find(f'<a id="{anchor}"></a>')
        
        # Find the end of this section (start of next section or end of content)
        if i < len(anchors) - 1:
            next_anchor = anchors[i + 1]
            next_anchor_start = content.find(f'<a id="{next_anchor}"></a>')
            section_end = content.rfind('<div align="center"><hr', anchor_start, next_anchor_start)
            
            if section_end == -1:
                section_end = next_anchor_start
        else:
            section_end = content.find("_API Categories last updated:", anchor_start)
            if section_end == -1:
                section_end = content.find("## 🚀 Trending GitHub API Repositories", anchor_start)
        
        if section_end == -1:
            continue
        
        # Extract the section content
        section_content = content[anchor_start:section_end].strip()
        
        # Fix any broken sections
        if anchor == "authentication":
            section_content = fix_authentication_section(section_content)
        elif anchor == "weather":
            section_content = fix_weather_section(section_content)
        
        category_sections[anchor] = section_content + "\n\n<div align=\"center\"><hr style=\"height:2px;border-width:0;color:rainbow;background-color:rainbow\"></div>\n"
    
    return category_sections

def fix_authentication_section(content):
    """Fix the authentication section if needed."""
    return re.sub(r'\| <a href="https://warrant\.dev/" target="_blank">Warrant</a> \| APIs for authorization and.*?_', 
                 '| <a href="https://warrant.dev/" target="_blank">Warrant</a> | APIs for authorization and access control | `apiKey` | Yes | yes |', 
                 content)

def fix_weather_section(content):
    """Fix the weather section if needed."""
    if "Tomorrow.io Weather API" not in content:
        content = re.sub(r'Weather Service \| none \| Yes \| yes \|', 
                        '| <a href="https://www.tomorrow.io/weather-api/" target="_blank">Tomorrow.io Weather API</a> | Weather API with forecasts, historical data, and severe weather alerts | `apiKey` | Yes | yes |', 
                        content)
    return content

def generate_update_info():
    """Generate the API Categories last updated section."""
    today = datetime.datetime.now().strftime('%B %d, %Y')
    
    # Calculate the next update dates
    now = datetime.datetime.now()
    
    # Next Sunday for Weekly API Status Checks
    days_until_sunday = (6 - now.weekday()) % 7
    if days_until_sunday == 0:
        days_until_sunday = 7  # If today is Sunday, get next Sunday
    next_sunday = now + datetime.timedelta(days=days_until_sunday)
    next_sunday_str = next_sunday.strftime('%B %d, %Y')
    
    # Next Monday for Enhanced API Discovery
    days_until_monday = (0 - now.weekday()) % 7
    if days_until_monday == 0:
        days_until_monday = 7  # If today is Monday, get next Monday
    next_monday = now + datetime.timedelta(days=days_until_monday)
    next_monday_str = next_monday.strftime('%B %d, %Y')
    
    # Next 1st of month for Monthly API Discovery
    if now.day == 1:
        # If today is the 1st, get 1st of next month
        next_month = now.replace(day=28) + datetime.timedelta(days=4)  # Move to next month
        next_first = next_month.replace(day=1)
    else:
        # Get 1st of next month
        if now.month == 12:
            next_first = now.replace(year=now.year + 1, month=1, day=1)
        else:
            next_first = now.replace(month=now.month + 1, day=1)
    next_first_str = next_first.strftime('%B %d, %Y')
    
    return f"""
_API Categories last updated: {today}_

**API Update Schedule:**
- Weekly API Status Checks (Next: {next_sunday_str})
- Enhanced API Discovery (Next: {next_monday_str})
- Monthly API Discovery (Next: {next_first_str})
"""

def rebuild_readme():
    """Rebuild the README.md file with all categories."""
    try:
        # Load README content
        with open(README_FILE, 'r', encoding='utf-8') as file:
            readme_content = file.read()
        
        # Extract header, categories list, and footer
        header_content = extract_header(readme_content)
        categories_list = extract_categories_list(readme_content)
        footer_content = extract_footer(readme_content)
        
        # Extract all category sections
        category_sections = extract_category_sections(readme_content)
        
        # Generate update info
        update_info = generate_update_info()
        
        # Build the new README content
        new_readme_content = (
            header_content + 
            "## 📋 API Categories - Find the Perfect API for Your Project\n\n" +
            "**Available Categories:**" + 
            categories_list + 
            "\n" + 
            "".join(category_sections.values()) + 
            update_info + 
            "\n" + 
            footer_content
        )
        
        # Write the new README content to a temporary file
        with open(TEMP_FILE, 'w', encoding='utf-8') as file:
            file.write(new_readme_content)
        
        # Replace the original README with the new one
        os.replace(TEMP_FILE, README_FILE)
        
        print(f"Rebuilt README.md with {len(category_sections)} categories")
        
    except Exception as e:
        print(f"Error rebuilding README.md: {e}")

def main():
    """Main function to rebuild README."""
    print("Starting README rebuild...")
    rebuild_readme()
    print("README rebuild completed.")

if __name__ == "__main__":
    main()
