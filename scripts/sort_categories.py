#!/usr/bin/env python3
"""
Sort categories alphabetically

This script sorts all categories in the README.md file alphabetically.
"""

import os
import re
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

def extract_categories_from_list(content):
    """Extract categories from the navigation list."""
    categories_start = content.find("**Available Categories:**")
    if categories_start == -1:
        return []
    
    categories_start = categories_start + len("**Available Categories:**")
    categories_end = content.find("<a id=", categories_start)
    
    if categories_end == -1:
        return []
    
    categories_list = content[categories_start:categories_end]
    
    # Extract category names and IDs using regex
    category_pattern = r'\[([^\]]+)\]\(#([^)]+)\)'
    return re.findall(category_pattern, categories_list)

def extract_category_sections(content):
    """Extract all category sections from the README content."""
    category_sections = {}
    
    # Find all anchor IDs
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
        
        # Add divider if missing
        if '<div align="center"><hr' not in section_content:
            section_content += '\n\n<div align="center"><hr style="height:2px;border-width:0;color:rainbow;background-color:rainbow"></div>'
        
        # Extract category name from heading
        heading_match = re.search(r'###\s+([^\n]+)', section_content)
        if heading_match:
            heading = heading_match.group(1)
            emoji = heading.split()[0] if heading.split() else ""
            name = ' '.join(heading.split()[1:]) if len(heading.split()) > 1 else ""
            
            # Store the section with its name for sorting
            category_sections[anchor] = {
                'name': name,
                'emoji': emoji,
                'content': section_content
            }
    
    return category_sections

def generate_update_info():
    """Generate the API Categories last updated section."""
    import datetime
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

def sort_categories():
    """Sort all categories in the README.md file alphabetically."""
    try:
        # Load README content
        with open(README_FILE, 'r', encoding='utf-8') as file:
            readme_content = file.read()
        
        # Extract header, categories list, and footer
        header_content = extract_header(readme_content)
        footer_content = extract_footer(readme_content)
        
        # Extract categories from the navigation list
        categories = extract_categories_from_list(readme_content)
        
        # Extract existing category sections
        category_sections = extract_category_sections(readme_content)
        
        # Sort categories alphabetically by name
        sorted_categories = sorted(categories, key=lambda x: x[0].split()[1] if len(x[0].split()) > 1 else x[0])
        
        # Build the new README content with sorted categories
        new_content = []
        new_content.append(header_content)
        new_content.append("## 📋 API Categories - Find the Perfect API for Your Project\n\n")
        new_content.append("**Available Categories:**\n")
        
        # Create alphabetically sorted navigation list
        for emoji_name, anchor_id in sorted_categories:
            new_content.append(f"- [{emoji_name}](#{anchor_id})")
        
        new_content.append("\n\n")
        
        # Sort category sections alphabetically
        sorted_sections = []
        for anchor_id, section_info in category_sections.items():
            sorted_sections.append((section_info['name'], anchor_id, section_info['content']))
        
        sorted_sections.sort(key=lambda x: x[0].lower())
        
        # Add all category sections in alphabetical order
        for name, anchor_id, content in sorted_sections:
            new_content.append(content)
        
        # Add update info and footer
        new_content.append(generate_update_info())
        new_content.append("\n")
        new_content.append(footer_content)
        
        # Join all content
        new_readme_content = '\n'.join(new_content)
        
        # Write the new README content to a temporary file
        with open(TEMP_FILE, 'w', encoding='utf-8') as file:
            file.write(new_readme_content)
        
        # Replace the original README with the new one
        os.replace(TEMP_FILE, README_FILE)
        
        print(f"Sorted {len(sorted_sections)} categories alphabetically in README.md")
        
    except Exception as e:
        print(f"Error sorting categories in README.md: {e}")

def main():
    """Main function to sort categories."""
    print("Starting category sorting...")
    sort_categories()
    print("Category sorting completed.")

if __name__ == "__main__":
    main()
