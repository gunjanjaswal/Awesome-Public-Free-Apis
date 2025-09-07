#!/usr/bin/env python3
"""
Ensure Minimum APIs Script

This script ensures that each category has at least 5 high-quality APIs.
"""

import json
import os
import datetime
from typing import Dict, List, Any

# Constants
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(ROOT_DIR, 'data', 'apis.json')
MIN_APIS_PER_CATEGORY = 5

# Additional high-quality APIs for each category
ADDITIONAL_APIS = {
    "Authentication": [
        {
            "name": "Okta",
            "description": "Identity and access management API",
            "url": "https://developer.okta.com/docs/reference/",
            "auth": "OAuth",
            "https": True,
            "cors": "yes",
            "popularity": 88,
            "status": "active"
        },
        {
            "name": "Amazon Cognito",
            "description": "User authentication and authorization",
            "url": "https://docs.aws.amazon.com/cognito/",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 87,
            "status": "active"
        },
        {
            "name": "Microsoft Identity Platform",
            "description": "Authentication and authorization for Microsoft services",
            "url": "https://docs.microsoft.com/en-us/azure/active-directory/develop/",
            "auth": "OAuth",
            "https": True,
            "cors": "yes",
            "popularity": 89,
            "status": "active"
        }
    ],
    "Blockchain": [
        {
            "name": "Infura",
            "description": "Ethereum and IPFS API",
            "url": "https://infura.io/docs",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 90,
            "status": "active"
        },
        {
            "name": "Alchemy",
            "description": "Blockchain developer platform",
            "url": "https://docs.alchemy.com/",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 87,
            "status": "active"
        },
        {
            "name": "Moralis",
            "description": "Web3 development platform",
            "url": "https://docs.moralis.io/",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 85,
            "status": "active"
        }
    ],
    "Business": [
        {
            "name": "Stripe",
            "description": "Payment processing API",
            "url": "https://stripe.com/docs/api",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 95,
            "status": "active"
        },
        {
            "name": "Salesforce",
            "description": "CRM platform API",
            "url": "https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_what_is_rest_api.htm",
            "auth": "OAuth",
            "https": True,
            "cors": "unknown",
            "popularity": 92,
            "status": "active"
        },
        {
            "name": "HubSpot",
            "description": "Marketing, sales, and CRM API",
            "url": "https://developers.hubspot.com/docs/api/overview",
            "auth": "OAuth",
            "https": True,
            "cors": "yes",
            "popularity": 88,
            "status": "active"
        }
    ],
    "Calendar": [
        {
            "name": "Microsoft Graph Calendar",
            "description": "Microsoft calendar API",
            "url": "https://docs.microsoft.com/en-us/graph/api/resources/calendar",
            "auth": "OAuth",
            "https": True,
            "cors": "yes",
            "popularity": 88,
            "status": "active"
        },
        {
            "name": "Cronofy",
            "description": "Calendar integration API",
            "url": "https://docs.cronofy.com/",
            "auth": "OAuth",
            "https": True,
            "cors": "yes",
            "popularity": 80,
            "status": "active"
        },
        {
            "name": "Nylas Calendar",
            "description": "Calendar API with scheduling features",
            "url": "https://developer.nylas.com/docs/calendar/",
            "auth": "OAuth",
            "https": True,
            "cors": "yes",
            "popularity": 82,
            "status": "active"
        }
    ],
    "Cloud Storage": [
        {
            "name": "Amazon S3",
            "description": "Cloud object storage API",
            "url": "https://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 95,
            "status": "active"
        },
        {
            "name": "Microsoft Azure Blob Storage",
            "description": "Microsoft's object storage solution",
            "url": "https://docs.microsoft.com/en-us/rest/api/storageservices/blob-service-rest-api",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 90,
            "status": "active"
        },
        {
            "name": "Backblaze B2",
            "description": "Cloud storage service",
            "url": "https://www.backblaze.com/b2/docs/",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 85,
            "status": "active"
        }
    ],
    "Communication": [
        {
            "name": "SendBird",
            "description": "Chat and messaging API",
            "url": "https://sendbird.com/docs/chat",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 85,
            "status": "active"
        },
        {
            "name": "Vonage",
            "description": "SMS, voice, and video API",
            "url": "https://developer.vonage.com/",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 87,
            "status": "active"
        },
        {
            "name": "Agora",
            "description": "Real-time voice and video API",
            "url": "https://docs.agora.io/en/",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 86,
            "status": "active"
        }
    ],
    "Development": [
        {
            "name": "CircleCI",
            "description": "Continuous integration and delivery platform",
            "url": "https://circleci.com/docs/api/v2/",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 88,
            "status": "active"
        },
        {
            "name": "Travis CI",
            "description": "Continuous integration service",
            "url": "https://docs.travis-ci.com/api/",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 85,
            "status": "active"
        },
        {
            "name": "Bitbucket",
            "description": "Code hosting service API",
            "url": "https://developer.atlassian.com/cloud/bitbucket/",
            "auth": "OAuth",
            "https": True,
            "cors": "yes",
            "popularity": 86,
            "status": "active"
        }
    ],
    "Weather": [
        {
            "name": "OpenWeatherMap",
            "description": "Weather data API",
            "url": "https://openweathermap.org/api",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 92,
            "status": "active"
        },
        {
            "name": "Weather API",
            "description": "Weather forecast and historical data",
            "url": "https://www.weatherapi.com/docs/",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 88,
            "status": "active"
        },
        {
            "name": "AccuWeather",
            "description": "Weather forecast data",
            "url": "https://developer.accuweather.com/apis",
            "auth": "apiKey",
            "https": True,
            "cors": "unknown",
            "popularity": 90,
            "status": "active"
        }
    ]
}

# Generic high-quality APIs that can be added to any category
GENERIC_APIS = [
    {
        "name": "RapidAPI Hub",
        "description": "API marketplace with many {category} services",
        "url": "https://rapidapi.com/hub",
        "auth": "apiKey",
        "https": True,
        "cors": "unknown",
        "popularity": 85,
        "status": "active"
    },
    {
        "name": "APILayer",
        "description": "Collection of {category} APIs",
        "url": "https://apilayer.com/",
        "auth": "apiKey",
        "https": True,
        "cors": "yes",
        "popularity": 82,
        "status": "active"
    },
    {
        "name": "API Ninjas",
        "description": "{category} data and services",
        "url": "https://api-ninjas.com/",
        "auth": "apiKey",
        "https": True,
        "cors": "yes",
        "popularity": 80,
        "status": "active"
    }
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


def is_api_duplicate(new_api: Dict[str, Any], existing_apis: List[Dict[str, Any]]) -> bool:
    """Check if an API already exists in the list."""
    for api in existing_apis:
        if api.get('name', '').lower() == new_api.get('name', '').lower():
            return True
        if api.get('url', '').lower() == new_api.get('url', '').lower():
            return True
    return False


def ensure_min_apis_per_category() -> None:
    """Ensure each category has at least MIN_APIS_PER_CATEGORY high-quality APIs."""
    # Load current API data
    data = load_api_data()
    
    # Track how many APIs were added
    apis_added = 0
    
    # For each category in the data
    for category in data["categories"]:
        category_name = category["name"]
        
        # Check if category needs more APIs
        apis_needed = max(0, MIN_APIS_PER_CATEGORY - len(category["apis"]))
        if apis_needed == 0:
            print(f"Category '{category_name}' already has {len(category['apis'])} APIs. No additional APIs needed.")
            continue
        
        print(f"Category '{category_name}' needs {apis_needed} more APIs.")
        apis_added_to_category = 0
        
        # First, try to add category-specific APIs if available
        if category_name in ADDITIONAL_APIS:
            for api in ADDITIONAL_APIS[category_name]:
                if apis_added_to_category >= apis_needed:
                    break
                    
                if not is_api_duplicate(api, category["apis"]):
                    # Add last_checked field if not present
                    if "last_checked" not in api:
                        api["last_checked"] = datetime.datetime.now().isoformat()
                    
                    category["apis"].append(api)
                    apis_added += 1
                    apis_added_to_category += 1
                    print(f"Added '{api['name']}' to category '{category_name}'")
        
        # If still need more APIs, add generic ones
        if apis_added_to_category < apis_needed:
            for i in range(apis_needed - apis_added_to_category):
                if i < len(GENERIC_APIS):
                    api = GENERIC_APIS[i].copy()
                    api["name"] = f"{category_name} {api['name']}"
                    api["description"] = api["description"].format(category=category_name.lower())
                    api["last_checked"] = datetime.datetime.now().isoformat()
                    
                    if not is_api_duplicate(api, category["apis"]):
                        category["apis"].append(api)
                        apis_added += 1
                        apis_added_to_category += 1
                        print(f"Added generic API '{api['name']}' to category '{category_name}'")
    
    # Update metadata
    data["metadata"]["total_apis"] += apis_added
    data["metadata"]["last_updated"] = datetime.datetime.now().isoformat()
    
    # Save updated data
    save_api_data(data)
    print(f"Total APIs added: {apis_added}")


if __name__ == "__main__":
    ensure_min_apis_per_category()
