#!/usr/bin/env python3
"""
Enhanced API Scrapers

This script contains additional scrapers to discover high-quality free APIs
from various sources and add them to the apis.json file.
"""

import json
import os
import requests
import datetime
import re
import time
import random
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
        # Ensure the data directory exists
        data_dir = os.path.dirname(DATA_FILE)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"Created data directory: {data_dir}")
            
        # Try to load existing data
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            # Create a new data structure with all categories
            categories = [
                {"name": "Authentication", "description": "APIs related to authentication, authorization, and identity management", "apis": []},
                {"name": "Blockchain", "description": "APIs related to blockchain technology and distributed ledgers", "apis": []},
                {"name": "Business", "description": "APIs for business operations, CRM, ERP, and other business functions", "apis": []},
                {"name": "Calendar", "description": "APIs for calendar and scheduling functionality", "apis": []},
                {"name": "Cloud Storage", "description": "APIs for cloud storage and file management", "apis": []},
                {"name": "Communication", "description": "APIs for messaging, chat, and other communication services", "apis": []},
                {"name": "Cryptocurrency", "description": "APIs for cryptocurrency data and transactions", "apis": []},
                {"name": "Currency Exchange", "description": "APIs for currency exchange rates and conversions", "apis": []},
                {"name": "Data Validation", "description": "APIs for validating various types of data", "apis": []},
                {"name": "Development", "description": "APIs for software development tools and services", "apis": []},
                {"name": "Email", "description": "APIs for email services and functionality", "apis": []},
                {"name": "Entertainment", "description": "APIs for entertainment content and services", "apis": []},
                {"name": "Environment", "description": "APIs for environmental data and services", "apis": []},
                {"name": "Finance", "description": "APIs for financial data and services", "apis": []},
                {"name": "Food & Drink", "description": "APIs for food and drink related data and services", "apis": []},
                {"name": "Games & Comics", "description": "APIs for games, comics, and related content", "apis": []},
                {"name": "Geocoding", "description": "APIs for geocoding and geolocation services", "apis": []},
                {"name": "Government", "description": "APIs provided by government entities", "apis": []},
                {"name": "Health", "description": "APIs for health and medical data and services", "apis": []},
                {"name": "Jobs", "description": "APIs for job listings and employment data", "apis": []},
                {"name": "Machine Learning", "description": "APIs for machine learning and AI services", "apis": []},
                {"name": "Music", "description": "APIs for music data and services", "apis": []},
                {"name": "News", "description": "APIs for news content and services", "apis": []},
                {"name": "Open Data", "description": "APIs for open data sets and services", "apis": []},
                {"name": "Open Source Projects", "description": "APIs for open source project data and services", "apis": []},
                {"name": "Patent", "description": "APIs for patent data and services", "apis": []},
                {"name": "Personality", "description": "APIs for personality and psychology related data", "apis": []},
                {"name": "Phone", "description": "APIs for phone and SMS related services", "apis": []},
                {"name": "Photography", "description": "APIs for photography and image related services", "apis": []},
                {"name": "Science & Math", "description": "APIs for scientific and mathematical data and services", "apis": []},
                {"name": "Security", "description": "APIs for security related services", "apis": []},
                {"name": "Shopping", "description": "APIs for e-commerce and shopping related services", "apis": []},
                {"name": "Social", "description": "APIs for social media and social networking", "apis": []},
                {"name": "Sports & Fitness", "description": "APIs for sports and fitness data and services", "apis": []},
                {"name": "Test Data", "description": "APIs for generating test data", "apis": []},
                {"name": "Text Analysis", "description": "APIs for text analysis and natural language processing", "apis": []},
                {"name": "Tracking", "description": "APIs for tracking various types of data", "apis": []},
                {"name": "Transportation", "description": "APIs for transportation data and services", "apis": []},
                {"name": "URL Shorteners", "description": "APIs for URL shortening services", "apis": []},
                {"name": "Video", "description": "APIs for video content and services", "apis": []},
                {"name": "Weather", "description": "APIs for weather data and forecasts", "apis": []}
            ]
            
            data = {
                "categories": categories,
                "metadata": {
                    "total_apis": 0,
                    "last_updated": datetime.datetime.now().isoformat(),
                    "version": "1.0.0"
                }
            }
            
            print("Created new API data structure with all categories")
            return data
    except Exception as e:
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

def scrape_public_apis_github() -> List[Dict[str, Any]]:
    """Scrape APIs from the public-apis GitHub repository."""
    apis = []
    try:
        headers = {'User-Agent': get_random_user_agent()}
        url = 'https://raw.githubusercontent.com/public-apis/public-apis/master/README.md'
        
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            print(f"Failed to fetch public-apis GitHub: {response.status_code}")
            return apis
            
        content = response.text
        
        # Parse the markdown content to extract API information
        # The format is typically: | API Name | Description | Auth | HTTPS | CORS |
        pattern = r'\|\s*\[([^]]+)\]\(([^)]+)\)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|'
        matches = re.findall(pattern, content)
        
        current_category = "Development"  # Default category
        
        # Extract category headers
        category_pattern = r'#{2,3}\s+([^#\n]+)'
        category_matches = re.findall(category_pattern, content)
        
        for line in content.split('\n'):
            # Check if this line is a category header
            cat_match = re.search(r'#{2,3}\s+([^#\n]+)', line)
            if cat_match:
                current_category = cat_match.group(1).strip()
                continue
                
            # Check if this line contains an API entry
            api_match = re.search(pattern, line)
            if api_match:
                name, url, description, auth, https, cors = api_match.groups()
                
                # Clean up the values
                name = name.strip()
                url = url.strip()
                description = description.strip()
                auth = auth.strip()
                https = https.strip().lower() == 'yes'
                cors = cors.strip()
                
                # Map the category name to our internal categories
                mapped_category = map_category_name(current_category)
                
                apis.append({
                    'name': name,
                    'description': description,
                    'url': url,
                    'category': mapped_category,
                    'auth': auth if auth != 'No' else 'none',
                    'https': https,
                    'cors': cors.lower(),
                    'popularity': 85,  # Default popularity for public-apis
                    'status': 'active',
                    'last_checked': datetime.datetime.now().isoformat()
                })
                
    except Exception as e:
        print(f"Error scraping public-apis GitHub: {e}")
        
    return apis

def scrape_apilist_fun() -> List[Dict[str, Any]]:
    """Scrape APIs from apilist.fun website."""
    apis = []
    try:
        headers = {'User-Agent': get_random_user_agent()}
        url = 'https://apilist.fun/'
        
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            print(f"Failed to fetch apilist.fun: {response.status_code}")
            return apis
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find API entries
        api_entries = soup.select('.api-entry')
        
        for entry in api_entries:
            try:
                name_elem = entry.select_one('.api-name')
                desc_elem = entry.select_one('.api-description')
                link_elem = entry.select_one('a.api-link')
                category_elem = entry.select_one('.api-category')
                
                if name_elem and link_elem:
                    name = name_elem.text.strip()
                    description = desc_elem.text.strip() if desc_elem else ""
                    url = link_elem['href'] if link_elem.get('href') else ""
                    category = category_elem.text.strip() if category_elem else "Development"
                    
                    # Only add if we have at least a name and URL
                    if name and url:
                        # Determine auth method based on description or other factors
                        auth = determine_auth_method(description, url)
                        
                        apis.append({
                            'name': name,
                            'description': description,
                            'url': url,
                            'category': map_category_name(category),
                            'auth': auth,
                            'https': True,  # Assume HTTPS by default
                            'cors': 'unknown',
                            'popularity': 80,  # Default popularity
                            'status': 'active',
                            'last_checked': datetime.datetime.now().isoformat()
                        })
            except Exception as e:
                print(f"Error parsing API entry: {e}")
                
    except Exception as e:
        print(f"Error scraping apilist.fun: {e}")
        
    return apis

def scrape_rapidapi_collections() -> List[Dict[str, Any]]:
    """Scrape APIs from RapidAPI collections."""
    apis = []
    collections = [
        'most-popular', 'trending', 'featured', 'free', 'weather', 'finance',
        'social', 'music', 'news', 'sports', 'health', 'food', 'travel'
    ]
    
    for collection in collections:
        try:
            headers = {'User-Agent': get_random_user_agent()}
            url = f'https://rapidapi.com/collections/{collection}'
            
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            if response.status_code != 200:
                print(f"Failed to fetch RapidAPI collection {collection}: {response.status_code}")
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find API cards
            api_cards = soup.select('.api-card')
            
            for card in api_cards:
                try:
                    name_elem = card.select_one('.api-name, .api-title')
                    desc_elem = card.select_one('.api-description, .api-desc')
                    link_elem = card.select_one('a.api-link, a.api-card-link')
                    
                    if name_elem and link_elem:
                        name = name_elem.text.strip()
                        description = desc_elem.text.strip() if desc_elem else ""
                        url = 'https://rapidapi.com' + link_elem['href'] if link_elem.get('href') else ""
                        
                        # Determine category based on collection or description
                        category = map_category_name(collection if collection != 'most-popular' and collection != 'trending' and collection != 'featured' and collection != 'free' else description)
                        
                        # Only add if we have at least a name and URL
                        if name and url:
                            apis.append({
                                'name': name,
                                'description': description,
                                'url': url,
                                'category': category,
                                'auth': 'apiKey',  # Most RapidAPI APIs use API keys
                                'https': True,
                                'cors': 'yes',  # RapidAPI generally supports CORS
                                'popularity': 85,  # Default popularity for RapidAPI
                                'status': 'active',
                                'last_checked': datetime.datetime.now().isoformat()
                            })
                except Exception as e:
                    print(f"Error parsing API card: {e}")
                    
        except Exception as e:
            print(f"Error scraping RapidAPI collection {collection}: {e}")
            
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
        
        # Find API entries
        api_entries = soup.select('.api-entry, .api-item')
        
        for entry in api_entries:
            try:
                name_elem = entry.select_one('.api-name, .api-title, h3')
                desc_elem = entry.select_one('.api-description, .api-desc, p')
                link_elem = entry.select_one('a')
                
                if name_elem and link_elem:
                    name = name_elem.text.strip()
                    description = desc_elem.text.strip() if desc_elem else ""
                    url = link_elem['href'] if link_elem.get('href') else ""
                    if not url.startswith('http'):
                        url = 'https://any-api.com' + url
                    
                    # Determine category based on description
                    category = determine_category_from_description(description)
                    
                    # Only add if we have at least a name and URL
                    if name and url:
                        apis.append({
                            'name': name,
                            'description': description,
                            'url': url,
                            'category': category,
                            'auth': determine_auth_method(description, url),
                            'https': True,  # Assume HTTPS by default
                            'cors': 'unknown',
                            'popularity': 75,  # Default popularity
                            'status': 'active',
                            'last_checked': datetime.datetime.now().isoformat()
                        })
            except Exception as e:
                print(f"Error parsing API entry: {e}")
                
    except Exception as e:
        print(f"Error scraping any-api.com: {e}")
        
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
                # Get the latest version
                latest_version = api_versions['preferred']
                api_info = api_versions['versions'][latest_version]
                
                name = api_info['info']['title']
                description = api_info['info'].get('description', '').split('\n')[0]  # Get first line of description
                url = api_info['info'].get('contact', {}).get('url', '') or api_info['swaggerUrl']
                
                # Determine category based on tags or description
                tags = api_info['info'].get('tags', [])
                category = map_category_name(tags[0] if tags else description)
                
                # Determine auth method
                auth = 'unknown'
                if 'securityDefinitions' in api_info:
                    if 'oauth' in str(api_info['securityDefinitions']).lower():
                        auth = 'OAuth'
                    elif 'apikey' in str(api_info['securityDefinitions']).lower():
                        auth = 'apiKey'
                    elif 'basic' in str(api_info['securityDefinitions']).lower():
                        auth = 'Basic'
                    else:
                        auth = 'Yes'
                
                apis.append({
                    'name': name,
                    'description': description,
                    'url': url,
                    'category': category,
                    'auth': auth,
                    'https': True,  # APIs.guru typically lists HTTPS APIs
                    'cors': 'unknown',
                    'popularity': 80,  # Default popularity
                    'status': 'active',
                    'last_checked': datetime.datetime.now().isoformat()
                })
            except Exception as e:
                print(f"Error parsing API {api_name}: {e}")
                
    except Exception as e:
        print(f"Error scraping APIs.guru: {e}")
        
    return apis

def determine_auth_method(description: str, url: str) -> str:
    """Determine the authentication method based on description and URL."""
    description_lower = description.lower()
    url_lower = url.lower()
    
    if 'no auth' in description_lower or 'no authentication' in description_lower:
        return 'none'
    elif 'oauth' in description_lower or 'oauth' in url_lower:
        return 'OAuth'
    elif 'api key' in description_lower or 'apikey' in description_lower or 'api-key' in url_lower:
        return 'apiKey'
    elif 'basic auth' in description_lower or 'basic authentication' in description_lower:
        return 'Basic'
    elif 'jwt' in description_lower or 'bearer' in description_lower:
        return 'Bearer'
    else:
        return 'unknown'

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
    updated_categories = set()
    
    for new_api in new_apis:
        category_name = new_api.get('category', 'Development')
        
        # Find the appropriate category
        category_found = False
        for category in updated_data['categories']:
            if category['name'] == category_name:
                category_found = True
                # Check if API already exists
                if not is_api_duplicate(new_api, category['apis']):
                    # Add required fields if missing
                    if 'status' not in new_api:
                        new_api['status'] = 'active'
                    if 'last_checked' not in new_api:
                        new_api['last_checked'] = datetime.datetime.now().isoformat()
                    
                    category['apis'].append(new_api)
                    added_count += 1
                    updated_categories.add(category_name)
                    print(f"Added new API: {new_api['name']} to category {category_name}")
                break
        
        # If category not found, create it
        if not category_found:
            new_category = {
                'name': category_name,
                'description': f"APIs for {category_name.lower()} related services",
                'apis': [new_api]
            }
            updated_data['categories'].append(new_category)
            added_count += 1
            updated_categories.add(category_name)
            print(f"Created new category {category_name} and added API: {new_api['name']}")
    
    # Update metadata
    total_apis = sum(len(category['apis']) for category in updated_data['categories'])
    updated_data['metadata']['total_apis'] = total_apis
    updated_data['metadata']['last_updated'] = datetime.datetime.now().isoformat()
    
    # Update README.md with the new APIs
    if added_count > 0:
        update_readme_with_apis(updated_data, list(updated_categories))
    
    print(f"Added {added_count} new APIs")
    return updated_data

def update_readme_with_apis(data: Dict[str, Any], updated_categories: List[str]) -> None:
    """Update the README.md file with APIs from the specified categories."""
    readme_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as file:
            readme_content = file.read()
        
        # Update each category section in the README
        for category_name in updated_categories:
            # Find the category in the data
            category = None
            for cat in data['categories']:
                if cat['name'] == category_name:
                    category = cat
                    break
            
            if not category or not category['apis']:
                continue
            
            # Create the API table for this category
            api_table = "| API | Description | Auth | HTTPS | CORS |\n"
            api_table += "| --- | --- | --- | --- | --- |\n"
            
            # Add each API to the table
            for api in category['apis']:
                name = api.get('name', '')
                url = api.get('url', '')
                description = api.get('description', '')
                auth = api.get('auth', 'unknown')
                https = 'Yes' if api.get('https', False) else 'No'
                cors = api.get('cors', 'unknown')
                
                # Format the API row
                api_table += f"| [{name}]({url}) | {description} | {auth} | {https} | {cors} |\n"
            
            # Find the category section in the README
            category_pattern = f"### {category_name}\n.*?\n\n"
            category_match = re.search(category_pattern, readme_content, re.DOTALL)
            
            if category_match:
                # Replace the existing category section
                new_category_section = f"### {category_name}\n{category.get('description', f'APIs for {category_name.lower()} related services.')}\n\n{api_table}\n"
                readme_content = readme_content.replace(category_match.group(0), new_category_section)
            else:
                # Find where to insert the new category section
                # Look for the next category section
                next_category_pattern = "### [A-Za-z\s&]+\n"
                next_category_matches = list(re.finditer(next_category_pattern, readme_content))
                
                # Find the position to insert based on alphabetical order
                insert_position = None
                for i, match in enumerate(next_category_matches):
                    next_category = match.group(0).strip()[4:].strip()
                    if category_name < next_category:
                        insert_position = match.start()
                        break
                
                if insert_position is None and next_category_matches:
                    # Insert at the end of the categories section
                    insert_position = next_category_matches[-1].end()
                
                if insert_position is not None:
                    # Insert the new category section
                    new_category_section = f"### {category_name}\n{category.get('description', f'APIs for {category_name.lower()} related services.')}\n\n{api_table}\n\n"
                    readme_content = readme_content[:insert_position] + new_category_section + readme_content[insert_position:]
        
        # Update the last updated timestamp
        today = datetime.datetime.now().strftime('%B %d, %Y')
        readme_content = re.sub(r'<p align="center">Last updated: .*?</p>', f'<p align="center">Last updated: {today}</p>', readme_content)
        
        # Write the updated README
        with open(readme_path, 'w', encoding='utf-8') as file:
            file.write(readme_content)
        
        print(f"Updated README.md with APIs from {len(updated_categories)} categories")
        
    except Exception as e:
        print(f"Error updating README.md: {e}")

def main():
    """Main function to discover APIs from multiple sources."""
    print("Starting enhanced API discovery process...")
    
    # Load current API data
    data = load_api_data()
    
    # Discover new APIs from various sources
    new_apis = []
    
    # Public APIs GitHub Repository - This is the most reliable source
    print("Scraping public-apis GitHub repository...")
    public_apis = scrape_public_apis_github()
    new_apis.extend(public_apis)
    print(f"Found {len(public_apis)} APIs from public-apis GitHub repository")
    
    # If we don't have enough APIs yet, try other sources
    if len(public_apis) < 50:
        # APIList.fun
        print("Scraping apilist.fun...")
        apilist_apis = scrape_apilist_fun()
        new_apis.extend(apilist_apis)
        print(f"Found {len(apilist_apis)} APIs from apilist.fun")
        
        # RapidAPI Collections
        print("Scraping RapidAPI collections...")
        rapidapi_apis = scrape_rapidapi_collections()
        new_apis.extend(rapidapi_apis)
        print(f"Found {len(rapidapi_apis)} APIs from RapidAPI collections")
        
        # Any-API
        print("Scraping any-api.com...")
        any_api_apis = scrape_any_api()
        new_apis.extend(any_api_apis)
        print(f"Found {len(any_api_apis)} APIs from any-api.com")
        
        # APIs.guru
        print("Scraping APIs.guru...")
        apis_guru_apis = scrape_apis_guru()
        new_apis.extend(apis_guru_apis)
        print(f"Found {len(apis_guru_apis)} APIs from APIs.guru")
    
    # Add sample APIs if we don't have any APIs yet
    if len(new_apis) == 0:
        print("No APIs found from scrapers, adding sample APIs...")
        sample_apis = [
            {
                'name': 'GitHub',
                'description': 'Make use of GitHub\'s APIs to fetch repository information, user data, and more',
                'url': 'https://docs.github.com/en/rest',
                'category': 'Development',
                'auth': 'OAuth',
                'https': True,
                'cors': 'yes',
                'popularity': 99,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            },
            {
                'name': 'OpenWeatherMap',
                'description': 'Weather forecasts, nowcasts and history in a fast and elegant way',
                'url': 'https://openweathermap.org/api',
                'category': 'Weather',
                'auth': 'apiKey',
                'https': True,
                'cors': 'yes',
                'popularity': 98,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            },
            {
                'name': 'Unsplash',
                'description': 'Free high-resolution photos API',
                'url': 'https://unsplash.com/developers',
                'category': 'Photography',
                'auth': 'OAuth',
                'https': True,
                'cors': 'yes',
                'popularity': 94,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            }
        ]
        new_apis.extend(sample_apis)
    
    # Add new APIs to the data
    if new_apis:
        updated_data = add_new_apis(data, new_apis)
        
        # Save updated data
        save_api_data(updated_data)
        print(f"Added {len(new_apis)} APIs to the database")
    else:
        print("No new APIs discovered")
    
    print("Enhanced API discovery process completed.")

if __name__ == "__main__":
    main()
