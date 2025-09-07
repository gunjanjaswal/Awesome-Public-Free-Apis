#!/usr/bin/env python3
"""
Category Population Script

This script adds sample APIs to each category to ensure all categories have at least some content.
"""

import json
import os
import datetime
from typing import Dict, List, Any

# Constants
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(ROOT_DIR, 'data', 'apis.json')

# Sample APIs for each category
SAMPLE_APIS = {
    "Authentication": [
        {
            "name": "Auth0",
            "description": "Easy to implement, adaptable authentication and authorization platform",
            "url": "https://auth0.com/docs/api/authentication",
            "auth": "OAuth",
            "https": True,
            "cors": "yes",
            "popularity": 92,
            "status": "active"
        },
        {
            "name": "Firebase Auth",
            "description": "Authentication service by Firebase",
            "url": "https://firebase.google.com/docs/auth",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 90,
            "status": "active"
        }
    ],
    "Blockchain": [
        {
            "name": "Etherscan",
            "description": "Ethereum explorer API",
            "url": "https://etherscan.io/apis",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 88,
            "status": "active"
        },
        {
            "name": "CoinGecko",
            "description": "Cryptocurrency data API",
            "url": "https://www.coingecko.com/api/documentations/v3",
            "auth": "No",
            "https": True,
            "cors": "yes",
            "popularity": 95,
            "status": "active"
        }
    ],
    "Business": [
        {
            "name": "Clearbit",
            "description": "Company data enrichment API",
            "url": "https://clearbit.com/docs",
            "auth": "apiKey",
            "https": True,
            "cors": "unknown",
            "popularity": 85,
            "status": "active"
        },
        {
            "name": "Hunter",
            "description": "Email verification API",
            "url": "https://hunter.io/api",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 82,
            "status": "active"
        }
    ],
    "Calendar": [
        {
            "name": "Google Calendar",
            "description": "Calendar API by Google",
            "url": "https://developers.google.com/calendar",
            "auth": "OAuth",
            "https": True,
            "cors": "yes",
            "popularity": 90,
            "status": "active"
        },
        {
            "name": "Nager.Date",
            "description": "Public holidays for more than 90 countries",
            "url": "https://date.nager.at/Api",
            "auth": "No",
            "https": True,
            "cors": "yes",
            "popularity": 75,
            "status": "active"
        }
    ],
    "Cloud Storage": [
        {
            "name": "Dropbox",
            "description": "File storage and sharing API",
            "url": "https://www.dropbox.com/developers",
            "auth": "OAuth",
            "https": True,
            "cors": "yes",
            "popularity": 88,
            "status": "active"
        },
        {
            "name": "Google Drive",
            "description": "File storage and sharing API by Google",
            "url": "https://developers.google.com/drive",
            "auth": "OAuth",
            "https": True,
            "cors": "yes",
            "popularity": 92,
            "status": "active"
        }
    ],
    "Communication": [
        {
            "name": "Twilio",
            "description": "SMS, Voice and Video API",
            "url": "https://www.twilio.com/docs/api",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 95,
            "status": "active"
        },
        {
            "name": "MessageBird",
            "description": "SMS, Voice and Chat API",
            "url": "https://developers.messagebird.com/",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 85,
            "status": "active"
        }
    ],
    "Cryptocurrency": [
        {
            "name": "Binance",
            "description": "Exchange for trading cryptocurrencies",
            "url": "https://binance-docs.github.io/apidocs/",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 95,
            "status": "active"
        },
        {
            "name": "CoinAPI",
            "description": "All cryptocurrency exchanges integrated under a single API",
            "url": "https://docs.coinapi.io/",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 85,
            "status": "active"
        }
    ],
    "Currency Exchange": [
        {
            "name": "ExchangeRate-API",
            "description": "Free currency exchange rates API",
            "url": "https://www.exchangerate-api.com",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 88,
            "status": "active"
        },
        {
            "name": "Fixer.io",
            "description": "Foreign exchange rates and currency conversion API",
            "url": "https://fixer.io",
            "auth": "apiKey",
            "https": True,
            "cors": "unknown",
            "popularity": 85,
            "status": "active"
        }
    ],
    "Data Validation": [
        {
            "name": "Abstract Email Validation",
            "description": "Validate email addresses",
            "url": "https://www.abstractapi.com/email-verification-validation-api",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 80,
            "status": "active"
        },
        {
            "name": "Vatlayer",
            "description": "VAT number validation",
            "url": "https://vatlayer.com/documentation",
            "auth": "apiKey",
            "https": True,
            "cors": "unknown",
            "popularity": 75,
            "status": "active"
        }
    ],
    "Email": [
        {
            "name": "Mailgun",
            "description": "Email API service",
            "url": "https://www.mailgun.com/",
            "auth": "apiKey",
            "https": True,
            "cors": "unknown",
            "popularity": 90,
            "status": "active"
        },
        {
            "name": "SendGrid",
            "description": "Email API",
            "url": "https://sendgrid.com/docs/API_Reference/api_v3.html",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 92,
            "status": "active"
        }
    ],
    "Environment": [
        {
            "name": "AirVisual",
            "description": "Air quality and weather data",
            "url": "https://www.iqair.com/air-pollution-data-api",
            "auth": "apiKey",
            "https": True,
            "cors": "unknown",
            "popularity": 85,
            "status": "active"
        },
        {
            "name": "OpenAQ",
            "description": "Open air quality data",
            "url": "https://docs.openaq.org/",
            "auth": "No",
            "https": True,
            "cors": "unknown",
            "popularity": 80,
            "status": "active"
        }
    ],
    "Finance": [
        {
            "name": "Alpha Vantage",
            "description": "Realtime and historical stock data",
            "url": "https://www.alphavantage.co/",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 92,
            "status": "active"
        },
        {
            "name": "IEX Cloud",
            "description": "Realtime and historical stock data",
            "url": "https://iexcloud.io/docs/api/",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 88,
            "status": "active"
        }
    ],
    "Food & Drink": [
        {
            "name": "Spoonacular",
            "description": "Recipe, food, and nutrition API",
            "url": "https://spoonacular.com/food-api",
            "auth": "apiKey",
            "https": True,
            "cors": "unknown",
            "popularity": 88,
            "status": "active"
        },
        {
            "name": "Open Food Facts",
            "description": "Food products database",
            "url": "https://world.openfoodfacts.org/data",
            "auth": "No",
            "https": True,
            "cors": "unknown",
            "popularity": 82,
            "status": "active"
        }
    ],
    "Games & Comics": [
        {
            "name": "Fortnite",
            "description": "Fortnite stats API",
            "url": "https://fortnitetracker.com/site-api",
            "auth": "apiKey",
            "https": True,
            "cors": "unknown",
            "popularity": 85,
            "status": "active"
        },
        {
            "name": "Marvel",
            "description": "Marvel Comics API",
            "url": "https://developer.marvel.com/",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 87,
            "status": "active"
        }
    ],
    "Geocoding": [
        {
            "name": "Google Maps",
            "description": "Maps, geolocation and places data",
            "url": "https://developers.google.com/maps/",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 95,
            "status": "active"
        },
        {
            "name": "Mapbox",
            "description": "Maps, geolocation and places data",
            "url": "https://docs.mapbox.com/api/",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 92,
            "status": "active"
        }
    ],
    "Government": [
        {
            "name": "Data.gov",
            "description": "US Government data",
            "url": "https://api.data.gov/",
            "auth": "apiKey",
            "https": True,
            "cors": "unknown",
            "popularity": 85,
            "status": "active"
        },
        {
            "name": "NASA",
            "description": "NASA data, including imagery",
            "url": "https://api.nasa.gov",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 90,
            "status": "active"
        }
    ],
    "Health": [
        {
            "name": "Nutritionix",
            "description": "Nutrition database API",
            "url": "https://developer.nutritionix.com/",
            "auth": "apiKey",
            "https": True,
            "cors": "unknown",
            "popularity": 85,
            "status": "active"
        },
        {
            "name": "COVID-19",
            "description": "COVID 19 spread, infection and recovery",
            "url": "https://covid19api.com/",
            "auth": "No",
            "https": True,
            "cors": "yes",
            "popularity": 90,
            "status": "active"
        }
    ],
    "Jobs": [
        {
            "name": "Indeed",
            "description": "Job board aggregator",
            "url": "https://developer.indeed.com/",
            "auth": "apiKey",
            "https": True,
            "cors": "unknown",
            "popularity": 88,
            "status": "active"
        },
        {
            "name": "LinkedIn",
            "description": "Professional networking platform",
            "url": "https://developer.linkedin.com/",
            "auth": "OAuth",
            "https": True,
            "cors": "unknown",
            "popularity": 90,
            "status": "active"
        }
    ],
    "Music": [
        {
            "name": "Deezer",
            "description": "Music streaming service",
            "url": "https://developers.deezer.com/api",
            "auth": "OAuth",
            "https": True,
            "cors": "unknown",
            "popularity": 85,
            "status": "active"
        },
        {
            "name": "Genius",
            "description": "Song lyrics and knowledge",
            "url": "https://docs.genius.com/",
            "auth": "OAuth",
            "https": True,
            "cors": "unknown",
            "popularity": 82,
            "status": "active"
        }
    ],
    "News": [
        {
            "name": "NewsAPI",
            "description": "Headlines currently published on various news sources and blogs",
            "url": "https://newsapi.org/",
            "auth": "apiKey",
            "https": True,
            "cors": "unknown",
            "popularity": 90,
            "status": "active"
        },
        {
            "name": "New York Times",
            "description": "News articles and metadata from NYT",
            "url": "https://developer.nytimes.com/",
            "auth": "apiKey",
            "https": True,
            "cors": "unknown",
            "popularity": 88,
            "status": "active"
        }
    ],
    "Open Data": [
        {
            "name": "OpenDataSoft",
            "description": "Cloud-based data publishing platform",
            "url": "https://www.opendatasoft.com/",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 80,
            "status": "active"
        },
        {
            "name": "Kaggle",
            "description": "Data science and machine learning platform",
            "url": "https://www.kaggle.com/docs/api",
            "auth": "apiKey",
            "https": True,
            "cors": "unknown",
            "popularity": 88,
            "status": "active"
        }
    ],
    "Open Source Projects": [
        {
            "name": "Libraries.io",
            "description": "Open source software libraries",
            "url": "https://libraries.io/api",
            "auth": "apiKey",
            "https": True,
            "cors": "unknown",
            "popularity": 82,
            "status": "active"
        },
        {
            "name": "Open Collective",
            "description": "Open Collective API",
            "url": "https://docs.opencollective.com/help/developers/api",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 75,
            "status": "active"
        }
    ],
    "Patent": [
        {
            "name": "EPO",
            "description": "European Patent Office",
            "url": "https://developers.epo.org/",
            "auth": "OAuth",
            "https": True,
            "cors": "unknown",
            "popularity": 80,
            "status": "active"
        },
        {
            "name": "USPTO",
            "description": "US Patent and Trademark Office API",
            "url": "https://www.uspto.gov/learning-and-resources/open-data-and-mobility",
            "auth": "No",
            "https": True,
            "cors": "unknown",
            "popularity": 82,
            "status": "active"
        }
    ],
    "Personality": [
        {
            "name": "Advice Slip",
            "description": "Generate random advice slips",
            "url": "https://api.adviceslip.com/",
            "auth": "No",
            "https": True,
            "cors": "unknown",
            "popularity": 75,
            "status": "active"
        },
        {
            "name": "Affirmations",
            "description": "Daily affirmations",
            "url": "https://affirmations.dev/",
            "auth": "No",
            "https": True,
            "cors": "yes",
            "popularity": 70,
            "status": "active"
        }
    ],
    "Phone": [
        {
            "name": "Twilio Lookup",
            "description": "Phone number verification and information",
            "url": "https://www.twilio.com/docs/lookup/api",
            "auth": "apiKey",
            "https": True,
            "cors": "unknown",
            "popularity": 88,
            "status": "active"
        },
        {
            "name": "NumVerify",
            "description": "Phone number validation",
            "url": "https://numverify.com/",
            "auth": "apiKey",
            "https": True,
            "cors": "unknown",
            "popularity": 82,
            "status": "active"
        }
    ],
    "Science & Math": [
        {
            "name": "Numbers API",
            "description": "Facts about numbers",
            "url": "http://numbersapi.com/",
            "auth": "No",
            "https": False,
            "cors": "yes",
            "popularity": 80,
            "status": "active"
        },
        {
            "name": "ISRO",
            "description": "ISRO Space Crafts Information",
            "url": "https://isro.vercel.app",
            "auth": "No",
            "https": True,
            "cors": "yes",
            "popularity": 75,
            "status": "active"
        }
    ],
    "Security": [
        {
            "name": "Have I Been Pwned",
            "description": "Check if email or password has been compromised",
            "url": "https://haveibeenpwned.com/API/v3",
            "auth": "apiKey",
            "https": True,
            "cors": "unknown",
            "popularity": 92,
            "status": "active"
        },
        {
            "name": "Virushee",
            "description": "Virushee file reputation service and malware lookup",
            "url": "https://api.virushee.com/",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 75,
            "status": "active"
        }
    ],
    "Shopping": [
        {
            "name": "Shopify",
            "description": "E-commerce platform",
            "url": "https://shopify.dev/docs/admin-api",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 92,
            "status": "active"
        },
        {
            "name": "Best Buy",
            "description": "Products, categories, stores and availability",
            "url": "https://bestbuyapis.github.io/api-documentation/",
            "auth": "apiKey",
            "https": True,
            "cors": "unknown",
            "popularity": 85,
            "status": "active"
        }
    ],
    "Social": [
        {
            "name": "Twitter",
            "description": "Twitter API",
            "url": "https://developer.twitter.com/en/docs",
            "auth": "OAuth",
            "https": True,
            "cors": "yes",
            "popularity": 95,
            "status": "active"
        },
        {
            "name": "Reddit",
            "description": "Reddit API",
            "url": "https://www.reddit.com/dev/api",
            "auth": "OAuth",
            "https": True,
            "cors": "yes",
            "popularity": 92,
            "status": "active"
        }
    ],
    "Sports & Fitness": [
        {
            "name": "Football-Data.org",
            "description": "Football data and statistics",
            "url": "https://www.football-data.org/",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 85,
            "status": "active"
        },
        {
            "name": "TheSportsDB",
            "description": "Sports data",
            "url": "https://www.thesportsdb.com/api.php",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 82,
            "status": "active"
        }
    ],
    "Test Data": [
        {
            "name": "JSONPlaceholder",
            "description": "Fake data for testing",
            "url": "https://jsonplaceholder.typicode.com/",
            "auth": "No",
            "https": True,
            "cors": "yes",
            "popularity": 90,
            "status": "active"
        },
        {
            "name": "Mockaroo",
            "description": "Generate realistic test data",
            "url": "https://www.mockaroo.com/docs",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 85,
            "status": "active"
        }
    ],
    "Text Analysis": [
        {
            "name": "Sentiment Analysis",
            "description": "Analyze text for sentiment",
            "url": "https://www.meaningcloud.com/developer/sentiment-analysis",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 85,
            "status": "active"
        },
        {
            "name": "Wordnik",
            "description": "Dictionary data",
            "url": "https://developer.wordnik.com/",
            "auth": "apiKey",
            "https": True,
            "cors": "unknown",
            "popularity": 80,
            "status": "active"
        }
    ],
    "Tracking": [
        {
            "name": "Postmon",
            "description": "Brazilian zip code API",
            "url": "https://postmon.com.br/",
            "auth": "No",
            "https": True,
            "cors": "yes",
            "popularity": 75,
            "status": "active"
        },
        {
            "name": "Aftership",
            "description": "Shipping tracking API",
            "url": "https://developers.aftership.com/reference/quick-start",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "popularity": 85,
            "status": "active"
        }
    ],
    "Transportation": [
        {
            "name": "Uber",
            "description": "Uber ride requests and price estimation",
            "url": "https://developer.uber.com/",
            "auth": "OAuth",
            "https": True,
            "cors": "yes",
            "popularity": 90,
            "status": "active"
        },
        {
            "name": "Amadeus",
            "description": "Travel search - flights, hotels, cars",
            "url": "https://developers.amadeus.com/",
            "auth": "OAuth",
            "https": True,
            "cors": "yes",
            "popularity": 88,
            "status": "active"
        }
    ],
    "URL Shorteners": [
        {
            "name": "Bitly",
            "description": "URL shortener and link management",
            "url": "https://dev.bitly.com/",
            "auth": "OAuth",
            "https": True,
            "cors": "unknown",
            "popularity": 90,
            "status": "active"
        },
        {
            "name": "TinyURL",
            "description": "URL shortener",
            "url": "https://tinyurl.com/app/dev",
            "auth": "apiKey",
            "https": True,
            "cors": "unknown",
            "popularity": 85,
            "status": "active"
        }
    ],
    "Video": [
        {
            "name": "YouTube",
            "description": "YouTube data API",
            "url": "https://developers.google.com/youtube/",
            "auth": "OAuth",
            "https": True,
            "cors": "yes",
            "popularity": 95,
            "status": "active"
        },
        {
            "name": "Vimeo",
            "description": "Vimeo API",
            "url": "https://developer.vimeo.com/",
            "auth": "OAuth",
            "https": True,
            "cors": "yes",
            "popularity": 88,
            "status": "active"
        }
    ]
}


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


def populate_categories() -> None:
    """Populate all categories with sample APIs."""
    # Load current API data
    data = load_api_data()
    
    # Track how many APIs were added
    apis_added = 0
    
    # For each category in the data
    for category in data["categories"]:
        category_name = category["name"]
        
        # Skip if category already has APIs
        if len(category["apis"]) > 0:
            print(f"Category '{category_name}' already has {len(category['apis'])} APIs. Skipping.")
            continue
        
        # Check if we have sample APIs for this category
        if category_name in SAMPLE_APIS:
            # Add sample APIs to the category
            for api in SAMPLE_APIS[category_name]:
                # Add last_checked field if not present
                if "last_checked" not in api:
                    api["last_checked"] = datetime.datetime.now().isoformat()
                
                category["apis"].append(api)
                apis_added += 1
            
            print(f"Added {len(SAMPLE_APIS[category_name])} APIs to category '{category_name}'")
        else:
            print(f"No sample APIs available for category '{category_name}'")
    
    # Update metadata
    data["metadata"]["total_apis"] += apis_added
    data["metadata"]["last_updated"] = datetime.datetime.now().isoformat()
    
    # Save updated data
    save_api_data(data)
    print(f"Total APIs added: {apis_added}")


if __name__ == "__main__":
    populate_categories()
