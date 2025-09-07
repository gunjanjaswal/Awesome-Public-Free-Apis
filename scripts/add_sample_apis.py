#!/usr/bin/env python3
"""
Simple script to add sample APIs to the apis.json file
"""

import json
import os
import datetime

# Constants
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'apis.json')

def main():
    print(f"Data file path: {DATA_FILE}")
    
    # Check if data directory exists
    data_dir = os.path.dirname(DATA_FILE)
    if not os.path.exists(data_dir):
        print(f"Creating data directory: {data_dir}")
        os.makedirs(data_dir)
    
    # Create sample data
    current_time = datetime.datetime.now().isoformat()
    
    data = {
        "categories": [
            {
                "name": "Weather",
                "description": "APIs for weather data and forecasts",
                "apis": [
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
                    }
                ]
            },
            {
                "name": "Development",
                "description": "APIs for software development tools and services",
                "apis": [
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
                ]
            },
            {
                "name": "Entertainment",
                "description": "APIs for entertainment content and services",
                "apis": [
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
                    }
                ]
            }
        ],
        "metadata": {
            "total_apis": 6,
            "last_updated": current_time,
            "version": "1.0.0"
        }
    }
    
    # Save data to file
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)
        print(f"Sample API data saved to {DATA_FILE}")
    except Exception as e:
        print(f"Error saving API data: {e}")

if __name__ == "__main__":
    main()
