#!/usr/bin/env python3
"""
Fix README duplicates

This script removes duplicated API sections from the README.md file.
"""

import os
import re

# Constants
README_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')

def fix_readme_duplicates():
    """Remove duplicated API sections from the README.md file."""
    try:
        # Load README content
        with open(README_FILE, 'r', encoding='utf-8') as file:
            readme_content = file.read()
        
        # Find the API Categories section
        api_categories_heading = "## 📋 API Categories"
        api_categories_index = readme_content.find(api_categories_heading)
        
        if api_categories_index == -1:
            print("Could not find API Categories section in README.md")
            return
        
        # Find the categories list
        categories_list_start = readme_content.find("- [", api_categories_index)
        categories_list_end = readme_content.find("\n\n", categories_list_start)
        
        if categories_list_start == -1 or categories_list_end == -1:
            print("Could not find API Categories list in README.md")
            return
        
        # Find the start of the next major section after API Categories
        next_section_index = readme_content.find("## 🚀 Trending GitHub API Repositories")
        
        if next_section_index == -1:
            print("Could not find next section after API Categories in README.md")
            return
        
        # Check if there are duplicate API sections
        # This happens when the update script adds new API sections without removing old ones
        
        # Find all anchor tags for API categories
        anchor_pattern = r'<a id="([^"]+)"></a>'
        anchors = re.findall(anchor_pattern, readme_content)
        
        # Count occurrences of each anchor
        anchor_counts = {}
        for anchor in anchors:
            if anchor in anchor_counts:
                anchor_counts[anchor] += 1
            else:
                anchor_counts[anchor] = 1
        
        # If there are duplicates, fix the README
        duplicates_found = any(count > 1 for count in anchor_counts.values())
        
        if duplicates_found:
            print("Found duplicate API sections. Fixing README...")
            
            # Find the first API section after the categories list
            first_api_section_start = readme_content.find("<a id=", categories_list_end)
            
            if first_api_section_start == -1:
                print("Could not find first API section")
                return
            
            # Extract content before API sections, API sections, and content after
            content_before = readme_content[:first_api_section_start]
            
            # Find all unique API sections
            unique_sections = {}
            
            # Extract all API sections
            api_sections = []
            current_pos = first_api_section_start
            
            while current_pos < next_section_index and current_pos != -1:
                # Find the start of the next API section
                section_start = current_pos
                
                # Find the anchor ID
                anchor_match = re.search(r'<a id="([^"]+)"></a>', readme_content[section_start:section_start + 100])
                if not anchor_match:
                    break
                
                anchor_id = anchor_match.group(1)
                
                # Find the end of this section (start of next section or end of API sections)
                next_section_start = readme_content.find("<a id=", section_start + 20)
                if next_section_start == -1 or next_section_start > next_section_index:
                    section_end = next_section_index
                else:
                    section_end = next_section_start
                
                # Extract the section content
                section_content = readme_content[section_start:section_end]
                
                # Only keep the first occurrence of each section
                if anchor_id not in unique_sections:
                    unique_sections[anchor_id] = section_content
                
                # Move to the next section
                current_pos = next_section_start
            
            # Combine unique API sections
            api_sections_content = "".join(unique_sections.values())
            
            # Get content after API sections
            content_after = readme_content[next_section_index:]
            
            # Create the updated README content
            updated_readme_content = content_before + api_sections_content + content_after
            
            # Write the updated README
            with open(README_FILE, 'w', encoding='utf-8') as file:
                file.write(updated_readme_content)
            
            print(f"Fixed README.md by removing {sum(count - 1 for count in anchor_counts.values() if count > 1)} duplicate API sections")
        else:
            print("No duplicate API sections found in README.md")
        
    except Exception as e:
        print(f"Error fixing README.md: {e}")

def main():
    """Main function to fix README duplicates."""
    print("Starting README duplicate fix...")
    fix_readme_duplicates()
    print("README duplicate fix completed.")

if __name__ == "__main__":
    main()
