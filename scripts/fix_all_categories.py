#!/usr/bin/env python3
"""
Fix README file with all categories

This script fixes the README.md file by preserving all categories and fixing formatting issues.
"""

import os
import re
import datetime

# Constants
README_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')

def fix_readme():
    """Fix the README.md file completely."""
    try:
        # Load README content
        with open(README_FILE, 'r', encoding='utf-8') as file:
            readme_content = file.read()
        
        # Extract the header section (everything before API Categories)
        header_end = readme_content.find("## 📋 API Categories")
        header_content = readme_content[:header_end]
        
        # Extract the categories list
        categories_start = readme_content.find("**Available Categories:**", header_end) + len("**Available Categories:**")
        categories_end = readme_content.find("<a id=", categories_start)
        categories_list = readme_content[categories_start:categories_end]
        
        # Extract all category sections
        categories_section_start = categories_end
        trending_repos_start = readme_content.find("## 🚀 Trending GitHub API Repositories")
        
        if trending_repos_start == -1:
            print("Could not find Trending GitHub API Repositories section")
            return
        
        # Extract all category content
        categories_content = readme_content[categories_section_start:trending_repos_start]
        
        # Fix the authentication section
        auth_pattern = r'<a id="authentication"></a>.*?<div align="center"><hr style="height:2px;border-width:0;color:rainbow;background-color:rainbow"></div>'
        auth_section = re.search(auth_pattern, categories_content, re.DOTALL)
        if auth_section:
            auth_content = auth_section.group(0)
            fixed_auth_content = re.sub(r'\| <a href="https://warrant\.dev/" target="_blank">Warrant</a> \| APIs for authorization and.*?_', 
                                       '| <a href="https://warrant.dev/" target="_blank">Warrant</a> | APIs for authorization and access control | `apiKey` | Yes | yes |', 
                                       auth_content)
            categories_content = categories_content.replace(auth_content, fixed_auth_content)
        
        # Fix the weather section
        weather_pattern = r'_API Categories last updated: .*?_\s*\n\s*\*\*API Update Schedule:\*\*.*?\n.*?\n.*?\n.*?\n\s*Weather Service \| none \| Yes \| yes \|'
        weather_replacement = '| <a href="https://www.tomorrow.io/weather-api/" target="_blank">Tomorrow.io Weather API</a> | Weather API with forecasts, historical data, and severe weather alerts | `apiKey` | Yes | yes |'
        categories_content = re.sub(weather_pattern, weather_replacement, categories_content)
        
        # Remove duplicate API Update Schedule sections
        categories_content = re.sub(r'(\n_API Categories last updated: .*?_\s*\n\s*\*\*API Update Schedule:\*\*.*?\n.*?\n.*?\n.*?\n).*?- Enhanced API Discovery.*?\n.*?Monthly API Discovery.*?\n', 
                                   r'\1', 
                                   categories_content)
        
        # Extract the footer (everything after API sections)
        footer_content = readme_content[trending_repos_start:]
        
        # Add the API Categories last updated section
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
        
        update_info = f"""
_API Categories last updated: {today}_

**API Update Schedule:**
- Weekly API Status Checks (Next: {next_sunday_str})
- Enhanced API Discovery (Next: {next_monday_str})
- Monthly API Discovery (Next: {next_first_str})
"""
        
        # Combine all parts to create the fixed README content
        fixed_readme_content = (
            header_content + 
            "## 📋 API Categories - Find the Perfect API for Your Project\n\n" +
            "**Available Categories:**" + 
            categories_list + 
            "\n" + 
            categories_content + 
            update_info + 
            "\n" + 
            footer_content
        )
        
        # Write the fixed README
        with open(README_FILE, 'w', encoding='utf-8') as file:
            file.write(fixed_readme_content)
        
        print("Fixed README.md file completely with all categories preserved")
        
    except Exception as e:
        print(f"Error fixing README.md: {e}")

def main():
    """Main function to fix README."""
    print("Starting complete README fix...")
    fix_readme()
    print("Complete README fix completed.")

if __name__ == "__main__":
    main()
