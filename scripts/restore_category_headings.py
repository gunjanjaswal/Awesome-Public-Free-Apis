#!/usr/bin/env python3
"""
Restore Category Headings in README.md

This script restores the heading style for each category title in the README.md file.
"""

import os
import re

# Constants
README_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')

def restore_category_headings():
    """Restore the heading style for each category title."""
    try:
        with open(README_FILE, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find all category headers in the content
        # Look for both HTML headers and plain text headers
        header_patterns = [
            r'<h3[^>]*>(.*?)</h3>',  # HTML headers
            r'###\s+(.*?)(?=\n)'  # Markdown headers
        ]
        
        # Process each header pattern
        for pattern in header_patterns:
            # Find all matches
            matches = list(re.finditer(pattern, content))
            
            # Process matches in reverse order to avoid messing up positions
            for match in reversed(matches):
                header_text = match.group(1)
                
                # Create a standard Markdown header
                new_header = f"### {header_text}\n"
                
                # Replace the old header with the new one
                start_pos = match.start()
                end_pos = match.end()
                content = content[:start_pos] + new_header + content[end_pos + 1:]
        
        # Write the updated content back to the README
        with open(README_FILE, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print("Restored category headings in README.md")
        return True
    
    except Exception as e:
        print(f"Error restoring category headings: {e}")
        return False

if __name__ == "__main__":
    restore_category_headings()
