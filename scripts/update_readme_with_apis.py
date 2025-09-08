#!/usr/bin/env python3
"""
Update README with APIs

This script reads the APIs data file and updates the README.md file with APIs by category.
"""

import os
import json
import re
import datetime
from typing import Dict, List, Any

# Constants
README_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'apis.json')

def load_api_data() -> Dict[str, Any]:
    """Load API data from the JSON file."""
    try:
        # Ensure the data directory exists
        data_dir = os.path.dirname(DATA_FILE)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"Created data directory: {data_dir}")
            
        # Try to load existing data
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            print(f"Data file {DATA_FILE} not found")
            return {"categories": [], "metadata": {"total_apis": 0}}
    except Exception as e:
        print(f"Error loading API data: {e}")
        return {"categories": [], "metadata": {"total_apis": 0}}

def update_readme_with_apis() -> None:
    """Update the README.md file with APIs from the data file."""
    try:
        # Load API data
        data = load_api_data()
        
        # Load README content
        with open(README_FILE, 'r', encoding='utf-8') as file:
            readme_content = file.read()
        
        # Find the API Categories section
        api_categories_heading = "## 📋 API Categories"
        api_categories_index = readme_content.find(api_categories_heading)
        
        if api_categories_index == -1:
            print("Could not find API Categories section in README.md")
            return
        
        # Find the end of the API Categories list
        categories_list_start = readme_content.find("- [", api_categories_index)
        categories_list_end = readme_content.find("\n\n", categories_list_start)
        
        if categories_list_start == -1 or categories_list_end == -1:
            print("Could not find API Categories list in README.md")
            return
        
        # Find the start of the next major section after API Categories
        next_section_index = readme_content.find("## 🚀 Trending GitHub API Repositories", categories_list_end)
        
        if next_section_index == -1:
            print("Could not find next section after API Categories in README.md")
            return
        
        # Extract the content before and after the API categories section
        content_before = readme_content[:categories_list_end + 2]  # Include the newlines after the categories list
        content_after = readme_content[next_section_index:]  # Everything from the next section onwards
        
        # Create the updated API categories content
        updated_categories_content = ""
        
        # Process each category
        for category in data['categories']:
            category_name = category['name']
            
            if not category['apis']:
                # Add empty category placeholder
                updated_categories_content += f"### {category_name}\n{category.get('description', f'APIs for {category_name.lower()} related services.')}\n\n"
                continue
            
            # Create the API table for this category
            api_table = "| API | Description | Auth | HTTPS | CORS |\n"
            api_table += "| --- | --- | --- | --- | --- |\n"
            
            # Add each API to the table
            for api in category['apis']:
                name = api.get('name', '')
                url = api.get('url', '')
                description = api.get('description', '')
                auth = api.get('auth', 'unknown')
                https = 'Yes' if api.get('https', False) else 'No'
                cors = api.get('cors', 'unknown')
                
                # Format the API row with HTML links that have target="_blank"
                if url:
                    link = f"<a href=\"{url}\" target=\"_blank\">{name}</a>"
                else:
                    link = name
                api_table += f"| {link} | {description} | {auth} | {https} | {cors} |\n"
            
            # Add the category section to the updated content
            updated_categories_content += f"### {category_name}\n{category.get('description', f'APIs for {category_name.lower()} related services.')}\n\n{api_table}\n\n"
            print(f"Added category section for {category_name} with {len(category['apis'])} APIs")
        
        # Add a 'Last updated' date and update schedules after the API categories section
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
        
        update_info = f"""_API Categories last updated: {today}_

**API Update Schedule:**
- Weekly API Status Checks (Next: {next_sunday_str})
- Enhanced API Discovery (Next: {next_monday_str})
- Monthly API Discovery (Next: {next_first_str})

"""        
        updated_categories_content += update_info
        
        # Combine all parts to create the updated README content
        updated_readme_content = content_before + updated_categories_content + content_after
        
        # Update the last updated timestamp
        today = datetime.datetime.now().strftime('%B %d, %Y')
        updated_readme_content = re.sub(r'<p align="center">Last updated: .*?</p>', f'<p align="center">Last updated: {today}</p>', updated_readme_content)
        
        # Write the updated README
        with open(README_FILE, 'w', encoding='utf-8') as file:
            file.write(updated_readme_content)
        
        print(f"Updated README.md with APIs from {len(data['categories'])} categories")
        
    except Exception as e:
        print(f"Error updating README.md: {e}")

def main():
    """Main function to update README with APIs."""
    print("Starting README update with APIs...")
    update_readme_with_apis()
    print("README update completed.")

if __name__ == "__main__":
    main()
