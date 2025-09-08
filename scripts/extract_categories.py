#!/usr/bin/env python3
"""
Extract categories from README navigation list

This script extracts all categories from the navigation list in the README file
and prints them for verification.
"""

import os
import re

# Constants
README_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')

def extract_categories():
    """Extract categories from the README navigation list."""
    try:
        # Load README content
        with open(README_FILE, 'r', encoding='utf-8') as file:
            readme_content = file.read()
        
        # Find the categories list section
        categories_start = readme_content.find("**Available Categories:**")
        if categories_start == -1:
            print("Could not find Available Categories section")
            return []
        
        categories_start = categories_start + len("**Available Categories:**")
        categories_end = readme_content.find("<a id=", categories_start)
        
        if categories_end == -1:
            print("Could not find end of categories list")
            return []
        
        categories_list = readme_content[categories_start:categories_end]
        
        # Extract category names and IDs using regex
        category_pattern = r'\[([^\]]+)\]\(#([^)]+)\)'
        categories = re.findall(category_pattern, categories_list)
        
        print(f"Found {len(categories)} categories in the navigation list:")
        for emoji_name, anchor_id in categories:
            print(f"- {emoji_name} -> {anchor_id}")
        
        return categories
    
    except Exception as e:
        print(f"Error extracting categories: {e}")
        return []

def main():
    """Main function."""
    print("Extracting categories from README navigation list...")
    extract_categories()
    print("Category extraction completed.")

if __name__ == "__main__":
    main()
