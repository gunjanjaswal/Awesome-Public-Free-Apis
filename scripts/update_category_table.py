#!/usr/bin/env python3
"""
Update Category Table in README.md

This script updates the category table in the README.md file to use links
that work correctly with GitHub's auto-generated section IDs.
"""

import os
import re

# Constants
README_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')

def update_category_table():
    """Update the category table in the README.md file."""
    try:
        with open(README_FILE, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find all category headers in the content
        header_pattern = r'###\s+(.*?)(?=\n)'
        headers = re.findall(header_pattern, content)
        
        # Create a mapping of category names to their positions in the file
        category_positions = {}
        for header in headers:
            # Extract category name (remove emoji and badge if present)
            parts = header.split(' ')
            if len(parts) > 1:
                # Skip first part (emoji) and any parts that look like badges
                category_parts = []
                for part in parts[1:]:
                    if not part.startswith('!['):
                        category_parts.append(part)
                category_name = ' '.join(category_parts)
            else:
                category_name = header
            
            # Store the position of this category in the file
            category_positions[category_name] = content.find('### ' + header)
        
        # Create a new table with direct links to each category
        new_table = """<table>
<tr>
  <th align="center">🔐 Authentication & Security</th>
  <th align="center">🌐 Data & Content</th>
  <th align="center">💼 Business & Finance</th>
  <th align="center">🌍 Utilities & Tools</th>
</tr>
"""
        
        # Define the categories for each column
        columns = [
            # Authentication & Security
            ["Authentication", "Blockchain", "Data Validation", "Security"],
            
            # Data & Content
            ["Cloud Storage", "Entertainment", "Games & Comics", "Music", 
             "News", "Open Data", "Open Source Projects", "Photography", "Video"],
            
            # Business & Finance
            ["Business", "Calendar", "Communication", "Cryptocurrency", 
             "Currency Exchange", "Finance", "Jobs", "Shopping"],
            
            # Utilities & Tools
            ["Development", "Email", "Environment", "Food & Drink", "Geocoding", 
             "Government", "Health", "Machine Learning", "Patent", "Personality", 
             "Phone", "Science & Math", "Social", "Sports & Fitness", "Test Data", 
             "Text Analysis", "Tracking", "Transportation", "URL Shorteners", "Weather"]
        ]
        
        # Define emojis for each category
        emojis = {
            'Authentication': '🔐', 'Blockchain': '🔗', 'Business': '💼',
            'Calendar': '📅', 'Cloud Storage': '💾', 'Communication': '💬',
            'Cryptocurrency': '💰', 'Currency Exchange': '💱', 'Data Validation': '✅',
            'Development': '👨‍💻', 'Email': '📧', 'Entertainment': '🎭',
            'Environment': '🌍', 'Finance': '💵', 'Food & Drink': '🍽️',
            'Games & Comics': '🎮', 'Geocoding': '🗺️', 'Government': '🏳️',
            'Health': '💉', 'Jobs': '💼', 'Machine Learning': '🤖',
            'Music': '🎵', 'News': '📰', 'Open Data': '📓',
            'Open Source Projects': '👨‍💻', 'Patent': '📄', 'Personality': '😎',
            'Phone': '📱', 'Photography': '📸', 'Science & Math': '🔬',
            'Security': '🔒', 'Shopping': '🛍️', 'Social': '👥',
            'Sports & Fitness': '⚽', 'Test Data': '📋', 'Text Analysis': '🔍',
            'Tracking': '📍', 'Transportation': '🚌', 'URL Shorteners': '🖇️',
            'Video': '🎥', 'Weather': '⛅'
        }
        
        # Find the maximum number of rows needed
        max_rows = max(len(column) for column in columns)
        
        # Generate the table rows
        for row in range(max_rows):
            new_table += "<tr>\n"
            
            for col in range(4):
                if row < len(columns[col]):
                    category = columns[col][row]
                    emoji = emojis.get(category, '💯')
                    
                    # Create a direct link to the category section
                    # GitHub's auto-generated IDs are lowercase with hyphens
                    anchor = category.lower().replace(' ', '-').replace('&', '')
                    
                    new_table += f'  <td align="center"><a href="#{anchor}">{emoji} {category}</a></td>\n'
                else:
                    new_table += "  <td></td>\n"
            
            new_table += "</tr>\n"
        
        new_table += "</table>\n\n"
        
        # Find the existing table in the content
        table_start = content.find("<table>")
        table_end = content.find("</table>", table_start)
        
        if table_start != -1 and table_end != -1:
            # Replace the old table with the new one
            content = content[:table_start] + new_table + content[table_end + 8:]
            
            # Write the updated content back to the README
            with open(README_FILE, 'w', encoding='utf-8') as file:
                file.write(content)
            
            print("Updated category table in README.md")
            return True
        else:
            print("Could not find category table in README.md")
            return False
    
    except Exception as e:
        print(f"Error updating category table: {e}")
        return False

if __name__ == "__main__":
    update_category_table()
