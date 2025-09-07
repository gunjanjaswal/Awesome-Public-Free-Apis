#!/usr/bin/env python3
"""
Initial API Data Population Script

This script populates the apis.json file with initial API data to get started.
It adds a set of popular, reliable APIs across different categories.
"""

import json
import os
import datetime
from typing import Dict, List, Any

# Constants
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(ROOT_DIR, 'data', 'apis.json')

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

def get_initial_apis() -> Dict[str, List[Dict[str, Any]]]:
    """Get initial API data to populate the file."""
    current_time = datetime.datetime.now().isoformat()
    
    return {
        "Weather": [
            {
                "name": "OpenWeatherMap",
                "description": "Current weather data, forecasts, and historical data for any location",
                "url": "https://openweathermap.org/api",
                "auth": "apiKey",
                "https": True,
                "cors": "yes",
                "popularity": 95,
                "status": "active",
                "working": True,
                "last_checked": current_time
            },
            {
                "name": "WeatherAPI",
                "description": "Weather forecast and historical data with high precision",
                "url": "https://www.weatherapi.com/",
                "auth": "apiKey",
                "https": True,
                "cors": "yes",
                "popularity": 90,
                "status": "active",
                "working": True,
                "last_checked": current_time
            },
            {
                "name": "Tomorrow.io",
                "description": "Weather API with hyperlocal forecasts and historical data",
                "url": "https://www.tomorrow.io/weather-api/",
                "auth": "apiKey",
                "https": True,
                "cors": "yes",
                "popularity": 85,
                "status": "active",
                "working": True,
                "last_checked": current_time
            }
        ],
        "Development": [
            {
                "name": "GitHub",
                "description": "Complete developer platform to build, scale, and deliver secure software",
                "url": "https://docs.github.com/en/rest",
                "auth": "OAuth",
                "https": True,
                "cors": "yes",
                "popularity": 98,
                "status": "active",
                "working": True,
                "last_checked": current_time
            },
            {
                "name": "Stack Exchange",
                "description": "Access to Stack Exchange API, including all Stack Overflow data",
                "url": "https://api.stackexchange.com/",
                "auth": "OAuth",
                "https": True,
                "cors": "yes",
                "popularity": 92,
                "status": "active",
                "working": True,
                "last_checked": current_time
            },
            {
                "name": "JSON Placeholder",
                "description": "Fake data for testing and prototyping",
                "url": "https://jsonplaceholder.typicode.com/",
                "auth": "",
                "https": True,
                "cors": "yes",
                "popularity": 90,
                "status": "active",
                "working": True,
                "last_checked": current_time
            }
        ],
        "Finance": [
            {
                "name": "Alpha Vantage",
                "description": "Realtime and historical stock data, forex, and cryptocurrency",
                "url": "https://www.alphavantage.co/",
                "auth": "apiKey",
                "https": True,
                "cors": "yes",
                "popularity": 92,
                "status": "active",
                "working": True,
                "last_checked": current_time
            },
            {
                "name": "Coinbase",
                "description": "Bitcoin, Bitcoin Cash, Litecoin, Ethereum, and more prices",
                "url": "https://docs.cloud.coinbase.com/sign-in-with-coinbase/docs/api-users",
                "auth": "apiKey",
                "https": True,
                "cors": "unknown",
                "popularity": 88,
                "status": "active",
                "working": True,
                "last_checked": current_time
            }
        ],
        "News": [
            {
                "name": "NewsAPI",
                "description": "Search for articles from over 80,000 news sources",
                "url": "https://newsapi.org/",
                "auth": "apiKey",
                "https": True,
                "cors": "unknown",
                "popularity": 90,
                "status": "active",
                "working": True,
                "last_checked": current_time
            },
            {
                "name": "New York Times",
                "description": "Article search, best sellers, campaign finance, community, most popular, and more",
                "url": "https://developer.nytimes.com/",
                "auth": "apiKey",
                "https": True,
                "cors": "unknown",
                "popularity": 87,
                "status": "active",
                "working": True,
                "last_checked": current_time
            }
        ],
        "Entertainment": [
            {
                "name": "TMDB",
                "description": "Community-built movie and TV database",
                "url": "https://www.themoviedb.org/documentation/api",
                "auth": "apiKey",
                "https": True,
                "cors": "yes",
                "popularity": 94,
                "status": "active",
                "working": True,
                "last_checked": current_time
            },
            {
                "name": "OMDB",
                "description": "Open Movie Database",
                "url": "https://www.omdbapi.com/",
                "auth": "apiKey",
                "https": True,
                "cors": "yes",
                "popularity": 92,
                "status": "active",
                "working": True,
                "last_checked": current_time
            },
            {
                "name": "Marvel",
                "description": "Marvel Comics API",
                "url": "https://developer.marvel.com/",
                "auth": "apiKey",
                "https": True,
                "cors": "unknown",
                "popularity": 85,
                "status": "active",
                "working": True,
                "last_checked": current_time
            }
        ],
        "Geocoding": [
            {
                "name": "Google Maps",
                "description": "Create customized, agile experiences that bring the real world to your users",
                "url": "https://developers.google.com/maps/",
                "auth": "apiKey",
                "https": True,
                "cors": "yes",
                "popularity": 96,
                "status": "active",
                "working": True,
                "last_checked": current_time
            },
            {
                "name": "OpenStreetMap",
                "description": "Navigation, geolocation and maps",
                "url": "https://wiki.openstreetmap.org/wiki/API",
                "auth": "OAuth",
                "https": True,
                "cors": "unknown",
                "popularity": 90,
                "status": "active",
                "working": True,
                "last_checked": current_time
            }
        ],
        "Machine Learning": [
            {
                "name": "OpenAI",
                "description": "Create images, generate text, analyze data, and more",
                "url": "https://platform.openai.com/docs/api-reference",
                "auth": "apiKey",
                "https": True,
                "cors": "yes",
                "popularity": 98,
                "status": "active",
                "working": True,
                "last_checked": current_time
            },
            {
                "name": "Hugging Face",
                "description": "Access to state-of-the-art machine learning models",
                "url": "https://huggingface.co/docs/api-inference/index",
                "auth": "apiKey",
                "https": True,
                "cors": "unknown",
                "popularity": 92,
                "status": "active",
                "working": True,
                "last_checked": current_time
            }
        ],
        "Social": [
            {
                "name": "Twitter",
                "description": "Access Twitter data",
                "url": "https://developer.twitter.com/en/docs",
                "auth": "OAuth",
                "https": True,
                "cors": "yes",
                "popularity": 95,
                "status": "active",
                "working": True,
                "last_checked": current_time
            },
            {
                "name": "Reddit",
                "description": "Reddit API",
                "url": "https://www.reddit.com/dev/api",
                "auth": "OAuth",
                "https": True,
                "cors": "yes",
                "popularity": 93,
                "status": "active",
                "working": True,
                "last_checked": current_time
            }
        ],
        "Photography": [
            {
                "name": "Unsplash",
                "description": "Free high-resolution photos",
                "url": "https://unsplash.com/developers",
                "auth": "OAuth",
                "https": True,
                "cors": "yes",
                "popularity": 92,
                "status": "active",
                "working": True,
                "last_checked": current_time
            },
            {
                "name": "Pexels",
                "description": "Free stock photos and videos",
                "url": "https://www.pexels.com/api/",
                "auth": "apiKey",
                "https": True,
                "cors": "yes",
                "popularity": 90,
                "status": "active",
                "working": True,
                "last_checked": current_time
            }
        ],
        "Text Analysis": [
            {
                "name": "Sentiment Analysis",
                "description": "Multilingual sentiment analysis of texts",
                "url": "https://www.meaningcloud.com/developer/sentiment-analysis",
                "auth": "apiKey",
                "https": True,
                "cors": "yes",
                "popularity": 85,
                "status": "active",
                "working": True,
                "last_checked": current_time
            },
            {
                "name": "Wordnik",
                "description": "Dictionary data including definitions, parts of speech, pronunciation, usage examples, and more",
                "url": "https://developer.wordnik.com/",
                "auth": "apiKey",
                "https": True,
                "cors": "unknown",
                "popularity": 80,
                "status": "active",
                "working": True,
                "last_checked": current_time
            }
        ]
    }

def populate_apis() -> None:
    """Populate the apis.json file with initial API data."""
    # Load existing data
    data = load_api_data()
    
    # Get initial APIs
    initial_apis = get_initial_apis()
    
    # Add APIs to their respective categories
    total_apis = 0
    for category in data["categories"]:
        category_name = category["name"]
        if category_name in initial_apis:
            category["apis"] = initial_apis[category_name]
            total_apis += len(initial_apis[category_name])
            print(f"Added {len(initial_apis[category_name])} APIs to {category_name} category")
    
    # Update metadata
    data["metadata"]["total_apis"] = total_apis
    data["metadata"]["last_updated"] = datetime.datetime.now().isoformat()
    
    # Save updated data
    save_api_data(data)
    print(f"Added a total of {total_apis} APIs across {len(initial_apis)} categories")

def main():
    """Main function to populate the apis.json file with initial API data."""
    print("Starting initial API population process...")
    print(f"Data file path: {DATA_FILE}")
    
    # Check if data directory exists
    data_dir = os.path.dirname(DATA_FILE)
    if not os.path.exists(data_dir):
        print(f"Creating data directory: {data_dir}")
        os.makedirs(data_dir)
    
    # Load existing data
    data = load_api_data()
    print(f"Loaded data with {len(data['categories'])} categories")
    
    # Populate APIs
    populate_apis()
    print("Initial API population process completed.")

if __name__ == "__main__":
    main()
