#!/usr/bin/env python3
"""
Fix Category Links in README.md

This script updates the README.md file to use proper HTML anchor links
that work correctly on GitHub.
"""

import os
import re

# Constants
README_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')

def fix_category_links():
    """Fix category links in the README.md file."""
    try:
        with open(README_FILE, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Extract the category table
        table_start = content.find("<table>")
        table_end = content.find("</table>", table_start)
        
        if table_start == -1 or table_end == -1:
            print("Could not find category table in README.md")
            return False
        
        table_content = content[table_start:table_end + 8]
        
        # Find all category links in the table
        link_pattern = r'<a href="#([^"]+)">([^<]+)</a>'
        links = re.findall(link_pattern, table_content)
        
        # Create a dictionary of category names to their actual IDs
        category_ids = {}
        for anchor, name in links:
            # Extract the category name without emoji
            category_name = name.split(' ', 1)[1] if ' ' in name else name
            category_ids[category_name] = anchor
        
        # Find all category headers in the content
        header_pattern = r'<h3[^>]*>(.*?)</h3>'
        headers = re.findall(header_pattern, content)
        
        # Create a new table with correct links
        new_table_content = table_content
        for anchor, name in links:
            category_name = name.split(' ', 1)[1] if ' ' in name else name
            
            # Find the actual header in the content
            actual_header = None
            for header in headers:
                if category_name in header:
                    actual_header = header
                    break
            
            if actual_header:
                # Create a unique ID for this category
                unique_id = f"category-{category_name.lower().replace(' ', '-').replace('&', '').replace('_', '')}"
                
                # Replace the header with one that has the unique ID
                header_pattern = f'<h3[^>]*>{re.escape(actual_header)}</h3>'
                content = re.sub(header_pattern, f'<h3 id="{unique_id}">{actual_header}</h3>', content)
                
                # Update the link in the table
                old_link = f'<a href="#{anchor}">{name}</a>'
                new_link = f'<a href="#{unique_id}">{name}</a>'
                new_table_content = new_table_content.replace(old_link, new_link)
        
        # Replace the old table with the new one
        content = content.replace(table_content, new_table_content)
        
        # Write the updated content back to the README
        with open(README_FILE, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print("Fixed category links in README.md")
        return True
    
    except Exception as e:
        print(f"Error fixing category links: {e}")
        return False

if __name__ == "__main__":
    fix_category_links()
