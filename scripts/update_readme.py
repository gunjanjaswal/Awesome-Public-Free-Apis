#!/usr/bin/env python3
"""
README Updater Script

This script automatically updates the README.md file with the latest API data from apis.json.
It ensures the README always reflects the current state of the API collection without manual intervention.
"""

import json
import os
import re
import datetime
from typing import Dict, List, Any

# Constants
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(ROOT_DIR, 'data', 'apis.json')
README_FILE = os.path.join(ROOT_DIR, 'README.md')


def load_api_data() -> Dict[str, Any]:
    """Load API data from the JSON file."""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading API data: {e}")
        return {"categories": [], "metadata": {"total_apis": 0}}


def load_readme() -> str:
    """Load the README.md file content."""
    try:
        with open(README_FILE, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError as e:
        print(f"Error loading README: {e}")
        return ""


def save_readme(content: str) -> None:
    """Save the updated README.md file."""
    try:
        with open(README_FILE, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"README updated successfully at {README_FILE}")
    except Exception as e:
        print(f"Error saving README: {e}")


def generate_api_table(apis: List[Dict[str, Any]]) -> str:
    """Generate a markdown table for a list of APIs."""
    if not apis:
        return "_No APIs in this category yet. They will be automatically added soon!_\n"
    
    # Create a proper markdown table
    table = "| API | Description | Auth | HTTPS | CORS |\n"
    table += "| --- | --- | --- | --- | --- |\n"
    
    for api in sorted(apis, key=lambda x: x.get('popularity', 0), reverse=True):
        # Get API properties with proper escaping and defaults
        name = api.get('name', '').replace('|', '\\|')
        url = api.get('url', '')
        description = api.get('description', '').replace('|', '\\|')  # Escape pipe characters
        
        # Ensure auth, https, and cors have proper values
        auth = api.get('auth', '')
        if not auth or auth == 'unknown':
            auth = ''
            
        https = "Yes" if api.get('https', False) else "No"
        
        cors = api.get('cors', '')
        if cors == 'unknown':
            cors = ''
        
        # Truncate description if too long
        if len(description) > 100:
            description = description[:97] + '...'
        
        # Ensure there are no trailing spaces that could break markdown formatting
        name = name.strip()
        description = description.strip()
        auth = auth.strip()
        https = https.strip()
        cors = cors.strip()
        
        # Create the table row with proper markdown formatting
        table += f"| [{name}]({url}) | {description} | {auth} | {https} | {cors} |\n"
    
    return table


def update_category_sections(readme_content: str, api_data: Dict[str, Any]) -> str:
    """Update the API category sections in the README."""
    updated_content = readme_content
    
    # For each category in the API data
    for category in api_data['categories']:
        try:
            category_name = category['name']
            category_apis = category['apis']
            
            # Create the API table for this category
            api_table = generate_api_table(category_apis)
            
            # Find the category section in the README
            # First try with the standard pattern
            category_pattern = f"### {re.escape(category_name)}\\n(.*?)\\n\\n### "
            category_match = re.search(category_pattern, updated_content, re.DOTALL)
            
            if not category_match:
                # Try alternative pattern for the last category in the file
                category_pattern = f"### {re.escape(category_name)}\\n(.*?)\\n\\n## "
                category_match = re.search(category_pattern, updated_content, re.DOTALL)
            
            if category_match:
                # Replace the existing content with the new API table
                section_start = category_match.start(1)
                section_end = category_match.end(1)
                
                # Keep the category description
                description_parts = category_match.group(1).split('\n')
                description_line = description_parts[0] if description_parts else ""
                
                # Replace the section with description + new API table
                new_section = f"{description_line}\n\n{api_table}"
                updated_content = updated_content[:section_start] + new_section + updated_content[section_end:]
            else:
                print(f"Warning: Could not find section for category {category_name} in README")
        except Exception as e:
            print(f"Error updating category {category.get('name', 'unknown')}: {e}")
            continue
    
    return updated_content


def update_metadata(readme_content: str, api_data: Dict[str, Any]) -> str:
    """Update metadata in the README (last updated date, total APIs count)."""
    updated_content = readme_content
    
    # Update last updated date
    today = datetime.datetime.now().strftime('%B %d, %Y')
    date_pattern = r"<p align=\"center\">Last updated: .*?</p>"
    updated_content = re.sub(date_pattern, f"<p align=\"center\">Last updated: {today}</p>", updated_content)
    
    # Update total APIs count if present
    total_apis = api_data['metadata']['total_apis']
    apis_count_pattern = r"(\d+)\+ categories"
    if re.search(apis_count_pattern, updated_content):
        updated_content = re.sub(apis_count_pattern, f"{total_apis}+ APIs across 40+ categories", updated_content)
    
    return updated_content


def main():
    """Main function to update the README with API data."""
    print("Starting README update process...")
    
    # Load API data and README content
    api_data = load_api_data()
    readme_content = load_readme()
    
    if not readme_content:
        print("README content is empty. Aborting.")
        return
    
    # Update category sections with API tables
    updated_content = update_category_sections(readme_content, api_data)
    
    # Update metadata (last updated date, total APIs)
    updated_content = update_metadata(updated_content, api_data)
    
    # Save the updated README
    save_readme(updated_content)
    
    print("README update process completed.")


if __name__ == "__main__":
    main()
