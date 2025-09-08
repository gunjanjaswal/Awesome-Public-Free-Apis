#!/usr/bin/env python3
"""
Fix Category Headings in README.md

This script fixes the heading style for each category title in the README.md file.
"""

import os
import re

# Constants
README_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')

def fix_category_headings():
    """Fix the heading style for each category title."""
    try:
        # Define the categories and their emojis
        categories = {
            'Authentication': '🔐',
            'Blockchain': '🔗',
            'Business': '💼',
            'Calendar': '📅',
            'Cloud Storage': '💾',
            'Communication': '💬',
            'Cryptocurrency': '💰',
            'Currency Exchange': '💱',
            'Data Validation': '✅',
            'Development': '👨‍💻',
            'Email': '📧',
            'Entertainment': '🎭',
            'Environment': '🌍',
            'Finance': '💵',
            'Food & Drink': '🍽️',
            'Games & Comics': '🎮',
            'Geocoding': '🗺️',
            'Government': '🏳️',
            'Health': '💉',
            'Jobs': '💼',
            'Machine Learning': '🤖',
            'Music': '🎵',
            'News': '📰',
            'Open Data': '📓',
            'Open Source Projects': '👨‍💻',
            'Patent': '📄',
            'Personality': '😎',
            'Phone': '📱',
            'Photography': '📸',
            'Science & Math': '🔬',
            'Security': '🔒',
            'Shopping': '🛍️',
            'Social': '👥',
            'Sports & Fitness': '⚽',
            'Test Data': '📋',
            'Text Analysis': '🔍',
            'Tracking': '📍',
            'Transportation': '🚌',
            'URL Shorteners': '🖇️',
            'Video': '🎥',
            'Weather': '⛅'
        }
        
        with open(README_FILE, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find all category sections and update their headings
        for category, emoji in categories.items():
            # Look for the category description
            description_pattern = f"{category}.*?APIs for.*?services"
            description_match = re.search(description_pattern, content)
            
            if description_match:
                # Find the start of the section
                section_start = content.rfind("###", 0, description_match.start())
                
                if section_start != -1:
                    # Find the end of the heading line
                    heading_end = content.find("\n", section_start)
                    
                    if heading_end != -1:
                        # Replace the heading with the standard format
                        old_heading = content[section_start:heading_end]
                        new_heading = f"### {emoji} {category}"
                        
                        content = content.replace(old_heading, new_heading)
        
        # Write the updated content back to the README
        with open(README_FILE, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print("Fixed category headings in README.md")
        return True
    
    except Exception as e:
        print(f"Error fixing category headings: {e}")
        return False

if __name__ == "__main__":
    fix_category_headings()
