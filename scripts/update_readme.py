#!/usr/bin/env python3
"""
Script to update the README.md file with the latest API data from apis.json
"""

import json
import os
import re
from datetime import datetime

def load_api_data():
    """Load API data from the JSON file."""
    try:
        with open('data/apis.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading API data: {e}")
        return None

def update_readme():
    """Update the README.md file with the latest API data."""
    # Load API data
    data = load_api_data()
    if not data:
        print("Failed to load API data")
        return False
    
    # Load README template
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            readme_content = f.read()
    except Exception as e:
        print(f"Error loading README: {e}")
        return False
    
    # Update API categories in README
    for category in data['categories']:
        category_name = category['name']
        category_description = category['description']
        apis = category['apis']
        
        # Sort APIs by popularity (descending)
        apis = sorted(apis, key=lambda x: x.get('popularity', 0), reverse=True)
        
        # Create category section
        category_section = f"\n### {category_name}\n{category_description}\n\n"
        category_section += "| API | Description | Auth | HTTPS | CORS |\n"
        category_section += "| --- | --- | --- | --- | --- |\n"
        
        # Add APIs to category section
        for api in apis:
            name = api.get('name', '')
            description = api.get('description', '')
            url = api.get('url', '')
            auth = api.get('auth', 'unknown')
            https = "Yes" if api.get('https', False) else "No"
            cors = api.get('cors', 'unknown')
            
            # Format the API row
            category_section += f"| [{name}]({url}) | {description} | {auth} | {https} | {cors} |\n"
        
        # Replace category section in README
        pattern = rf"### {re.escape(category_name)}.*?(?=\n## |\n### |\Z)"
        replacement = category_section.rstrip()
        readme_content = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)
    
    # Update last updated date
    today = datetime.now().strftime("%B %d, %Y")
    readme_content = re.sub(r"Last updated: .*?<", f"Last updated: {today}<", readme_content)
    
    # Write updated README
    try:
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"README updated successfully with {len(data['categories'])} categories")
        return True
    except Exception as e:
        print(f"Error writing README: {e}")
        return False

if __name__ == "__main__":
    update_readme()
