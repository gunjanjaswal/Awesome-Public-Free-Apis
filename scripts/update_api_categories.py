#!/usr/bin/env python3
"""
Script to update API categories in the README.md file while preserving the structure.
"""

import re
import json
import os
from typing import Dict, List, Any

def load_api_data(api_data_file: str) -> Dict[str, Any]:
    """Load API data from a JSON file."""
    try:
        with open(api_data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading API data: {e}")
        return {"categories": []}

def update_readme_api_categories(api_data: Dict[str, Any]) -> None:
    """Update API categories in the README.md file while preserving the structure."""
    try:
        readme_path = "README.md"
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Make a backup of the original README
        with open(f"{readme_path}.bak", 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Update each category section individually
        for category in api_data["categories"]:
            category_name = category["name"]
            category_description = category["description"]
            apis = category["apis"]
            
            # Skip categories with no APIs
            if not apis:
                print(f"Skipping empty category: {category_name}")
                continue
            
            # Find the category section
            section_start_pattern = f"### {category_name}\n"
            section_end_pattern = "\n\n###"
            
            start_pos = content.find(section_start_pattern)
            if start_pos == -1:
                # Category doesn't exist yet, add it before the next section
                print(f"Adding new category: {category_name}")
                
                # Find the position to insert the new category
                categories_section_start = content.find("## 📃 API Categories")
                if categories_section_start == -1:
                    print("Could not find API Categories section")
                    continue
                
                # Find the next section after API Categories
                next_section_pos = content.find("\n## ", categories_section_start + 1)
                if next_section_pos == -1:
                    print("Could not find the next section after API Categories")
                    continue
                
                # Create the new category section
                new_category_section = f"\n### {category_name}\n{category_description}\n\n"
                new_category_section += "| API | Description | Auth | HTTPS | CORS |\n"
                new_category_section += "| --- | --- | --- | --- | --- |\n"
                
                for api in apis:
                    name = api["name"]
                    if api["url"]:
                        name = f"[{name}]({api['url']})"
                    
                    https = "Yes" if api["https"] else "No"
                    
                    new_category_section += f"| {name} | {api['description']} | {api['auth']} | {https} | {api['cors']} |\n"
                
                new_category_section += "\n"
                
                # Add the new category to the content
                content = content[:next_section_pos] + new_category_section + content[next_section_pos:]
                
                # Also add to the category list at the top
                categories_list_end = content.find("\n\n###", categories_section_start)
                if categories_list_end != -1:
                    category_link = f"- [{category_name}](#{category_name.lower().replace(' ', '-').replace('&', '').replace('/', '')}) - {category_description.split(':')[0] if ':' in category_description else category_description}\n"
                    content = content[:categories_list_end] + category_link + content[categories_list_end:]
            else:
                # Category exists, update it
                print(f"Updating existing category: {category_name}")
                
                # Find the end of the category section
                end_pos = content.find(section_end_pattern, start_pos)
                if end_pos == -1:
                    # This might be the last category
                    next_section_pos = content.find("\n## ", start_pos)
                    if next_section_pos == -1:
                        print(f"Could not find the end of category {category_name}")
                        continue
                    end_pos = next_section_pos
                
                # Extract the section to replace
                section_to_replace = content[start_pos:end_pos]
                
                # Create the updated category section
                new_category_section = f"### {category_name}\n{category_description}\n\n"
                new_category_section += "| API | Description | Auth | HTTPS | CORS |\n"
                new_category_section += "| --- | --- | --- | --- | --- |\n"
                
                for api in apis:
                    name = api["name"]
                    if api["url"]:
                        name = f"[{name}]({api['url']})"
                    
                    https = "Yes" if api["https"] else "No"
                    
                    new_category_section += f"| {name} | {api['description']} | {api['auth']} | {https} | {api['cors']} |\n"
                
                # Replace the old category section with the new one
                content = content.replace(section_to_replace, new_category_section)
        
        # Write the updated content
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("Successfully updated API categories in README.md")
    
    except Exception as e:
        print(f"Error updating README: {e}")
        # Restore from backup if something went wrong
        try:
            with open(f"{readme_path}.bak", 'r', encoding='utf-8') as f:
                backup_content = f.read()
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(backup_content)
            print("Restored README.md from backup after error")
        except Exception:
            print("Failed to restore README.md from backup")

def main():
    """Main function to update API categories in the README."""
    # Path to the API data file (created by discover_trending_apis.py)
    api_data_file = "api_data.json"
    
    # Check if the API data file exists
    if not os.path.exists(api_data_file):
        print(f"API data file {api_data_file} not found")
        return
    
    print(f"Found API data file: {api_data_file}")
    
    # Load API data
    api_data = load_api_data(api_data_file)
    print(f"Loaded API data with {len(api_data.get('categories', []))} categories")
    
    # Update README API categories
    update_readme_api_categories(api_data)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        print(f"Error in main function: {e}")
        traceback.print_exc()
