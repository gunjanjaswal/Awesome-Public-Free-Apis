#!/usr/bin/env python3
"""
Script to discover trending APIs and update the README.md file.
"""

import datetime
import json
import os
import random
import re
import time
from typing import Dict, List, Any, Tuple

import requests
from bs4 import BeautifulSoup

# Constants
REQUEST_TIMEOUT = 10  # seconds
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
]


def get_random_user_agent() -> str:
    """Get a random user agent to avoid being blocked."""
    return random.choice(USER_AGENTS)


def load_data() -> Dict[str, Any]:
    """Load the current API data from README.md."""
    readme_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract categories and APIs
    categories = []
    current_category = None
    
    for line in content.split('\n'):
        if line.startswith('## ') and not line.startswith('## Table of Contents'):
            # New category
            if current_category:
                categories.append(current_category)
            
            category_name = line[3:].strip()
            description = ''
            apis = []
            current_category = {
                'name': category_name,
                'description': description,
                'apis': apis
            }
        elif current_category and line.startswith('APIs related to'):
            # Category description
            current_category['description'] = line.strip()
        elif current_category and line.startswith('|') and not line.startswith('| API') and not line.startswith('| ---'):
            # API entry
            parts = line.split('|')
            if len(parts) >= 5:
                name = parts[1].strip()
                description = parts[2].strip()
                auth = parts[3].strip()
                https = parts[4].strip() == 'Yes'
                cors = parts[5].strip().lower() if len(parts) > 5 else 'unknown'
                
                # Extract URL if present
                url_match = re.search(r'\[(.*?)\]\((.*?)\)', name)
                if url_match:
                    name = url_match.group(1)
                    url = url_match.group(2)
                else:
                    url = ''
                
                api = {
                    'name': name,
                    'description': description,
                    'url': url,
                    'auth': auth,
                    'https': https,
                    'cors': cors,
                    'status': 'active',
                    'last_checked': datetime.datetime.now().isoformat()
                }
                
                current_category['apis'].append(api)
    
    # Add the last category
    if current_category:
        categories.append(current_category)
    
    # Create the data structure
    data = {
        'metadata': {
            'total_apis': sum(len(category['apis']) for category in categories),
            'last_updated': datetime.datetime.now().isoformat()
        },
        'categories': categories
    }
    
    return data


def save_data(data: Dict[str, Any]) -> None:
    """Save the API data to README.md."""
    readme_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')
    
    # Generate the README content
    content = """# Public APIs

A collective list of free APIs for use in software and web development.

## Table of Contents

"""
    
    # Add categories to table of contents
    for category in data['categories']:
        anchor = category['name'].lower().replace(' ', '-').replace('&', '').replace('/', '')
        content += f"- [{category['name']}](#{anchor})\n"
    
    content += "\n"
    
    # Add each category and its APIs
    for category in data['categories']:
        content += f"## {category['name']}\n"
        content += f"{category['description']}\n\n"
        content += "| API | Description | Auth | HTTPS | CORS |\n"
        content += "| --- | --- | --- | --- | --- |\n"
        
        for api in category['apis']:
            name = api['name']
            if api['url']:
                name = f"[{name}]({api['url']})"
            
            https = "Yes" if api['https'] else "No"
            
            content += f"| {name} | {api['description']} | {api['auth']} | {https} | {api['cors']} |\n"
        
        content += "\n"
    
    # Add footer
    content += """## License

[MIT](LICENSE)
"""
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated README.md with {data['metadata']['total_apis']} APIs")


def get_generic_apis_for_category(category_name: str, count: int) -> List[Dict[str, Any]]:
    """Get high-quality real APIs for a specific category.
    Only returns real, verified APIs - no generic placeholders.
    """
    # Map category names to API lists
    category_map = {
        'Authentication': [
            {
                'name': 'Auth0',
                'description': 'Authentication platform',
                'url': 'https://auth0.com/docs/api/authentication',
                'auth': 'OAuth',
                'https': True,
                'cors': 'yes',
                'popularity': 92,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            },
            {
                'name': 'Okta',
                'description': 'Identity management API',
                'url': 'https://developer.okta.com/docs/reference/',
                'auth': 'OAuth',
                'https': True,
                'cors': 'yes',
                'popularity': 90,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            },
            {
                'name': 'Firebase Auth',
                'description': 'Authentication service by Google Firebase',
                'url': 'https://firebase.google.com/docs/auth',
                'auth': 'apiKey',
                'https': True,
                'cors': 'yes',
                'popularity': 88,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            }
        ],
        'Development': [
            {
                'name': 'GitHub',
                'description': 'GitHub REST API',
                'url': 'https://docs.github.com/en/rest',
                'auth': 'OAuth',
                'https': True,
                'cors': 'yes',
                'popularity': 95,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            },
            {
                'name': 'GitLab',
                'description': 'GitLab API',
                'url': 'https://docs.gitlab.com/ee/api/',
                'auth': 'OAuth',
                'https': True,
                'cors': 'yes',
                'popularity': 88,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            },
            {
                'name': 'Stack Exchange',
                'description': 'Access to Stack Exchange API',
                'url': 'https://api.stackexchange.com/docs',
                'auth': 'OAuth',
                'https': True,
                'cors': 'yes',
                'popularity': 87,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            }
        ],
        'Weather': [
            {
                'name': 'OpenWeatherMap',
                'description': 'Weather forecasts and data',
                'url': 'https://openweathermap.org/api',
                'auth': 'apiKey',
                'https': True,
                'cors': 'yes',
                'popularity': 90,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            },
            {
                'name': 'WeatherAPI',
                'description': 'Weather API with forecasts',
                'url': 'https://www.weatherapi.com/',
                'auth': 'apiKey',
                'https': True,
                'cors': 'yes',
                'popularity': 88,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            },
            {
                'name': 'Tomorrow.io',
                'description': 'Weather API powered by proprietary technology',
                'url': 'https://www.tomorrow.io/weather-api/',
                'auth': 'apiKey',
                'https': True,
                'cors': 'yes',
                'popularity': 85,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            }
        ],
        'Blockchain': [
            {
                'name': 'Etherscan',
                'description': 'Ethereum blockchain explorer API',
                'url': 'https://etherscan.io/apis',
                'auth': 'apiKey',
                'https': True,
                'cors': 'yes',
                'popularity': 88,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            },
            {
                'name': 'CoinGecko',
                'description': 'Cryptocurrency data API',
                'url': 'https://www.coingecko.com/api/documentations/v3',
                'auth': 'No',
                'https': True,
                'cors': 'yes',
                'popularity': 90,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            },
            {
                'name': 'Blockchain.com',
                'description': 'Bitcoin blockchain API',
                'url': 'https://www.blockchain.com/api',
                'auth': 'apiKey',
                'https': True,
                'cors': 'unknown',
                'popularity': 85,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            }
        ]
    }
    
    # Return APIs for the requested category if available
    if category_name in category_map:
        return category_map[category_name][:count]
    
    # Return empty list for categories not in our map - no generic placeholders
    print(f"No high-quality APIs available for category '{category_name}'. Keeping category empty to maintain quality.")
    return []


def validate_api_url(url: str) -> bool:
    """Validate that an API URL is accessible."""
    try:
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.head(url, headers=headers, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        return response.status_code < 400  # Consider any 2xx or 3xx status as valid
    except Exception as e:
        print(f"Error validating URL {url}: {e}")
        return False


def is_api_duplicate(new_api: Dict[str, Any], existing_apis: List[Dict[str, Any]]) -> bool:
    """Check if an API already exists in the list."""
    for existing_api in existing_apis:
        if new_api['name'] == existing_api['name']:
            return True
        
        if new_api['url'] and existing_api['url']:
            api_url = new_api['url'].lower()
            existing_url = existing_api['url'].lower()
            
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
    category_counts = {category['name']: len(category['apis']) for category in updated_data['categories']}
    
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
                    category_counts[category_name] += 1
                    added_count += 1
                    print(f"Added new API: {new_api['name']} to category {category_name}")
                break
    
    # Log categories with fewer than 10 APIs but don't add generic APIs
    for category in updated_data['categories']:
        if category_counts[category['name']] < 10:
            print(f"Category {category['name']} has only {category_counts[category['name']]} APIs. Keeping as is to maintain quality.")
    
    # Update metadata
    total_apis = sum(len(category['apis']) for category in updated_data['categories'])
    updated_data['metadata']['total_apis'] = total_apis
    updated_data['metadata']['last_updated'] = datetime.datetime.now().isoformat()
    
    print(f"Added {added_count} new APIs")
    return updated_data


def scrape_apilist_fun() -> List[Dict[str, Any]]:
    """Scrape APIs from APIList.fun."""
    apis = []
    try:
        headers = {'User-Agent': get_random_user_agent()}
        url = 'https://apilist.fun/'
        
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            api_items = soup.select('.api-entry')
            
            for item in api_items:
                name_elem = item.select_one('.api-entry-name')
                desc_elem = item.select_one('.api-entry-description')
                link_elem = item.select_one('a')
                
                if name_elem and desc_elem and link_elem:
                    name = name_elem.text.strip()
                    description = desc_elem.text.strip()
                    url = link_elem['href']
                    
                    # Validate URL
                    if validate_api_url(url):
                        api = {
                            'name': name,
                            'description': description,
                            'url': url,
                            'auth': 'unknown',  # Need to determine from documentation
                            'https': True,      # Assume HTTPS
                            'cors': 'unknown',  # Need to determine from documentation
                            'category': 'Development'  # Default category
                        }
                        apis.append(api)
                        print(f"Found API: {name}")
    except Exception as e:
        print(f"Error scraping APIList.fun: {e}")
    
    return apis


def scrape_programmableweb() -> List[Dict[str, Any]]:
    """Scrape APIs from ProgrammableWeb."""
    apis = []
    try:
        headers = {'User-Agent': get_random_user_agent()}
        url = 'https://www.programmableweb.com/category/all/apis'
        
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            api_rows = soup.select('table.views-table tbody tr')
            
            for row in api_rows:
                name_elem = row.select_one('td.views-field-title a')
                desc_elem = row.select_one('td.views-field-field-api-description')
                category_elem = row.select_one('td.views-field-field-article-primary-category a')
                
                if name_elem and desc_elem:
                    name = name_elem.text.strip()
                    description = desc_elem.text.strip()
                    api_url = 'https://www.programmableweb.com' + name_elem['href']
                    
                    # Get the API documentation URL
                    try:
                        api_page = requests.get(api_url, headers=headers, timeout=REQUEST_TIMEOUT)
                        if api_page.status_code == 200:
                            api_soup = BeautifulSoup(api_page.text, 'html.parser')
                            doc_link = api_soup.select_one('a[href*="documentation"]')
                            if doc_link and 'href' in doc_link.attrs:
                                doc_url = doc_link['href']
                                if not doc_url.startswith('http'):
                                    doc_url = 'https://www.programmableweb.com' + doc_url
                            else:
                                # Try to find any external link
                                external_links = api_soup.select('a[href^="http"]:not([href*="programmableweb.com"])')
                                if external_links:
                                    doc_url = external_links[0]['href']
                                else:
                                    doc_url = api_url
                        else:
                            doc_url = api_url
                    except Exception:
                        doc_url = api_url
                    
                    category = 'Development'
                    if category_elem:
                        category = category_elem.text.strip()
                    
                    # Validate URL
                    if validate_api_url(doc_url):
                        api = {
                            'name': name,
                            'description': description,
                            'url': doc_url,
                            'auth': 'unknown',  # Need to determine from documentation
                            'https': True,      # Assume HTTPS
                            'cors': 'unknown',  # Need to determine from documentation
                            'category': category
                        }
                        apis.append(api)
                        print(f"Found API: {name}")
    except Exception as e:
        print(f"Error scraping ProgrammableWeb: {e}")
    
    return apis


def scrape_github_trending() -> List[Dict[str, Any]]:
    """Scrape trending API repositories from GitHub."""
    apis = []
    try:
        headers = {'User-Agent': get_random_user_agent()}
        url = 'https://github.com/topics/api'
        
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            repo_items = soup.select('article.border')
            
            for item in repo_items:
                name_elem = item.select_one('h3 a:last-child')
                desc_elem = item.select_one('div.px-3 > p')
                
                if name_elem and desc_elem:
                    repo_url = 'https://github.com' + name_elem['href']
                    name = name_elem.text.strip()
                    description = desc_elem.text.strip()
                    
                    # Get the API documentation URL
                    try:
                        repo_page = requests.get(repo_url, headers=headers, timeout=REQUEST_TIMEOUT)
                        if repo_page.status_code == 200:
                            repo_soup = BeautifulSoup(repo_page.text, 'html.parser')
                            
                            # Look for documentation links
                            doc_links = repo_soup.select('a[href*="docs"], a[href*="documentation"], a[href*="api-reference"]')
                            if doc_links:
                                doc_url = doc_links[0]['href']
                                if not doc_url.startswith('http'):
                                    doc_url = 'https://github.com' + doc_url
                            else:
                                doc_url = repo_url
                        else:
                            doc_url = repo_url
                    except Exception:
                        doc_url = repo_url
                    
                    # Validate URL
                    if validate_api_url(doc_url):
                        api = {
                            'name': name,
                            'description': description,
                            'url': doc_url,
                            'auth': 'unknown',  # Need to determine from documentation
                            'https': True,      # Assume HTTPS
                            'cors': 'unknown',  # Need to determine from documentation
                            'category': 'Development'  # Default category
                        }
                        apis.append(api)
                        print(f"Found API: {name}")
    except Exception as e:
        print(f"Error scraping GitHub trending: {e}")
    
    return apis


def main() -> None:
    """Main function to discover trending APIs and update the README."""
    print("Loading current API data...")
    data = load_data()
    
    print("Scraping new APIs...")
    new_apis = []
    
    # Scrape from various sources
    new_apis.extend(scrape_apilist_fun())
    new_apis.extend(scrape_programmableweb())
    new_apis.extend(scrape_github_trending())
    
    print(f"Found {len(new_apis)} potential new APIs")
    
    print("Adding new APIs to the data...")
    updated_data = add_new_apis(data, new_apis)
    
    print("Saving updated data to README.md...")
    save_data(updated_data)
    
    print("Done!")


if __name__ == "__main__":
    main()
