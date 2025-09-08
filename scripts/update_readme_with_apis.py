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
        
        # Update each category section in the README
        for category in data['categories']:
            category_name = category['name']
            
            if not category['apis']:
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
                
                # Format the API row
                api_table += f"| [{name}]({url}) | {description} | {auth} | {https} | {cors} |\n"
            
            # Find the category section in the README
            category_pattern = f"### {category_name}\\n.*?\\n\\n"
            category_match = re.search(category_pattern, readme_content, re.DOTALL)
            
            if category_match:
                # Replace the existing category section
                new_category_section = f"### {category_name}\n{category.get('description', f'APIs for {category_name.lower()} related services.')}\n\n{api_table}\n"
                readme_content = readme_content.replace(category_match.group(0), new_category_section)
                print(f"Updated category section for {category_name} with {len(category['apis'])} APIs")
            else:
                # Find where to insert the new category section
                # Look for the next category section after the API Categories heading
                api_categories_heading = "## 📋 API Categories"
                api_categories_index = readme_content.find(api_categories_heading)
                
                if api_categories_index != -1:
                    # Find the position after the API Categories list
                    categories_list_end = readme_content.find("\n\n", api_categories_index + len(api_categories_heading))
                    
                    if categories_list_end != -1:
                        # Insert the new category section after the categories list
                        new_category_section = f"\n### {category_name}\n{category.get('description', f'APIs for {category_name.lower()} related services.')}\n\n{api_table}\n"
                        readme_content = readme_content[:categories_list_end + 2] + new_category_section + readme_content[categories_list_end + 2:]
                        print(f"Added new category section for {category_name} with {len(category['apis'])} APIs")
        
        # Update the last updated timestamp
        today = datetime.datetime.now().strftime('%B %d, %Y')
        readme_content = re.sub(r'<p align="center">Last updated: .*?</p>', f'<p align="center">Last updated: {today}</p>', readme_content)
        
        # Write the updated README
        with open(README_FILE, 'w', encoding='utf-8') as file:
            file.write(readme_content)
        
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
