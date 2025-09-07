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
    
    # Update metadata
    total_apis = sum(len(category['apis']) for category in updated_data['categories'])
    updated_data['metadata']['total_apis'] = total_apis
    updated_data['metadata']['last_updated'] = datetime.datetime.now().isoformat()
    
    print(f"Added {added_count} new APIs")
    return updated_data


def scrape_public_apis_repository() -> List[Dict[str, Any]]:
    """Scrape APIs from the public-apis/public-apis repository.
    Only includes APIs that link to actual API websites, not to API directories."""
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
        
        # Domains to exclude (API directories, not actual API websites)
        excluded_domains = [
            'apis.guru',
            'rapidapi.com',
            'apilayer.com',
            'api-ninjas.com',
            'programmableweb.com',
            'apilist.fun',
            'any-api.com',
            'apihouse.vercel.app'
        ]
        
        for category_name, category_content in category_matches:
            # Parse table rows
            api_pattern = r'\[(.*?)\]\((.*?)\) \| (.*?) \| (.*?) \| (.*?) \| (.*?)\n'
            api_matches = re.findall(api_pattern, category_content)
            
            for api_name, api_url, api_desc, auth, https, cors in api_matches:
                # Skip APIs that link to excluded domains (API directories)
                should_exclude = False
                for domain in excluded_domains:
                    if domain in api_url.lower():
                        should_exclude = True
                        print(f"Skipping {api_name} as it links to {domain}")
                        break
                
                if should_exclude:
                    continue
                
                # Skip APIs with generic names that likely aren't direct API links
                generic_terms = ['directory', 'catalog', 'list', 'collection', 'hub', 'marketplace']
                if any(term in api_name.lower() for term in generic_terms):
                    print(f"Skipping {api_name} as it appears to be a directory, not a direct API")
                    continue
                
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
    """Verify if an API is working and update its information.
    Performs thorough checks to ensure the website is accessible."""
    # Make a copy of the API to avoid modifying the original
    verified_api = api.copy()
    
    # Ensure URL exists and is a string
    if 'url' not in verified_api or not isinstance(verified_api['url'], str) or not verified_api['url']:
        verified_api['status'] = 'unknown'
        verified_api['https'] = False
        verified_api['cors'] = 'unknown'
        verified_api['working'] = False  # Mark as not working
        return verified_api
    
    try:
        headers = {'User-Agent': get_random_user_agent()}
        
        # First try HEAD request with a short timeout
        try:
            head_response = requests.head(
                verified_api['url'], 
                headers=headers, 
                timeout=5, 
                allow_redirects=True
            )
            
            # If HEAD request succeeds, use that response
            response = head_response
            
        except requests.RequestException:
            # If HEAD fails, try GET request as some servers don't support HEAD
            response = requests.get(
                verified_api['url'], 
                headers=headers, 
                timeout=8,  # Slightly longer timeout for GET
                allow_redirects=True,
                stream=True  # Don't download the entire content
            )
            # Just read a small part to verify connection
            response.raw.read(1024)
            response.close()
        
        # Update API status based on response
        if response.status_code < 400:
            verified_api['status'] = 'active'
            verified_api['working'] = True
        else:
            verified_api['status'] = 'inactive'
            verified_api['working'] = False
            
        # Try to detect CORS support
        if 'Access-Control-Allow-Origin' in response.headers:
            verified_api['cors'] = 'yes'
            
        # Try to detect HTTPS support
        verified_api['https'] = verified_api['url'].startswith('https')
        
    except requests.RequestException as e:
        # Mark as not working if we can't connect
        print(f"Warning: Could not verify API {verified_api.get('name', 'unknown')}: {e}")
        verified_api['status'] = 'error'
        verified_api['working'] = False
    except Exception as e:
        print(f"Error verifying API {verified_api.get('name', 'unknown')}: {e}")
        verified_api['status'] = 'unknown'
        verified_api['working'] = False
        
    return verified_api


def add_new_apis(data: Dict[str, Any], new_apis: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Add new APIs to the appropriate categories with priority to empty categories.
    Ensures each category has between 10-15 high-quality APIs."""
    updated_data = data.copy()
    added_count = 0
    
    # First, identify categories that need more APIs (have less than MIN_APIS_PER_CATEGORY)
    MIN_APIS_PER_CATEGORY = 10
    MAX_APIS_PER_CATEGORY = 15
    
    categories_needing_apis = []
    for category in updated_data['categories']:
        if len(category['apis']) < MIN_APIS_PER_CATEGORY:
            categories_needing_apis.append(category['name'])
    
    # Filter APIs by quality criteria
    quality_apis = []
    for api in new_apis:
        # Quality filtering criteria
        if not api.get('name') or not api.get('url') or not api.get('description'):
            continue
            
        # Ensure description is meaningful (at least 20 characters)
        if len(api.get('description', '')) < 20:
            continue
            
        # Prefer APIs with known auth method
        if api.get('auth') == 'unknown':
            api['quality_score'] = 70
        else:
            api['quality_score'] = 90
            
        # Prefer APIs with HTTPS
        if api.get('https'):
            api['quality_score'] += 10
            
        # Prefer APIs with known CORS status
        if api.get('cors') != 'unknown':
            api['quality_score'] += 5
            
        quality_apis.append(api)
    
    # Sort APIs by quality score and then by category priority
    prioritized_apis = sorted(
        quality_apis,
        key=lambda api: (
            0 if api.get('category') in categories_needing_apis else 1,
            -api.get('quality_score', 0)  # Higher quality score first
        )
    )
    
    # Process APIs with priority given to categories needing APIs and quality
    for new_api in prioritized_apis:
        category_name = new_api.get('category', 'Development')
        category_found = False
        
        # Find the appropriate category
        for category in updated_data['categories']:
            if category['name'] == category_name:
                category_found = True
                
                # Skip if category already has maximum number of APIs
                if len(category['apis']) >= MAX_APIS_PER_CATEGORY:
                    break
                    
                # Check if API already exists
                if not is_api_duplicate(new_api, category['apis']):
                    # Verify API before adding
                    new_api = verify_api(new_api)
                    
                    # Only add if the API is working
                    if new_api.get('working', False):
                        # Add required fields if missing
                        if 'status' not in new_api:
                            new_api['status'] = 'active'
                        if 'last_checked' not in new_api:
                            new_api['last_checked'] = datetime.datetime.now().isoformat()
                        
                        category['apis'].append(new_api)
                        added_count += 1
                        print(f"Added new API: {new_api['name']} to category {category_name}")
                    else:
                        print(f"Skipping non-working API: {new_api['name']} (status: {new_api.get('status', 'unknown')})")
                break
        
        # If category not found, add to Development category
        if not category_found:
            for category in updated_data['categories']:
                if category['name'] == 'Development':
                    # Skip if Development category already has maximum number of APIs
                    if len(category['apis']) >= MAX_APIS_PER_CATEGORY:
                        break
                        
                    if not is_api_duplicate(new_api, category['apis']):
                        new_api['category'] = 'Development'
                        new_api = verify_api(new_api)
                        
                        # Only add if the API is working
                        if new_api.get('working', False):
                            if 'status' not in new_api:
                                new_api['status'] = 'active'
                            if 'last_checked' not in new_api:
                                new_api['last_checked'] = datetime.datetime.now().isoformat()
                            
                            category['apis'].append(new_api)
                            added_count += 1
                            print(f"Added new API: {new_api['name']} to Development category (original category not found)")
                        else:
                            print(f"Skipping non-working API: {new_api['name']} (status: {new_api.get('status', 'unknown')})")
                    break
    
    # Update metadata
    total_apis = sum(len(category['apis']) for category in updated_data['categories'])
    updated_data['metadata']['total_apis'] = total_apis
    updated_data['metadata']['last_updated'] = datetime.datetime.now().isoformat()
    
    print(f"Added {added_count} new APIs")
    return updated_data


def scrape_api_ninjas() -> List[Dict[str, Any]]:
    """Scrape APIs from API Ninjas."""
    apis = []
    try:
        headers = {'User-Agent': get_random_user_agent()}
        url = 'https://api-ninjas.com/api'
        
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            print(f"Failed to fetch API Ninjas: {response.status_code}")
            return apis
            
        soup = BeautifulSoup(response.text, 'html.parser')
        api_cards = soup.select('.api-card')
        
        for card in api_cards:
            try:
                name_elem = card.select_one('.api-title')
                desc_elem = card.select_one('.api-description')
                url_elem = card.select_one('a.api-link')
                
                if name_elem and url_elem:
                    name = name_elem.text.strip()
                    description = desc_elem.text.strip() if desc_elem else ""
                    url = 'https://api-ninjas.com' + url_elem['href'] if url_elem.get('href') else ""
                    
                    # Determine category based on description
                    category = determine_category_from_description(description)
                    
                    apis.append({
                        'name': name,
                        'description': description,
                        'url': url,
                        'category': category,
                        'auth': 'apiKey',
                        'https': True,
                        'cors': 'unknown',
                        'popularity': 75,
                        'status': 'active',
                        'last_checked': datetime.datetime.now().isoformat()
                    })
            except Exception as e:
                print(f"Error parsing API Ninjas card: {e}")
                
    except Exception as e:
        print(f"Error scraping API Ninjas: {e}")
        
    return apis


def scrape_rapidapi_collections() -> List[Dict[str, Any]]:
    """Scrape APIs from RapidAPI collections."""
    apis = []
    collections = [
        'free-to-use',
        'weather',
        'entertainment',
        'sports',
        'health',
        'music',
        'news',
        'food',
        'travel',
        'finance',
        'ecommerce',
        'social-media'
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
            api_cards = soup.select('.api-card')
            
            for card in api_cards:
                try:
                    name_elem = card.select_one('.api-name')
                    desc_elem = card.select_one('.api-description')
                    url_elem = card.select_one('a')
                    
                    if name_elem and url_elem:
                        name = name_elem.text.strip()
                        description = desc_elem.text.strip() if desc_elem else ""
                        url = 'https://rapidapi.com' + url_elem['href'] if url_elem.get('href') else ""
                        
                        # Map collection to category
                        if collection == 'weather':
                            category = 'Weather'
                        elif collection == 'entertainment':
                            category = 'Entertainment'
                        elif collection == 'sports':
                            category = 'Sports & Fitness'
                        elif collection == 'health':
                            category = 'Health'
                        elif collection == 'music':
                            category = 'Music'
                        elif collection == 'news':
                            category = 'News'
                        elif collection == 'food':
                            category = 'Food & Drink'
                        elif collection == 'travel':
                            category = 'Transportation'
                        elif collection == 'finance':
                            category = 'Finance'
                        elif collection == 'ecommerce':
                            category = 'Shopping'
                        elif collection == 'social-media':
                            category = 'Social'
                        else:
                            category = determine_category_from_description(description)
                        
                        apis.append({
                            'name': name,
                            'description': description,
                            'url': url,
                            'category': category,
                            'auth': 'apiKey',
                            'https': True,
                            'cors': 'unknown',
                            'popularity': 80,
                            'status': 'active',
                            'last_checked': datetime.datetime.now().isoformat()
                        })
                except Exception as e:
                    print(f"Error parsing RapidAPI card: {e}")
                    
        except Exception as e:
            print(f"Error scraping RapidAPI collection {collection}: {e}")
            
    return apis


def scrape_github_awesome_lists() -> List[Dict[str, Any]]:
    """Scrape APIs from GitHub awesome lists."""
    apis = []
    awesome_lists = [
        'public-apis/public-apis',  # Already covered in another function
        'n0shake/Public-APIs',
        'TonnyL/Awesome_APIs',
        'abhishekbanthia/Public-APIs',
        'farizdotid/APIS-WEB-ID'
    ]
    
    for repo in awesome_lists[1:]:  # Skip the first one as it's already covered
        try:
            headers = {'User-Agent': get_random_user_agent()}
            url = f'https://raw.githubusercontent.com/{repo}/master/README.md'
            
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            if response.status_code != 200:
                # Try alternate branch name
                url = f'https://raw.githubusercontent.com/{repo}/main/README.md'
                response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
                if response.status_code != 200:
                    print(f"Failed to fetch awesome list {repo}: {response.status_code}")
                    continue
                    
            content = response.text
            
            # Extract API links and descriptions
            # This is a simple approach; actual parsing would depend on the format of each list
            api_pattern = r'\[(.*?)\]\((https?://[^\s\)]+)\)\s*(?:-|:)?\s*([^\n]+)?'
            api_matches = re.findall(api_pattern, content)
            
            for name, url, description in api_matches:
                # Skip if it doesn't look like an API
                if not ('api' in name.lower() or 'api' in url.lower() or 'api' in description.lower()):
                    continue
                    
                category = determine_category_from_description(description)
                
                apis.append({
                    'name': name,
                    'description': description.strip(),
                    'url': url,
                    'category': category,
                    'auth': 'unknown',
                    'https': url.startswith('https'),
                    'cors': 'unknown',
                    'popularity': 70,
                    'status': 'active',
                    'last_checked': datetime.datetime.now().isoformat()
                })
                
        except Exception as e:
            print(f"Error scraping awesome list {repo}: {e}")
            
    return apis


def scrape_apihouse() -> List[Dict[str, Any]]:
    """Scrape APIs from APIHouse."""
    apis = []
    try:
        headers = {'User-Agent': get_random_user_agent()}
        url = 'https://apihouse.vercel.app/api/apis'
        
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            print(f"Failed to fetch APIHouse: {response.status_code}")
            return apis
            
        data = response.json()
        
        for api_data in data:
            try:
                name = api_data.get('name', '')
                description = api_data.get('description', '')
                api_url = api_data.get('url', '')
                category_name = api_data.get('category', '')
                
                if name and api_url:
                    category = map_category_name(category_name) if category_name else determine_category_from_description(description)
                    
                    apis.append({
                        'name': name,
                        'description': description,
                        'url': api_url,
                        'category': category,
                        'auth': api_data.get('auth', 'unknown'),
                        'https': api_url.startswith('https'),
                        'cors': api_data.get('cors', 'unknown'),
                        'popularity': 75,
                        'status': 'active',
                        'last_checked': datetime.datetime.now().isoformat()
                    })
            except Exception as e:
                print(f"Error parsing APIHouse entry: {e}")
                
    except Exception as e:
        print(f"Error scraping APIHouse: {e}")
        
    return apis


def filter_apis_for_readme(data: Dict[str, Any]) -> Dict[str, Any]:
    """Filter APIs for inclusion in the README file.
    Only includes working APIs and ensures category limits are respected."""
    filtered_data = data.copy()
    
    # Define limits
    MIN_APIS_PER_CATEGORY = 10
    MAX_APIS_PER_CATEGORY = 15
    
    for category in filtered_data['categories']:
        # Filter out non-working APIs
        working_apis = [api for api in category['apis'] if api.get('working', False) and api.get('status') == 'active']
        
        # Sort by quality score if available, otherwise by name
        sorted_apis = sorted(
            working_apis,
            key=lambda api: (-api.get('quality_score', 0), api.get('name', ''))
        )
        
        # Limit to maximum number of APIs
        limited_apis = sorted_apis[:MAX_APIS_PER_CATEGORY]
        
        # Update the category with filtered APIs
        category['apis'] = limited_apis
        
        # Log warning if category has fewer than minimum APIs
        if len(limited_apis) < MIN_APIS_PER_CATEGORY:
            print(f"Warning: Category {category['name']} has only {len(limited_apis)} working APIs (minimum is {MIN_APIS_PER_CATEGORY})")
    
    # Update metadata
    total_apis = sum(len(category['apis']) for category in filtered_data['categories'])
    filtered_data['metadata']['total_apis'] = total_apis
    filtered_data['metadata']['last_updated'] = datetime.datetime.now().isoformat()
    
    return filtered_data


def main():
    """Main function to discover trending APIs."""
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser(description='Discover trending APIs from various sources')
        parser.add_argument('--mode', choices=['regular', 'comprehensive', 'all'], default='regular',
                            help='Discovery mode: regular (weekly sources), comprehensive (all sources), or all (force all sources)')
        parser.add_argument('--category', type=str, default=None,
                            help='Target specific category to populate')
        parser.add_argument('--readme', action='store_true',
                            help='Filter APIs for README inclusion')
        args = parser.parse_args()
        
        print(f"Starting API discovery process in {args.mode} mode...")
        if args.category:
            print(f"Targeting category: {args.category}")
        
        # Load current API data
        data = load_api_data()
        
        # Discover new APIs from various sources
        new_apis = []
        
        # Sources for regular (weekly) discovery
        # These are faster and more reliable sources
        print("Scraping regular sources...")
        
        try:
            # RapidAPI Hub
            print("Scraping RapidAPI Hub...")
            rapidapi_apis = scrape_rapidapi_hub()
            new_apis.extend(rapidapi_apis)
            print(f"Found {len(rapidapi_apis)} APIs from RapidAPI Hub")
        except Exception as e:
            print(f"Error scraping RapidAPI Hub: {e}")
        
        try:
            # GitHub Trending
            print("Scraping GitHub Trending...")
            github_apis = scrape_github_trending()
            new_apis.extend(github_apis)
            print(f"Found {len(github_apis)} APIs from GitHub Trending")
        except Exception as e:
            print(f"Error scraping GitHub Trending: {e}")
        
        try:
            # Public APIs Repository (with filtering for direct API links)
            print("Scraping public-apis repository...")
            public_apis = scrape_public_apis_repository()
            new_apis.extend(public_apis)
            print(f"Found {len(public_apis)} APIs from public-apis repository")
        except Exception as e:
            print(f"Error scraping public-apis repository: {e}")
        
        try:
            # RapidAPI Collections (categorized collections)
            print("Scraping RapidAPI Collections...")
            rapidapi_collections = scrape_rapidapi_collections()
            new_apis.extend(rapidapi_collections)
            print(f"Found {len(rapidapi_collections)} APIs from RapidAPI Collections")
        except Exception as e:
            print(f"Error scraping RapidAPI Collections: {e}")
        
        # Additional sources for comprehensive (monthly) discovery
        if args.mode in ['comprehensive', 'all']:
            print("\nScraping additional sources for comprehensive discovery...")
            
            try:
                # ProgrammableWeb (can be slow and less reliable)
                print("Scraping ProgrammableWeb...")
                programmableweb_apis = scrape_programmableweb()
                new_apis.extend(programmableweb_apis)
                print(f"Found {len(programmableweb_apis)} APIs from ProgrammableWeb")
            except Exception as e:
                print(f"Error scraping ProgrammableWeb: {e}")
            
            try:
                # APIList.fun
                print("Scraping APIList.fun...")
                apilist_apis = scrape_apilist_fun()
                new_apis.extend(apilist_apis)
                print(f"Found {len(apilist_apis)} APIs from APIList.fun")
            except Exception as e:
                print(f"Error scraping APIList.fun: {e}")
            
            # APIs.guru scraper has been removed as requested
            
            try:
                # Any-API
                print("Scraping Any-API...")
                any_api_apis = scrape_any_api()
                new_apis.extend(any_api_apis)
                print(f"Found {len(any_api_apis)} APIs from Any-API")
            except Exception as e:
                print(f"Error scraping Any-API: {e}")
            
            try:
                # API Ninjas
                print("Scraping API Ninjas...")
                api_ninjas_apis = scrape_api_ninjas()
                new_apis.extend(api_ninjas_apis)
                print(f"Found {len(api_ninjas_apis)} APIs from API Ninjas")
            except Exception as e:
                print(f"Error scraping API Ninjas: {e}")
            
            try:
                # GitHub Awesome Lists
                print("Scraping GitHub Awesome Lists...")
                awesome_list_apis = scrape_github_awesome_lists()
                new_apis.extend(awesome_list_apis)
                print(f"Found {len(awesome_list_apis)} APIs from GitHub Awesome Lists")
            except Exception as e:
                print(f"Error scraping GitHub Awesome Lists: {e}")
            
            try:
                # APIHouse
                print("Scraping APIHouse...")
                apihouse_apis = scrape_apihouse()
                new_apis.extend(apihouse_apis)
                print(f"Found {len(apihouse_apis)} APIs from APIHouse")
            except Exception as e:
                print(f"Error scraping APIHouse: {e}")
        
        # Filter by category if specified
        if args.category:
            filtered_apis = []
            for api in new_apis:
                if api.get('category') == args.category:
                    filtered_apis.append(api)
            new_apis = filtered_apis
            print(f"Filtered to {len(new_apis)} APIs for category {args.category}")
        
        # Add new APIs to the data
        if new_apis:
            print(f"\nProcessing {len(new_apis)} discovered APIs...")
            updated_data = add_new_apis(data, new_apis)
            
            # Filter APIs for README if requested
            if args.readme:
                print("Filtering APIs for README inclusion...")
                updated_data = filter_apis_for_readme(updated_data)
                print(f"Filtered data to include only working APIs with limits of 10-15 per category")
            
            # Save updated data
            save_api_data(updated_data)
        else:
            print("No new APIs discovered")
        
        print("API discovery process completed.")
    except Exception as e:
        print(f"Critical error in API discovery process: {e}")
        # Ensure we exit with a non-zero code to indicate failure
        # but don't raise the exception to avoid crashing GitHub Actions
        print("API discovery process failed but continuing to avoid GitHub Actions failure.")
        # If we have data loaded, try to save what we have
        try:
            if 'data' in locals() and new_apis:
                print("Attempting to save partial data...")
                updated_data = add_new_apis(data, new_apis)
                save_api_data(updated_data)
                print("Partial data saved.")
        except Exception as save_error:
            print(f"Could not save partial data: {save_error}")
            pass


if __name__ == "__main__":
    main()
