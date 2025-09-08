#!/usr/bin/env python3
"""
Run All Updates Script

This script runs all update scripts to ensure the repository is fully updated.
It updates APIs, trending repositories, and trending API repositories.
"""

import os
import sys
import subprocess
import datetime

def run_script(script_name):
    """Run a Python script and return its output."""
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
    
    if not os.path.exists(script_path):
        print(f"Error: Script {script_path} not found")
        return False
    
    print(f"Running {script_name}...")
    try:
        result = subprocess.run([sys.executable, script_path], 
                               capture_output=True, 
                               text=True, 
                               check=True)
        print(result.stdout)
        if result.stderr:
            print(f"Errors: {result.stderr}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def update_readme_dates():
    """Update the dates in the README.md file."""
    readme_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')
    today = datetime.datetime.now().strftime('%B %d, %Y')
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Update dates in the README
        content = content.replace('_Last updated: September 7, 2025_', f'_Last updated: {today}_')
        content = content.replace('_Last updated: September 08, 2025_', f'_Last updated: {today}_')
        
        with open(readme_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"Updated dates in README.md to {today}")
        return True
    except Exception as e:
        print(f"Error updating README dates: {e}")
        return False

def ensure_data_directory():
    """Ensure the data directory exists."""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created data directory: {data_dir}")
    return True

def main():
    """Main function to run all updates."""
    print("Starting all updates...")
    
    # Ensure the data directory exists
    ensure_data_directory()
    
    # Run the enhanced API scrapers
    run_script('enhanced_api_scrapers.py')
    
    # Run the trending repositories update
    run_script('update_trending_repos.py')
    
    # Run the trending API repositories update
    run_script('update_trending_api_repos.py')
    
    # Update dates in the README
    update_readme_dates()
    
    print("All updates completed.")

if __name__ == "__main__":
    main()
