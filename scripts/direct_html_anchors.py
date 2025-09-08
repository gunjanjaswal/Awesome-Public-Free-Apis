#!/usr/bin/env python3
"""
Create Direct HTML Anchors in README.md

This script adds direct HTML anchor tags before each category header
to ensure reliable linking on GitHub.
"""

import os
import re

# Constants
README_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')

def add_direct_html_anchors():
    """Add direct HTML anchor tags before each category header."""
    try:
        with open(README_FILE, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find all category headers in the content
        # Look for both Markdown headers and HTML headers
        header_patterns = [
            r'### (.*?)(?=\n)',  # Markdown headers
            r'<h3[^>]*>(.*?)</h3>'  # HTML headers
        ]
        
        # Process each header pattern
        for pattern in header_patterns:
            matches = re.finditer(pattern, content)
            
            # Process matches in reverse order to avoid messing up positions
            matches = list(matches)
            for match in reversed(matches):
                header_text = match.group(1)
                
                # Extract category name (remove emoji and badge if present)
                parts = header_text.split(' ')
                if len(parts) > 1:
                    # Skip first part (emoji) and any parts that look like badges
                    category_parts = []
                    for part in parts[1:]:
                        if not part.startswith('!['):
                            category_parts.append(part)
                    category_name = ' '.join(category_parts)
                else:
                    category_name = header_text
                
                # Create a unique anchor ID
                anchor_id = category_name.lower().replace(' ', '-').replace('&', '').replace('_', '')
                
                # Create direct HTML anchor tag
                anchor_tag = f'<a id="{anchor_id}"></a>'
                
                # Insert the anchor tag before the header
                start_pos = match.start()
                content = content[:start_pos] + anchor_tag + content[start_pos:]
        
        # Update the category table links
        table_start = content.find("<table>")
        table_end = content.find("</table>", table_start)
        
        if table_start != -1 and table_end != -1:
            table_content = content[table_start:table_end + 8]
            
            # Find all category links in the table
            link_pattern = r'<a href="#([^"]+)">([^<]+)</a>'
            
            # Process each link
            for match in re.finditer(link_pattern, table_content):
                old_anchor = match.group(1)
                link_text = match.group(2)
                
                # Extract category name from link text (remove emoji)
                parts = link_text.split(' ')
                if len(parts) > 1:
                    category_name = ' '.join(parts[1:])
                else:
                    category_name = link_text
                
                # Create the new anchor ID
                new_anchor = category_name.lower().replace(' ', '-').replace('&', '').replace('_', '')
                
                # Replace the old link with the new one
                old_link = match.group(0)
                new_link = f'<a href="#{new_anchor}">{link_text}</a>'
                table_content = table_content.replace(old_link, new_link)
            
            # Replace the old table with the new one
            content = content.replace(content[table_start:table_end + 8], table_content)
        
        # Write the updated content back to the README
        with open(README_FILE, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print("Added direct HTML anchors to README.md")
        return True
    
    except Exception as e:
        print(f"Error adding direct HTML anchors: {e}")
        return False

if __name__ == "__main__":
    add_direct_html_anchors()
