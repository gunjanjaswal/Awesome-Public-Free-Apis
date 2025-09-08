#!/usr/bin/env python3
"""
Fix README file

This script fixes the broken sections in the README.md file.
"""

import os
import re

# Constants
README_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')

def fix_readme():
    """Fix the broken sections in the README.md file."""
    try:
        # Load README content
        with open(README_FILE, 'r', encoding='utf-8') as file:
            readme_content = file.read()
        
        # Fix the broken authentication section
        auth_pattern = r'\| <a href="https://warrant\.dev/" target="_blank">Warrant</a> \| APIs for authorization and _API Categories last updated: .*?_'
        auth_replacement = '| <a href="https://warrant.dev/" target="_blank">Warrant</a> | APIs for authorization and access control | `apiKey` | Yes | yes |'
        readme_content = re.sub(auth_pattern, auth_replacement, readme_content)
        
        # Fix the broken weather section
        weather_pattern = r'_API Categories last updated: .*?_\s*\n\s*\*\*API Update Schedule:\*\*.*?\n.*?\n.*?\n.*?\n\s*Weather Service \| none \| Yes \| yes \|'
        weather_replacement = '| <a href="https://www.tomorrow.io/weather-api/" target="_blank">Tomorrow.io Weather API</a> | Weather API with forecasts, historical data, and severe weather alerts | `apiKey` | Yes | yes |'
        readme_content = re.sub(weather_pattern, weather_replacement, readme_content)
        
        # Remove duplicate API Update Schedule sections
        update_pattern = r'(\n_API Categories last updated: .*?_\s*\n\s*\*\*API Update Schedule:\*\*.*?\n.*?\n.*?\n.*?\n).*?- Enhanced API Discovery.*?\n.*?Monthly API Discovery.*?\n'
        update_replacement = r'\1'
        readme_content = re.sub(update_pattern, update_replacement, readme_content)
        
        # Write the fixed README
        with open(README_FILE, 'w', encoding='utf-8') as file:
            file.write(readme_content)
        
        print("Fixed README.md file")
        
    except Exception as e:
        print(f"Error fixing README.md: {e}")

def main():
    """Main function to fix README."""
    print("Starting README fix...")
    fix_readme()
    print("README fix completed.")

if __name__ == "__main__":
    main()
