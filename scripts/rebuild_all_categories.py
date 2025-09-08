#!/usr/bin/env python3
"""
Rebuild README with all categories

This script rebuilds the README.md file by ensuring all categories from the navigation list
are included in the final document.
"""

import os
import re
import datetime

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
    
    # Find all sections with anchor IDs
    section_pattern = r'<a id="([^"]+)"></a>\s*###\s+([^\n]+)'
    sections = re.findall(section_pattern, content)
    
    for anchor_id, title in sections:
        # Find the start of this section
        section_start = content.find(f'<a id="{anchor_id}"></a>')
        
        # Find the end of this section (start of next section or divider)
        next_section = content.find('<a id="', section_start + 1)
        if next_section == -1:
            next_section = len(content)
        
        divider = content.find('<div align="center"><hr', section_start)
        if divider != -1 and divider < next_section:
            section_end = divider + len('<div align="center"><hr style="height:2px;border-width:0;color:rainbow;background-color:rainbow"></div>')
        else:
            section_end = next_section
        
        # Extract the section content
        section_content = content[section_start:section_end].strip()
        
        # Fix any broken sections
        if anchor_id == "authentication":
            section_content = fix_authentication_section(section_content)
        elif anchor_id == "weather":
            section_content = fix_weather_section(section_content)
        
        # Add divider if missing
        if '<div align="center"><hr' not in section_content:
            section_content += '\n\n<div align="center"><hr style="height:2px;border-width:0;color:rainbow;background-color:rainbow"></div>'
        
        category_sections[anchor_id] = section_content
    
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

def create_placeholder_section(category_name, anchor_id, emoji):
    """Create a placeholder section for missing categories."""
    return f"""<a id="{anchor_id}"></a>
### {emoji} {category_name}
APIs for {category_name.lower()} related services

🌱 This category is freshly planted. APIs will sprout soon!

<div align="center"><hr style="height:2px;border-width:0;color:rainbow;background-color:rainbow"></div>"""

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
        
        # Extract categories from the navigation list
        categories = extract_categories_from_list(readme_content)
        
        # Extract existing category sections
        existing_sections = extract_category_sections(readme_content)
        
        # Build the new README content with all categories
        new_content = []
        new_content.append(header_content)
        new_content.append("## 📋 API Categories - Find the Perfect API for Your Project\n\n")
        new_content.append("**Available Categories:**")
        new_content.append(categories_list)
        new_content.append("\n")
        
        # Add all category sections in the order they appear in the navigation list
        for emoji_name, anchor_id in categories:
            emoji = emoji_name.split()[0]
            name = ' '.join(emoji_name.split()[1:])
            
            if anchor_id in existing_sections:
                new_content.append(existing_sections[anchor_id])
            else:
                new_content.append(create_placeholder_section(name, anchor_id, emoji))
        
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
        
        print(f"Rebuilt README.md with all {len(categories)} categories")
        
    except Exception as e:
        print(f"Error rebuilding README.md: {e}")

def main():
    """Main function to rebuild README."""
    print("Starting README rebuild with all categories...")
    rebuild_readme()
    print("README rebuild completed.")

if __name__ == "__main__":
    main()
