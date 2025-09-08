#!/usr/bin/env python3
"""
Restore Table Design in README.md

This script restores the previous HTML table design in the README.md file
without using anchor links.
"""

import os
import re

# Constants
README_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')

def restore_table_design():
    """Restore the previous table design without anchor links."""
    try:
        with open(README_FILE, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find the current table in the content
        table_start = content.find("| 🔐 Authentication & Security")
        if table_start == -1:
            table_start = content.find("<table>")
        
        table_end = content.find("\n\n", table_start)
        if table_end == -1:
            table_end = content.find("</table>", table_start)
            if table_end != -1:
                table_end += 8  # Include the closing </table> tag
        
        if table_start == -1 or table_end == -1:
            print("Could not find category table in README.md")
            return False
        
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
        
        # Create the new HTML table
        new_table = "<table>\n<tr>\n"
        new_table += "  <th align=\"center\">🔐 Authentication & Security</th>\n"
        new_table += "  <th align=\"center\">🌐 Data & Content</th>\n"
        new_table += "  <th align=\"center\">💼 Business & Finance</th>\n"
        new_table += "  <th align=\"center\">🌍 Utilities & Tools</th>\n"
        new_table += "</tr>\n"
        
        # Find the maximum number of rows needed
        max_rows = max(len(column) for column in columns)
        
        # Generate the table rows
        for row in range(max_rows):
            new_table += "<tr>\n"
            
            for col in range(4):
                if row < len(columns[col]):
                    category = columns[col][row]
                    emoji = emojis.get(category, '💯')
                    
                    # Add the category without a link
                    new_table += f"  <td align=\"center\">{emoji} {category}</td>\n"
                else:
                    new_table += "  <td></td>\n"
            
            new_table += "</tr>\n"
        
        new_table += "</table>\n\n"
        
        # Replace the old table with the new one
        content = content[:table_start] + new_table + content[table_end:]
        
        # Write the updated content back to the README
        with open(README_FILE, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print("Restored table design in README.md")
        return True
    
    except Exception as e:
        print(f"Error restoring table design: {e}")
        return False

if __name__ == "__main__":
    restore_table_design()
