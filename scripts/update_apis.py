#!/usr/bin/env python3
"""
API Status Checker and Updater

This script checks the status of APIs listed in the apis.json file and updates their information.
It verifies if the APIs are still active and updates their status and last checked timestamp.
"""

import json
import os
import requests
import time
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Any, Optional

# Constants
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'apis.json')
REQUEST_TIMEOUT = 10  # seconds
MAX_WORKERS = 10  # Maximum number of concurrent requests


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


def check_api_status(api: Dict[str, Any]) -> Dict[str, Any]:
    """Check if an API is active by making a request to its URL."""
    updated_api = api.copy()
    
    try:
        # Some APIs might not have a direct endpoint to test
        # We're just checking if the documentation site is up
        url = api.get('url', '')
        if not url:
            updated_api['status'] = 'unknown'
            return updated_api
            
        response = requests.head(url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        
        if response.status_code < 400:
            updated_api['status'] = 'active'
        else:
            updated_api['status'] = 'inactive'
            
    except requests.RequestException:
        updated_api['status'] = 'error'
    
    # Update the last checked timestamp
    updated_api['last_checked'] = datetime.datetime.now().isoformat()
    
    return updated_api


def update_apis(data: Dict[str, Any]) -> Dict[str, Any]:
    """Update the status of all APIs in the data."""
    updated_data = data.copy()
    total_apis = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        
        # Collect all APIs that need to be checked
        for category in updated_data['categories']:
            for api in category.get('apis', []):
                futures.append((executor.submit(check_api_status, api), category['name']))
        
        # Process results as they complete
        for future, category_name in futures:
            try:
                result = future.result()
                # Find the category and update the API
                for category in updated_data['categories']:
                    if category['name'] == category_name:
                        for i, api in enumerate(category['apis']):
                            if api['name'] == result['name']:
                                category['apis'][i] = result
                                total_apis += 1
                                print(f"Updated {result['name']} - Status: {result['status']}")
                                break
            except Exception as e:
                print(f"Error processing API: {e}")
    
    # Update metadata
    updated_data['metadata']['total_apis'] = total_apis
    updated_data['metadata']['last_updated'] = datetime.datetime.now().isoformat()
    
    return updated_data


def fetch_trending_apis() -> List[Dict[str, Any]]:
    """
    Fetch trending APIs from various sources.
    This is a placeholder function that would be implemented to find new popular APIs.
    """
    # In a real implementation, this would scrape sources like:
    # - GitHub trending repositories related to APIs
    # - API marketplaces like RapidAPI
    # - Developer forums and communities
    
    # For now, return an empty list as this would require external API calls
    return []


def add_new_apis(data: Dict[str, Any], new_apis: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Add new APIs to the appropriate categories."""
    updated_data = data.copy()
    
    for new_api in new_apis:
        category_name = new_api.get('category', '')
        
        # Find the appropriate category
        for category in updated_data['categories']:
            if category['name'].lower() == category_name.lower():
                # Check if API already exists
                api_exists = any(api['name'] == new_api['name'] for api in category['apis'])
                
                if not api_exists:
                    # Add required fields if missing
                    if 'status' not in new_api:
                        new_api['status'] = 'active'
                    if 'last_checked' not in new_api:
                        new_api['last_checked'] = datetime.datetime.now().isoformat()
                    
                    category['apis'].append(new_api)
                    print(f"Added new API: {new_api['name']} to category {category_name}")
                break
    
    return updated_data


def main():
    """Main function to update API information."""
    print("Starting API update process...")
    
    # Load current API data
    data = load_api_data()
    
    # Update existing APIs
    updated_data = update_apis(data)
    
    # Fetch and add trending APIs
    new_apis = fetch_trending_apis()
    if new_apis:
        updated_data = add_new_apis(updated_data, new_apis)
    
    # Save updated data
    save_api_data(updated_data)
    
    print("API update process completed.")


if __name__ == "__main__":
    main()
