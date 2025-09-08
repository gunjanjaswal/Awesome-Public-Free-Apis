#!/usr/bin/env python3
"""
Fix Anchor Links in README.md

This script adds explicit HTML anchor tags before each section header
to ensure proper linking from the table of contents.
"""

import os
import re

# Constants
README_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')

def fix_anchors():
    """Add explicit HTML anchor tags before each section header."""
    try:
        with open(README_FILE, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find all section headers
        header_pattern = r'### (.*?)(?=\n)'
        headers = re.findall(header_pattern, content)
        
        # Process each header
        for header in headers:
            # Extract emoji and category name
            parts = header.split(' ')
            if len(parts) >= 2:
                emoji = parts[0]
                # Create anchor ID
                anchor_id = emoji
                
                # Add explicit HTML anchor tag before the header
                old_header = f"### {header}"
                new_header = f"<a id=\"{anchor_id}\"></a>\n### {header}"
                
                content = content.replace(old_header, new_header)
        
        # Write the updated content back to the README
        with open(README_FILE, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print("Added explicit HTML anchor tags to README.md")
        return True
    
    except Exception as e:
        print(f"Error adding HTML anchor tags: {e}")
        return False

if __name__ == "__main__":
    fix_anchors()
