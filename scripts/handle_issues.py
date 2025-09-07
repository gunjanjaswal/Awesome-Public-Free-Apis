#!/usr/bin/env python3
"""
Automatic Issue Handler

This script automatically processes GitHub issues:
1. Processes API suggestions and adds them to the collection
2. Handles reports of non-working APIs
3. Responds to issues with appropriate comments
"""

import json
import os
import sys
import re
import datetime
import requests
from typing import Dict, List, Any, Optional

# Constants
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(ROOT_DIR, 'data', 'apis.json')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_OWNER = os.environ.get('GITHUB_REPOSITORY_OWNER')
REPO_NAME = os.environ.get('GITHUB_REPOSITORY').split('/')[1] if os.environ.get('GITHUB_REPOSITORY') else None


def load_api_data() -> Dict[str, Any]:
    """Load API data from the JSON file."""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading API data: {e}")
        return {"categories": [], "metadata": {"total_apis": 0}}


def save_api_data(data: Dict[str, Any]) -> None:
    """Save API data to the JSON file."""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)
        print(f"API data saved to {DATA_FILE}")
    except Exception as e:
        print(f"Error saving API data: {e}")


def get_open_issues() -> List[Dict[str, Any]]:
    """Get open issues from GitHub."""
    if not GITHUB_TOKEN or not REPO_OWNER or not REPO_NAME:
        print("GitHub environment variables not set. Skipping issue processing.")
        return []
        
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    params = {'state': 'open'}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching GitHub issues: {e}")
        return []


def comment_on_issue(issue_number: int, comment: str) -> bool:
    """Add a comment to a GitHub issue."""
    if not GITHUB_TOKEN or not REPO_OWNER or not REPO_NAME:
        print("GitHub environment variables not set. Skipping comment.")
        return False
        
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}/comments"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {'body': comment}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Error commenting on issue: {e}")
        return False


def close_issue(issue_number: int) -> bool:
    """Close a GitHub issue."""
    if not GITHUB_TOKEN or not REPO_OWNER or not REPO_NAME:
        print("GitHub environment variables not set. Skipping issue closing.")
        return False
        
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {'state': 'closed'}
    
    try:
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Error closing issue: {e}")
        return False


def extract_api_suggestion(issue_body: str) -> Optional[Dict[str, Any]]:
    """Extract API details from an issue suggesting a new API."""
    # Common patterns in API suggestion issues
    name_pattern = r"API Name:?\s*(.+?)(?:\n|$)"
    url_pattern = r"API (?:Documentation )?URL:?\s*(.+?)(?:\n|$)"
    description_pattern = r"API Description:?\s*(.+?)(?:\n|$)"
    auth_pattern = r"Authentication Type:?\s*(.+?)(?:\n|$)"
    https_pattern = r"HTTPS Support:?\s*(.+?)(?:\n|$)"
    cors_pattern = r"CORS Support:?\s*(.+?)(?:\n|$)"
    category_pattern = r"Category:?\s*(.+?)(?:\n|$)"
    
    # Extract information
    name_match = re.search(name_pattern, issue_body, re.IGNORECASE)
    url_match = re.search(url_pattern, issue_body, re.IGNORECASE)
    description_match = re.search(description_pattern, issue_body, re.IGNORECASE)
    auth_match = re.search(auth_pattern, issue_body, re.IGNORECASE)
    https_match = re.search(https_pattern, issue_body, re.IGNORECASE)
    cors_match = re.search(cors_pattern, issue_body, re.IGNORECASE)
    category_match = re.search(category_pattern, issue_body, re.IGNORECASE)
    
    # If we don't have at least a name and URL, it's not a valid API suggestion
    if not name_match or not url_match:
        return None
        
    # Create API object
    api = {
        'name': name_match.group(1).strip(),
        'url': url_match.group(1).strip(),
        'description': description_match.group(1).strip() if description_match else "",
        'auth': auth_match.group(1).strip() if auth_match else "unknown",
        'https': https_match.group(1).lower() in ('yes', 'true', 'y') if https_match else True,
        'cors': cors_match.group(1).lower() if cors_match else "unknown",
        'category': category_match.group(1).strip() if category_match else "Development",
        'popularity': 70,  # Default popularity for user-suggested APIs
        'status': 'active',
        'last_checked': datetime.datetime.now().isoformat()
    }
    
    return api


def extract_non_working_api(issue_body: str) -> Optional[Dict[str, str]]:
    """Extract details about a non-working API from an issue."""
    # Common patterns in non-working API reports
    name_pattern = r"API Name:?\s*(.+?)(?:\n|$)"
    category_pattern = r"Category:?\s*(.+?)(?:\n|$)"
    
    # Extract information
    name_match = re.search(name_pattern, issue_body, re.IGNORECASE)
    category_match = re.search(category_pattern, issue_body, re.IGNORECASE)
    
    if not name_match:
        return None
        
    return {
        'name': name_match.group(1).strip(),
        'category': category_match.group(1).strip() if category_match else None
    }


def add_api_to_data(api_data: Dict[str, Any], new_api: Dict[str, Any]) -> bool:
    """Add a new API to the data if it doesn't already exist."""
    # Find the appropriate category
    category_name = new_api.get('category', 'Development')
    category_found = False
    
    for category in api_data['categories']:
        if category['name'] == category_name:
            category_found = True
            
            # Check if API already exists
            for existing_api in category['apis']:
                if existing_api['name'].lower() == new_api['name'].lower():
                    return False  # API already exists
            
            # Add the new API
            category['apis'].append(new_api)
            
            # Update metadata
            api_data['metadata']['total_apis'] += 1
            api_data['metadata']['last_updated'] = datetime.datetime.now().isoformat()
            
            return True
    
    # If category not found, default to Development
    if not category_found:
        for category in api_data['categories']:
            if category['name'] == 'Development':
                category['apis'].append(new_api)
                
                # Update metadata
                api_data['metadata']['total_apis'] += 1
                api_data['metadata']['last_updated'] = datetime.datetime.now().isoformat()
                
                return True
    
    return False


def mark_api_inactive(api_data: Dict[str, Any], api_info: Dict[str, str]) -> bool:
    """Mark an API as inactive in the data."""
    api_name = api_info['name']
    category_name = api_info.get('category')
    
    # If category is specified, only look in that category
    if category_name:
        for category in api_data['categories']:
            if category['name'] == category_name:
                for api in category['apis']:
                    if api['name'].lower() == api_name.lower():
                        api['status'] = 'inactive'
                        api['last_checked'] = datetime.datetime.now().isoformat()
                        return True
    # Otherwise, look in all categories
    else:
        for category in api_data['categories']:
            for api in category['apis']:
                if api['name'].lower() == api_name.lower():
                    api['status'] = 'inactive'
                    api['last_checked'] = datetime.datetime.now().isoformat()
                    return True
    
    return False


def process_issues():
    """Process open GitHub issues."""
    # Load API data
    api_data = load_api_data()
    data_modified = False
    
    # Get open issues
    issues = get_open_issues()
    
    for issue in issues:
        issue_number = issue['number']
        issue_title = issue['title']
        issue_body = issue['body'] or ""
        
        # Process API suggestions
        if '[API Suggestion]' in issue_title:
            print(f"Processing API suggestion: {issue_title}")
            
            # Extract API details
            new_api = extract_api_suggestion(issue_body)
            
            if new_api:
                # Add API to data
                if add_api_to_data(api_data, new_api):
                    data_modified = True
                    
                    # Comment on the issue
                    comment = f"Thank you for suggesting the {new_api['name']} API! It has been added to our collection in the {new_api['category']} category."
                    comment_on_issue(issue_number, comment)
                    
                    # Close the issue
                    close_issue(issue_number)
                else:
                    # API already exists
                    comment = f"Thank you for your suggestion, but the {new_api['name']} API is already in our collection."
                    comment_on_issue(issue_number, comment)
                    close_issue(issue_number)
            else:
                # Invalid API suggestion
                comment = "Thank you for your suggestion, but we couldn't extract the necessary API details from your issue. Please make sure to include at least the API name and URL."
                comment_on_issue(issue_number, comment)
        
        # Process non-working API reports
        elif '[Non-working API]' in issue_title:
            print(f"Processing non-working API report: {issue_title}")
            
            # Extract API details
            api_info = extract_non_working_api(issue_body)
            
            if api_info:
                # Mark API as inactive
                if mark_api_inactive(api_data, api_info):
                    data_modified = True
                    
                    # Comment on the issue
                    comment = f"Thank you for reporting that the {api_info['name']} API is not working. We've marked it as inactive in our collection."
                    comment_on_issue(issue_number, comment)
                    
                    # Close the issue
                    close_issue(issue_number)
                else:
                    # API not found
                    comment = f"Thank you for your report, but we couldn't find the {api_info['name']} API in our collection."
                    comment_on_issue(issue_number, comment)
                    close_issue(issue_number)
            else:
                # Invalid report
                comment = "Thank you for your report, but we couldn't extract the necessary API details from your issue. Please make sure to include at least the API name."
                comment_on_issue(issue_number, comment)
    
    # Save modified data
    if data_modified:
        save_api_data(api_data)


if __name__ == "__main__":
    process_issues()
