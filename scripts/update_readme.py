#!/usr/bin/env python3
"""
Script to update the README.md file with the latest API data.
"""

import json
import os
import re
from datetime import datetime

def load_api_data():
    """Load API data from the discover_trending_apis.py script."""
    try:
        # Check if api_data.json exists
        api_data_file = "api_data.json"
        if os.path.exists(api_data_file):
            with open(api_data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"API data file {api_data_file} not found. Using fallback method.")
            return load_api_data_fallback()
    except Exception as e:
        print(f"Error loading API data: {e}")
        return load_api_data_fallback()

def load_api_data_fallback():
    """Fallback method to load API data directly from README.md."""
    readme_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract categories and APIs
    categories = []
    current_category = None
    
    for line in content.split('\n'):
        if line.startswith('### ') and not line.startswith('### Table of Contents'):
            # New category
            if current_category:
                categories.append(current_category)
            
            category_name = line[4:].strip()
            description = ''
            apis = []
            current_category = {
                'name': category_name,
                'description': description,
                'apis': apis
            }
        elif current_category and line.startswith('APIs related to'):
            # Category description
            current_category['description'] = line.strip()
        elif current_category and line.startswith('|') and not line.startswith('| API') and not line.startswith('| ---'):
            # API entry
            parts = line.split('|')
            if len(parts) >= 5:
                name = parts[1].strip()
                description = parts[2].strip()
                auth = parts[3].strip()
                https = parts[4].strip() == 'Yes'
                cors = parts[5].strip().lower() if len(parts) > 5 else 'unknown'
                
                # Extract URL if present
                url_match = re.search(r'\[(.*?)\]\((.*?)\)', name)
                if url_match:
                    name = url_match.group(1)
                    url = url_match.group(2)
                else:
                    url = ''
                
                api = {
                    'name': name,
                    'description': description,
                    'url': url,
                    'auth': auth,
                    'https': https,
                    'cors': cors,
                    'status': 'active',
                    'last_checked': datetime.now().isoformat()
                }
                
                current_category['apis'].append(api)
    
    # Add the last category
    if current_category:
        categories.append(current_category)
    
    # Sort categories alphabetically
    categories.sort(key=lambda x: x['name'])
    
    # Remove Testing category if it exists
    categories = [category for category in categories if category['name'] != 'Testing']
    
    # Create the data structure
    data = {
        'metadata': {
            'total_apis': sum(len(category['apis']) for category in categories),
            'last_updated': datetime.now().isoformat()
        },
        'categories': categories
    }
    
    return data

def update_readme(data):
    """Update the README.md file with the API data."""
    readme_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Make a backup of the README
    with open(f"{readme_path}.bak", 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Find the API categories section
    categories_section_pattern = r'## 📃 API Categories - Find the Perfect API for Your Project\n\n(.*?)(?=\n## )'
    categories_section_match = re.search(categories_section_pattern, content, re.DOTALL)
    
    if categories_section_match:
        # Create new categories section content
        new_section = "## 📃 API Categories - Find the Perfect API for Your Project\n\n"
        
        # Create the category links list
        for category in data['categories']:
            category_anchor = category['name'].lower().replace(' ', '-').replace('&', '').replace('/', '')
            category_desc = category['description'].split(':')[0] if ':' in category['description'] else category['description']
            new_section += f"- [{category['name']}](#{category_anchor}) - {category_desc}\n"
        
        new_section += "\n"
        
        # Add each category and its APIs
        for category in data['categories']:
            new_section += f"### {category['name']}\n"
            new_section += f"{category['description']}\n\n"
            new_section += "| API | Description | Auth | HTTPS | CORS |\n"
            new_section += "| --- | --- | --- | --- | --- |\n"
            
            for api in category['apis']:
                name = api['name']
                if api['url']:
                    name = f"[{name}]({api['url']})"
                
                https = "Yes" if api['https'] else "No"
                
                new_section += f"| {name} | {api['description']} | {api['auth']} | {https} | {api['cors']} |\n"
            
            new_section += "\n"
        
        # Replace the old section with the new one
        updated_content = re.sub(categories_section_pattern, new_section, content, flags=re.DOTALL)
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"Updated README.md with {data['metadata']['total_apis']} APIs")
    else:
        print("Could not find API categories section in README.md")

def main():
    """Main function to update the README."""
    print("Loading API data...")
    data = load_api_data()
    
    # Save API data to JSON file for future use
    try:
        with open("api_data.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print("Saved API data to api_data.json")
    except Exception as e:
        print(f"Error saving API data to JSON: {e}")
    
    print("Updating README.md...")
    update_readme(data)
    
    print("Done!")

if __name__ == "__main__":
    main()
