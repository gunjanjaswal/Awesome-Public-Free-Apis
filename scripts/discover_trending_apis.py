#!/usr/bin/env python3
"""
Trending API Discovery Script

This script discovers trending APIs from various sources and adds them to the apis.json file.
It uses web scraping and API calls to find popular and new APIs that should be added to the collection.
"""

import json
import os
import requests
import datetime
import re
import time
import random
import argparse
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
import feedparser

# Constants
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'apis.json')
REQUEST_TIMEOUT = 15  # seconds
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
]


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


def get_random_user_agent() -> str:
    """Return a random user agent to avoid being blocked by websites."""
    return random.choice(USER_AGENTS)


def scrape_rapidapi_hub() -> List[Dict[str, Any]]:
    """Scrape trending APIs from RapidAPI Hub."""
    apis = []
    try:
        headers = {'User-Agent': get_random_user_agent()}
        url = 'https://rapidapi.com/collections/trending'
        
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            print(f"Failed to fetch RapidAPI Hub: {response.status_code}")
            return apis
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This is a placeholder for the actual scraping logic
        # The exact selectors would depend on the website structure
        api_cards = soup.select('.api-card')  # Adjust selector based on actual page structure
        
        for card in api_cards:
            try:
                name_elem = card.select_one('.api-name')
                desc_elem = card.select_one('.api-description')
                url_elem = card.select_one('a')
                category_elem = card.select_one('.api-category')
                
                if name_elem and url_elem:
                    name = name_elem.text.strip()
                    description = desc_elem.text.strip() if desc_elem else ""
                    url = 'https://rapidapi.com' + url_elem['href'] if url_elem.get('href') else ""
                    category = category_elem.text.strip() if category_elem else "Development"
                    
                    # Only add if we have at least a name and URL
                    if name and url:
                        apis.append({
                            'name': name,
                            'description': description,
                            'url': url,
                            'category': map_category_name(category),
                            'auth': 'apiKey',  # Most RapidAPI APIs use API keys
                            'https': True,
                            'cors': 'unknown',
                            'popularity': 80,  # Default popularity for trending APIs
                            'status': 'active',
                            'last_checked': datetime.datetime.now().isoformat()
                        })
            except Exception as e:
                print(f"Error parsing API card: {e}")
                
    except Exception as e:
        print(f"Error scraping RapidAPI Hub: {e}")
        
    return apis


def scrape_github_trending() -> List[Dict[str, Any]]:
    """Scrape trending API repositories from GitHub."""
    apis = []
    try:
        headers = {'User-Agent': get_random_user_agent()}
        # Search for repositories with "api" in the name or description that are trending
        url = 'https://github.com/trending/javascript?since=monthly'
        
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            print(f"Failed to fetch GitHub trending: {response.status_code}")
            return apis
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This is a placeholder for the actual scraping logic
        # The exact selectors would depend on the website structure
        repo_items = soup.select('article.Box-row')
        
        for item in repo_items:
            try:
                # Check if the repository is API-related
                description_elem = item.select_one('p')
                if not description_elem:
                    continue
                    
                description = description_elem.text.strip()
                if 'api' not in description.lower() and 'sdk' not in description.lower():
                    continue
                
                name_elem = item.select_one('h2 a')
                if not name_elem:
                    continue
                    
                repo_path = name_elem.get('href', '')
                if not repo_path:
                    continue
                    
                repo_name = repo_path.split('/')[-1]
                repo_url = f"https://github.com{repo_path}"
                
                # Determine category based on description keywords
                category = determine_category_from_description(description)
                
                apis.append({
                    'name': repo_name,
                    'description': description,
                    'url': repo_url,
                    'category': category,
                    'auth': 'unknown',
                    'https': True,
                    'cors': 'unknown',
                    'popularity': 85,  # Default popularity for GitHub trending
                    'status': 'active',
                    'last_checked': datetime.datetime.now().isoformat()
                })
            except Exception as e:
                print(f"Error parsing GitHub repo: {e}")
                
    except Exception as e:
        print(f"Error scraping GitHub trending: {e}")
        
    return apis


def scrape_programmableweb() -> List[Dict[str, Any]]:
    """Scrape new APIs from ProgrammableWeb."""
    apis = []
    try:
        headers = {'User-Agent': get_random_user_agent()}
        url = 'https://www.programmableweb.com/category/all/apis'
        
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            print(f"Failed to fetch ProgrammableWeb: {response.status_code}")
            return apis
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This is a placeholder for the actual scraping logic
        api_rows = soup.select('tr.views-row')
        
        for row in api_rows:
            try:
                name_elem = row.select_one('td.views-field-title a')
                category_elem = row.select_one('td.views-field-field-article-primary-category a')
                
                if name_elem:
                    name = name_elem.text.strip()
                    url = 'https://www.programmableweb.com' + name_elem['href'] if name_elem.get('href') else ""
                    category = category_elem.text.strip() if category_elem else "Development"
                    
                    # Get more details from the API page
                    if url:
                        time.sleep(1)  # Be nice to the server
                        api_response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
                        if api_response.status_code == 200:
                            api_soup = BeautifulSoup(api_response.text, 'html.parser')
                            desc_elem = api_soup.select_one('div.api_description')
                            description = desc_elem.text.strip() if desc_elem else ""
                            
                            apis.append({
                                'name': name,
                                'description': description,
                                'url': url,
                                'category': map_category_name(category),
                                'auth': 'unknown',
                                'https': True,
                                'cors': 'unknown',
                                'popularity': 75,  # Default popularity
                                'status': 'active',
                                'last_checked': datetime.datetime.now().isoformat()
                            })
            except Exception as e:
                print(f"Error parsing ProgrammableWeb API: {e}")
                
    except Exception as e:
        print(f"Error scraping ProgrammableWeb: {e}")
        
    return apis


def map_category_name(external_category: str) -> str:
    """Map external category names to our internal category structure."""
    category_mapping = {
        # Common mappings from external sources to our categories
        'weather': 'Weather',
        'map': 'Geocoding',
        'maps': 'Geocoding',
        'geo': 'Geocoding',
        'location': 'Geocoding',
        'finance': 'Finance',
        'financial': 'Finance',
        'banking': 'Finance',
        'payment': 'Finance',
        'social': 'Social',
        'media': 'Social',
        'messaging': 'Communication',
        'sms': 'Communication',
        'email': 'Email',
        'mail': 'Email',
        'image': 'Photography',
        'photo': 'Photography',
        'video': 'Video',
        'movie': 'Entertainment',
        'music': 'Music',
        'audio': 'Music',
        'news': 'News',
        'sport': 'Sports & Fitness',
        'fitness': 'Sports & Fitness',
        'health': 'Health',
        'medical': 'Health',
        'food': 'Food & Drink',
        'drink': 'Food & Drink',
        'job': 'Jobs',
        'career': 'Jobs',
        'employment': 'Jobs',
        'science': 'Science & Math',
        'math': 'Science & Math',
        'ai': 'Machine Learning',
        'ml': 'Machine Learning',
        'machine learning': 'Machine Learning',
        'artificial intelligence': 'Machine Learning',
        'security': 'Security',
        'authentication': 'Authentication',
        'auth': 'Authentication',
        'identity': 'Authentication',
        'blockchain': 'Blockchain',
        'crypto': 'Cryptocurrency',
        'bitcoin': 'Cryptocurrency',
        'ethereum': 'Cryptocurrency',
        'currency': 'Currency Exchange',
        'exchange': 'Currency Exchange',
        'forex': 'Currency Exchange',
        'business': 'Business',
        'calendar': 'Calendar',
        'schedule': 'Calendar',
        'storage': 'Cloud Storage',
        'cloud': 'Cloud Storage',
        'file': 'Cloud Storage',
        'validation': 'Data Validation',
        'verify': 'Data Validation',
        'development': 'Development',
        'dev': 'Development',
        'code': 'Development',
        'environment': 'Environment',
        'climate': 'Environment',
        'game': 'Games & Comics',
        'comic': 'Games & Comics',
        'government': 'Government',
        'gov': 'Government',
        'open data': 'Open Data',
        'dataset': 'Open Data',
        'open source': 'Open Source Projects',
        'oss': 'Open Source Projects',
        'patent': 'Patent',
        'ip': 'Patent',
        'personality': 'Personality',
        'psychology': 'Personality',
        'phone': 'Phone',
        'telecom': 'Phone',
        'shopping': 'Shopping',
        'ecommerce': 'Shopping',
        'e-commerce': 'Shopping',
        'retail': 'Shopping',
        'test': 'Test Data',
        'mock': 'Test Data',
        'dummy': 'Test Data',
        'text': 'Text Analysis',
        'nlp': 'Text Analysis',
        'language': 'Text Analysis',
        'tracking': 'Tracking',
        'monitor': 'Tracking',
        'analytics': 'Tracking',
        'transport': 'Transportation',
        'transit': 'Transportation',
        'travel': 'Transportation',
        'url': 'URL Shorteners',
        'shortener': 'URL Shorteners'
    }
    
    # Convert to lowercase for matching
    external_category_lower = external_category.lower()
    
    # Try to find a direct match
    for key, value in category_mapping.items():
        if key in external_category_lower:
            return value
    
    # Default to Development if no match found
    return 'Development'


def determine_category_from_description(description: str) -> str:
    """Determine the category based on the description text."""
    # Simply reuse our mapping function
    return map_category_name(description)


def is_api_duplicate(api: Dict[str, Any], existing_apis: List[Dict[str, Any]]) -> bool:
    """Check if an API already exists in our collection."""
    for existing_api in existing_apis:
        # Check for name similarity
        if api['name'].lower() == existing_api['name'].lower():
            return True
        
        # Check for URL similarity (ignoring protocol and www)
        api_url = api.get('url', '').lower()
        existing_url = existing_api.get('url', '').lower()
        
        if api_url and existing_url:
            # Strip protocol and www
            api_url = re.sub(r'^https?://(www\.)?', '', api_url)
            existing_url = re.sub(r'^https?://(www\.)?', '', existing_url)
            
            if api_url == existing_url:
                return True
    
    return False


def add_new_apis(data: Dict[str, Any], new_apis: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Add new APIs to the appropriate categories."""
    updated_data = data.copy()
    added_count = 0
    
    for new_api in new_apis:
        category_name = new_api.get('category', 'Development')
        
        # Find the appropriate category
        for category in updated_data['categories']:
            if category['name'] == category_name:
                # Check if API already exists
                if not is_api_duplicate(new_api, category['apis']):
                    # Add required fields if missing
                    if 'status' not in new_api:
                        new_api['status'] = 'active'
                    if 'last_checked' not in new_api:
                        new_api['last_checked'] = datetime.datetime.now().isoformat()
                    
                    category['apis'].append(new_api)
                    added_count += 1
                    print(f"Added new API: {new_api['name']} to category {category_name}")
                break
    
    # Update metadata
    total_apis = sum(len(category['apis']) for category in updated_data['categories'])
    updated_data['metadata']['total_apis'] = total_apis
    updated_data['metadata']['last_updated'] = datetime.datetime.now().isoformat()
    
    print(f"Added {added_count} new APIs")
    return updated_data


def scrape_public_apis_repository() -> List[Dict[str, Any]]:
    """Scrape APIs from the public-apis/public-apis repository."""
    apis = []
    try:
        headers = {'User-Agent': get_random_user_agent()}
        url = 'https://raw.githubusercontent.com/public-apis/public-apis/master/README.md'
        
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            print(f"Failed to fetch public-apis repository: {response.status_code}")
            return apis
            
        content = response.text
        
        # Parse markdown sections
        category_pattern = r'### (.+?)\n\n(.+?)(?=\n\n### |$)'
        category_matches = re.findall(category_pattern, content, re.DOTALL)
        
        for category_name, category_content in category_matches:
            # Parse table rows
            api_pattern = r'\[(.*?)\]\((.*?)\) \| (.*?) \| (.*?) \| (.*?) \| (.*?)\n'
            api_matches = re.findall(api_pattern, category_content)
            
            for api_name, api_url, api_desc, auth, https, cors in api_matches:
                apis.append({
                    'name': api_name,
                    'description': api_desc,
                    'url': api_url,
                    'category': map_category_name(category_name),
                    'auth': auth,
                    'https': https.lower() == 'yes',
                    'cors': cors.lower(),
                    'popularity': 80,
                    'status': 'active',
                    'last_checked': datetime.datetime.now().isoformat()
                })
                
    except Exception as e:
        print(f"Error scraping public-apis repository: {e}")
        
    return apis


def scrape_apilist_fun() -> List[Dict[str, Any]]:
    """Scrape APIs from apilist.fun."""
    apis = []
    try:
        headers = {'User-Agent': get_random_user_agent()}
        url = 'https://apilist.fun/'
        
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            print(f"Failed to fetch apilist.fun: {response.status_code}")
            return apis
            
        soup = BeautifulSoup(response.text, 'html.parser')
        api_items = soup.select('.api-entry')
        
        for item in api_items:
            try:
                name_elem = item.select_one('.api-name')
                desc_elem = item.select_one('.api-description')
                url_elem = item.select_one('a.api-url')
                category_elem = item.select_one('.api-category')
                
                if name_elem and url_elem:
                    name = name_elem.text.strip()
                    description = desc_elem.text.strip() if desc_elem else ""
                    url = url_elem['href']
                    category = category_elem.text.strip() if category_elem else "Development"
                    
                    apis.append({
                        'name': name,
                        'description': description,
                        'url': url,
                        'category': map_category_name(category),
                        'auth': 'unknown',
                        'https': True,
                        'cors': 'unknown',
                        'popularity': 75,
                        'status': 'active',
                        'last_checked': datetime.datetime.now().isoformat()
                    })
            except Exception as e:
                print(f"Error parsing API entry: {e}")
                
    except Exception as e:
        print(f"Error scraping apilist.fun: {e}")
        
    return apis


def scrape_apis_guru() -> List[Dict[str, Any]]:
    """Scrape APIs from APIs.guru."""
    apis = []
    try:
        headers = {'User-Agent': get_random_user_agent()}
        url = 'https://api.apis.guru/v2/list.json'
        
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            print(f"Failed to fetch APIs.guru: {response.status_code}")
            return apis
            
        data = response.json()
        
        for api_name, api_versions in data.items():
            try:
                api_info = api_versions['versions'][list(api_versions['versions'].keys())[0]]
                
                name = api_info['info']['title']
                description = api_info['info'].get('description', '')
                api_url = api_info['info'].get('contact', {}).get('url', '')
                
                # Extract category from tags
                category = 'Development'
                if 'tags' in api_info['info'] and api_info['info']['tags']:
                    category = map_category_name(api_info['info']['tags'][0])
                
                apis.append({
                    'name': name,
                    'description': description[:200] + '...' if len(description) > 200 else description,
                    'url': api_url or f"https://apis.guru/#{api_name}",
                    'category': category,
                    'auth': 'unknown',
                    'https': True,
                    'cors': 'unknown',
                    'popularity': 70,
                    'status': 'active',
                    'last_checked': datetime.datetime.now().isoformat()
                })
            except Exception as e:
                print(f"Error parsing API entry: {e}")
                
    except Exception as e:
        print(f"Error scraping APIs.guru: {e}")
        
    return apis


def scrape_any_api() -> List[Dict[str, Any]]:
    """Scrape APIs from any-api.com."""
    apis = []
    try:
        headers = {'User-Agent': get_random_user_agent()}
        url = 'https://any-api.com/'
        
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            print(f"Failed to fetch any-api.com: {response.status_code}")
            return apis
            
        soup = BeautifulSoup(response.text, 'html.parser')
        api_items = soup.select('.api-box')
        
        for item in api_items:
            try:
                name_elem = item.select_one('.api-title')
                url_elem = item.select_one('a')
                
                if name_elem and url_elem:
                    name = name_elem.text.strip()
                    url = 'https://any-api.com' + url_elem['href'] if url_elem.get('href') else ""
                    
                    # Visit the API page to get more details
                    if url:
                        time.sleep(0.5)  # Be nice to the server
                        api_response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
                        if api_response.status_code == 200:
                            api_soup = BeautifulSoup(api_response.text, 'html.parser')
                            desc_elem = api_soup.select_one('.api-description')
                            category_elem = api_soup.select_one('.api-category')
                            
                            description = desc_elem.text.strip() if desc_elem else ""
                            category = category_elem.text.strip() if category_elem else "Development"
                            
                            apis.append({
                                'name': name,
                                'description': description,
                                'url': url,
                                'category': map_category_name(category),
                                'auth': 'unknown',
                                'https': True,
                                'cors': 'unknown',
                                'popularity': 65,
                                'status': 'active',
                                'last_checked': datetime.datetime.now().isoformat()
                            })
            except Exception as e:
                print(f"Error parsing API entry: {e}")
                
    except Exception as e:
        print(f"Error scraping any-api.com: {e}")
        
    return apis


def verify_api(api: Dict[str, Any]) -> Dict[str, Any]:
    """Verify if an API is working and update its information."""
    try:
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.head(api['url'], headers=headers, timeout=5)
        
        # Update API status based on response
        if response.status_code < 400:
            api['status'] = 'active'
        else:
            api['status'] = 'inactive'
            
        # Try to detect CORS support
        if 'Access-Control-Allow-Origin' in response.headers:
            api['cors'] = 'yes'
            
        # Try to detect HTTPS support
        api['https'] = api['url'].startswith('https')
        
    except requests.RequestException:
        # Don't mark as inactive on first check
        pass
        
    return api


def add_new_apis(data: Dict[str, Any], new_apis: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Add new APIs to the appropriate categories with priority to empty categories."""
    updated_data = data.copy()
    added_count = 0
    
    # First, identify empty categories
    empty_categories = []
    for category in updated_data['categories']:
        if len(category['apis']) == 0:
            empty_categories.append(category['name'])
    
    # Sort APIs by category, prioritizing those that would fill empty categories
    prioritized_apis = sorted(
        new_apis,
        key=lambda api: 0 if api.get('category') in empty_categories else 1
    )
    
    # Process APIs with priority given to empty categories
    for new_api in prioritized_apis:
        category_name = new_api.get('category', 'Development')
        
        # Find the appropriate category
        for category in updated_data['categories']:
            if category['name'] == category_name:
                # Check if API already exists
                if not is_api_duplicate(new_api, category['apis']):
                    # Verify API before adding
                    new_api = verify_api(new_api)
                    
                    # Add required fields if missing
                    if 'status' not in new_api:
                        new_api['status'] = 'active'
                    if 'last_checked' not in new_api:
                        new_api['last_checked'] = datetime.datetime.now().isoformat()
                    
                    category['apis'].append(new_api)
                    added_count += 1
                    print(f"Added new API: {new_api['name']} to category {category_name}")
                break
    
    # Update metadata
    total_apis = sum(len(category['apis']) for category in updated_data['categories'])
    updated_data['metadata']['total_apis'] = total_apis
    updated_data['metadata']['last_updated'] = datetime.datetime.now().isoformat()
    
    print(f"Added {added_count} new APIs")
    return updated_data


def main():
    """Main function to discover trending APIs."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Discover trending APIs from various sources')
    parser.add_argument('--mode', choices=['regular', 'comprehensive'], default='regular',
                        help='Discovery mode: regular (weekly sources) or comprehensive (all sources)')
    args = parser.parse_args()
    
    print(f"Starting API discovery process in {args.mode} mode...")
    
    # Load current API data
    data = load_api_data()
    
    # Discover new APIs from various sources
    new_apis = []
    
    # Sources for regular (weekly) discovery
    # These are faster and more reliable sources
    print("Scraping regular sources...")
    
    # RapidAPI Hub
    print("Scraping RapidAPI Hub...")
    rapidapi_apis = scrape_rapidapi_hub()
    new_apis.extend(rapidapi_apis)
    print(f"Found {len(rapidapi_apis)} APIs from RapidAPI Hub")
    
    # GitHub Trending
    print("Scraping GitHub Trending...")
    github_apis = scrape_github_trending()
    new_apis.extend(github_apis)
    print(f"Found {len(github_apis)} APIs from GitHub Trending")
    
    # Public APIs Repository (always included as it's very reliable)
    print("Scraping public-apis repository...")
    public_apis = scrape_public_apis_repository()
    new_apis.extend(public_apis)
    print(f"Found {len(public_apis)} APIs from public-apis repository")
    
    # Additional sources for comprehensive (monthly) discovery
    if args.mode == 'comprehensive':
        print("\nScraping additional sources for comprehensive discovery...")
        
        # ProgrammableWeb (can be slow and less reliable)
        print("Scraping ProgrammableWeb...")
        programmableweb_apis = scrape_programmableweb()
        new_apis.extend(programmableweb_apis)
        print(f"Found {len(programmableweb_apis)} APIs from ProgrammableWeb")
        
        # APIList.fun
        print("Scraping APIList.fun...")
        apilist_apis = scrape_apilist_fun()
        new_apis.extend(apilist_apis)
        print(f"Found {len(apilist_apis)} APIs from APIList.fun")
        
        # APIs.guru
        print("Scraping APIs.guru...")
        apis_guru_apis = scrape_apis_guru()
        new_apis.extend(apis_guru_apis)
        print(f"Found {len(apis_guru_apis)} APIs from APIs.guru")
        
        # Any-API
        print("Scraping Any-API...")
        any_api_apis = scrape_any_api()
        new_apis.extend(any_api_apis)
        print(f"Found {len(any_api_apis)} APIs from Any-API")
    
    # Add new APIs to the data
    if new_apis:
        print(f"\nProcessing {len(new_apis)} discovered APIs...")
        updated_data = add_new_apis(data, new_apis)
        
        # Save updated data
        save_api_data(updated_data)
    else:
        print("No new APIs discovered")
    
    print("API discovery process completed.")


if __name__ == "__main__":
    main()
