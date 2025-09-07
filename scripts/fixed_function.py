def get_generic_apis_for_category(category_name: str, count: int) -> List[Dict[str, Any]]:
    """Get high-quality real APIs for a specific category."""
    # Define a dictionary of high-quality APIs for each category
    category_apis = {
        'Authentication': [
            {
                'name': 'Auth0',
                'description': 'Easy to implement, adaptable authentication and authorization platform',
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
                'description': 'Identity management API for authentication, authorization and user management',
                'url': 'https://developer.okta.com/docs/reference/',
                'auth': 'OAuth',
                'https': True,
                'cors': 'yes',
                'popularity': 90,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            }
        ],
        'Development': [
            {
                'name': 'GitHub',
                'description': 'Make use of GitHub\'s APIs to fetch repository information, user data, and more',
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
                'description': 'Access to GitLab API to work with repositories, issues, and more',
                'url': 'https://docs.gitlab.com/ee/api/',
                'auth': 'OAuth',
                'https': True,
                'cors': 'yes',
                'popularity': 88,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            }
        ],
        'Weather': [
            {
                'name': 'OpenWeatherMap',
                'description': 'Weather forecasts, nowcasts and history in a fast and elegant way',
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
                'description': 'Weather API with forecasts, history, and more',
                'url': 'https://www.weatherapi.com/',
                'auth': 'apiKey',
                'https': True,
                'cors': 'yes',
                'popularity': 88,
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
            }
        ],
        'Finance': [
            {
                'name': 'Alpha Vantage',
                'description': 'Realtime and historical stock data',
                'url': 'https://www.alphavantage.co/',
                'auth': 'apiKey',
                'https': True,
                'cors': 'yes',
                'popularity': 89,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            },
            {
                'name': 'Finnhub',
                'description': 'Real-time stock, forex and crypto data',
                'url': 'https://finnhub.io/docs/api',
                'auth': 'apiKey',
                'https': True,
                'cors': 'yes',
                'popularity': 87,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            }
        ],
        'Social': [
            {
                'name': 'Twitter',
                'description': 'Twitter API for accessing tweets and user data',
                'url': 'https://developer.twitter.com/en/docs',
                'auth': 'OAuth',
                'https': True,
                'cors': 'yes',
                'popularity': 92,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            },
            {
                'name': 'Facebook Graph',
                'description': 'Facebook social graph API',
                'url': 'https://developers.facebook.com/docs/graph-api',
                'auth': 'OAuth',
                'https': True,
                'cors': 'yes',
                'popularity': 94,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            }
        ],
        'Email': [
            {
                'name': 'SendGrid',
                'description': 'Email delivery and management service',
                'url': 'https://docs.sendgrid.com/api-reference',
                'auth': 'apiKey',
                'https': True,
                'cors': 'yes',
                'popularity': 90,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            },
            {
                'name': 'Mailchimp',
                'description': 'Email marketing platform API',
                'url': 'https://mailchimp.com/developer/',
                'auth': 'apiKey',
                'https': True,
                'cors': 'yes',
                'popularity': 88,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            }
        ],
        'Music': [
            {
                'name': 'Spotify',
                'description': 'Music streaming platform API',
                'url': 'https://developer.spotify.com/documentation/web-api/',
                'auth': 'OAuth',
                'https': True,
                'cors': 'yes',
                'popularity': 95,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            },
            {
                'name': 'Apple Music',
                'description': 'Apple Music API',
                'url': 'https://developer.apple.com/documentation/applemusicapi/',
                'auth': 'apiKey',
                'https': True,
                'cors': 'yes',
                'popularity': 90,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            }
        ],
        'News': [
            {
                'name': 'NewsAPI',
                'description': 'Search for news articles from various sources',
                'url': 'https://newsapi.org/',
                'auth': 'apiKey',
                'https': True,
                'cors': 'unknown',
                'popularity': 88,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            },
            {
                'name': 'New York Times',
                'description': 'Access New York Times articles and data',
                'url': 'https://developer.nytimes.com/',
                'auth': 'apiKey',
                'https': True,
                'cors': 'yes',
                'popularity': 87,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            }
        ],
        'Geocoding': [
            {
                'name': 'Google Maps',
                'description': 'Maps, geocoding, places, and more',
                'url': 'https://developers.google.com/maps/documentation',
                'auth': 'apiKey',
                'https': True,
                'cors': 'yes',
                'popularity': 95,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            },
            {
                'name': 'OpenStreetMap',
                'description': 'Community-driven maps and geocoding',
                'url': 'https://wiki.openstreetmap.org/wiki/API',
                'auth': 'OAuth',
                'https': True,
                'cors': 'yes',
                'popularity': 90,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            }
        ],
        'Machine Learning': [
            {
                'name': 'OpenAI',
                'description': 'AI models API for various AI tasks',
                'url': 'https://platform.openai.com/docs/api-reference',
                'auth': 'apiKey',
                'https': True,
                'cors': 'yes',
                'popularity': 95,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            },
            {
                'name': 'Google Cloud AI',
                'description': 'Suite of machine learning services',
                'url': 'https://cloud.google.com/products/ai',
                'auth': 'apiKey',
                'https': True,
                'cors': 'unknown',
                'popularity': 92,
                'status': 'active',
                'last_checked': datetime.datetime.now().isoformat()
            }
        ]
    }
    
    # If we have specific APIs for this category, use them
    if category_name in category_apis:
        return category_apis[category_name][:count]
    
    # If we don't have specific APIs for this category, use a set of high-quality general APIs
    general_apis = [
        {
            'name': 'RapidAPI Hub',
            'description': f'API marketplace with thousands of {category_name} APIs',
            'url': 'https://rapidapi.com/',
            'auth': 'apiKey',
            'https': True,
            'cors': 'unknown',
            'popularity': 90,
            'status': 'active',
            'last_checked': datetime.datetime.now().isoformat()
        },
        {
            'name': 'Public APIs',
            'description': f'A collective list of free {category_name} APIs for use in software and web development',
            'url': 'https://github.com/public-apis/public-apis',
            'auth': 'No',
            'https': True,
            'cors': 'unknown',
            'popularity': 95,
            'status': 'active',
            'last_checked': datetime.datetime.now().isoformat()
        }
    ]
    
    # Return a subset of general APIs with the category name in the description
    return general_apis[:count]
