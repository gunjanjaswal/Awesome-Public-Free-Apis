#!/usr/bin/env python3
"""
Update README with APIs

This script reads the APIs data file and updates the README.md file with APIs by category.
"""

import os
import json
import re
import datetime
import hashlib
from typing import Dict, List, Any

def generate_anchor_id(category_name: str) -> str:
    """Generate a consistent anchor ID from a category name."""
    # Convert to lowercase and replace spaces, ampersands, and underscores
    return category_name.lower().replace(' ', '-').replace('&', '').replace('_', '')

# Constants
README_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md')
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'apis.json')

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
            print(f"Data file {DATA_FILE} not found")
            return {"categories": [], "metadata": {"total_apis": 0}}
    except Exception as e:
        print(f"Error loading API data: {e}")
        return {"categories": [], "metadata": {"total_apis": 0}}

def update_readme_with_apis() -> None:
    """Update the README.md file with APIs from the data file."""
    try:
        # Load API data
        data = load_api_data()
        
        # Load README template to ensure proper section ordering
        template_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates', 'README_template.md')
        
        # Check if template exists, if not, use current README as template
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as file:
                template_content = file.read()
            print("Using README template for structured section ordering")
        else:
            # If template doesn't exist, use current README but ensure proper section ordering
            with open(README_FILE, 'r', encoding='utf-8') as file:
                template_content = file.read()
            print("Template not found, using current README as template")
        
        # Find the API categories section markers in the template
        api_categories_start = "<!-- BEGIN API CATEGORIES SECTION - DO NOT REMOVE OR MODIFY THIS COMMENT -->"
        api_categories_end = "<!-- END API CATEGORIES SECTION - DO NOT REMOVE OR MODIFY THIS COMMENT -->"
        
        # Check if the template has the API categories section markers
        if api_categories_start not in template_content or api_categories_end not in template_content:
            print("API categories section markers not found in template")
            # Load current README as fallback
            with open(README_FILE, 'r', encoding='utf-8') as file:
                readme_content = file.read()
                
            # Extract parts before and after API categories section
            if api_categories_start in readme_content and api_categories_end in readme_content:
                content_before = readme_content.split(api_categories_start)[0] + api_categories_start + "\n"
                content_after = api_categories_end + readme_content.split(api_categories_end)[1]
            else:
                print("API categories section markers not found in README.md")
                content_before = readme_content
                content_after = ""
        else:
            # Extract parts from template to ensure proper section ordering
            content_before = template_content.split(api_categories_start)[0] + api_categories_start + "\n"
            content_after = api_categories_end + template_content.split(api_categories_end)[1]
            
            # Preserve existing trending repositories content from current README
            with open(README_FILE, 'r', encoding='utf-8') as file:
                current_readme = file.read()
                
            # Find trending repositories sections in current README
            trending_repos_pattern = r'(## :rocket: Trending GitHub Repositories.*?)(?=^## |\Z)'
            trending_api_repos_pattern = r'(## :rocket: Trending GitHub API Repositories.*?)(?=^## |\Z)'
            
            trending_repos_match = re.search(trending_repos_pattern, current_readme, re.DOTALL | re.MULTILINE)
            trending_api_repos_match = re.search(trending_api_repos_pattern, current_readme, re.DOTALL | re.MULTILINE)
            
            # Replace placeholder content in template with actual content from current README
            if trending_repos_match:
                content_after = re.sub(trending_repos_pattern, trending_repos_match.group(0), content_after, flags=re.DOTALL | re.MULTILINE)
                
            if trending_api_repos_match:
                content_after = re.sub(trending_api_repos_pattern, trending_api_repos_match.group(0), content_after, flags=re.DOTALL | re.MULTILINE)
        
        # Sort categories alphabetically
        data['categories'].sort(key=lambda x: x['name'])
        
        # Generate the updated categories content
        updated_categories_content = "## :card_index: API Categories - Find the Perfect API for Your Project\n\n\n**Available Categories:**\n\n"
        
        # Add category emojis for the table of contents
        category_emojis = {
            'Authentication': ':closed_lock_with_key:', 'Blockchain': ':link:', 'Business': ':briefcase:',
            'Calendar': ':calendar:', 'Cloud Storage': ':floppy_disk:', 'Communication': ':speech_balloon:',
            'Cryptocurrency': ':moneybag:', 'Currency Exchange': ':currency_exchange:', 'Data Validation': ':white_check_mark:',
            'Development': ':man_technologist:', 'Email': ':email:', 'Entertainment': ':performing_arts:',
            'Environment': ':earth_africa:', 'Finance': ':dollar:', 'Food & Drink': ':fork_and_knife:',
            'Games & Comics': ':video_game:', 'Geocoding': ':world_map:', 'Government': ':classical_building:',
            'Health': ':syringe:', 'Jobs': ':briefcase:', 'Machine Learning': ':robot:',
            'Music': ':musical_note:', 'News': ':newspaper:', 'Open Data': ':notebook:',
            'Open Source Projects': ':man_technologist:', 'Patent': ':page_facing_up:', 'Personality': ':sunglasses:',
            'Phone': ':iphone:', 'Photography': ':camera:', 'Science & Math': ':microscope:',
            'Security': ':lock:', 'Shopping': ':shopping:', 'Social': ':busts_in_silhouette:',
            'Sports & Fitness': ':soccer:', 'Test Data': ':card_index:', 'Text Analysis': ':mag:',
            'Tracking': ':round_pushpin:', 'Transportation': ':bus:', 'URL Shorteners': ':paperclip:',
            'Video': ':movie_camera:', 'Weather': ':partly_sunny:'
        }
        
        # Add categories to the table of contents
        for category in data['categories']:
            category_name = category['name']
            category_id = generate_anchor_id(category_name)
            emoji = category_emojis.get(category_name, ':100:')
            updated_categories_content += f"- [{emoji} {category_name}](#{category_id})\n"
        
        updated_categories_content += "\n\n"
        
        # Add a colorful divider
        colorful_divider = '<div align="center"><hr style="height:2px;border-width:0;color:rainbow;background-color:rainbow"></div>\n\n'
        
        # Add each category section with its APIs
        for category in data['categories']:
            category_name = category['name']
            
            if not category['apis']:
                # Add witty placeholder for empty categories
                witty_messages = [
                    "🔍 APIs for this category are playing hide and seek. Check back soon!",
                    "⏳ APIs loading... Estimated time of arrival: sooner than you think!",
                    "🧙‍♂️ Our API wizards are brewing something special for this category.",
                    "🚀 APIs for this section are currently in orbit. Landing soon!",
                    "🔮 The crystal ball says APIs will appear here in the near future.",
                    "🏗️ Under construction! We're building something awesome here.",
                    "🌱 This category is freshly planted. APIs will sprout soon!",
                    "📡 Scanning the digital universe for the best APIs in this category...",
                    "🎁 APIs for this category are being wrapped. Surprise coming soon!",
                    "🧩 The final pieces of this API puzzle are being assembled.",
                    "🔭 Our API astronomers are searching the stars for this category.",
                    "🧪 API scientists are in the lab cooking up something amazing!",
                    "🎭 The APIs for this category are still rehearsing their grand entrance.",
                    "🌊 The tide of APIs for this category is coming in soon!",
                    "🎯 Our API hunters are tracking down the perfect matches for this category.",
                    "🧠 The AI is thinking really hard about which APIs belong here.",
                    "🎨 Painting a masterpiece of APIs for this category... please wait!",
                    "🧬 The DNA of this category's APIs is still being sequenced.",
                    "🎲 Rolling the dice to find the perfect APIs for this category.",
                    "🧙‍♀️ Magical APIs are being summoned for this category.",
                    "🏄‍♂️ Surfing the web for the coolest APIs to add here!",
                    "🧶 Knitting together a cozy collection of APIs for this category.",
                    "🌋 Volcanic APIs are brewing beneath the surface. Eruption imminent!",
                    "🌈 Somewhere over the rainbow, there are APIs for this category.",
                    "🧩 The API puzzle pieces for this category are still being collected.",
                    "🧁 Baking a batch of fresh APIs for this category. Smells delicious!",
                    "🎣 Fishing for the finest APIs to add to this category.",
                    "🧪 The API potion for this category is still brewing in our cauldron.",
                    "🎪 The API circus for this category is setting up the big tent!",
                    "🔋 Charging up the batteries for this category's API showcase."
                ]
                
                # Use category name to consistently select the same message for the same category
                hash_value = int(hashlib.md5(category_name.encode()).hexdigest(), 16)
                selected_message = witty_messages[hash_value % len(witty_messages)]
                
                # Add emoji to category name based on category
                category_emojis_unicode = {
                    'Authentication': '🔐', 'Blockchain': '🔗', 'Business': '💼',
                    'Calendar': '📅', 'Cloud Storage': '💾', 'Communication': '💬',
                    'Cryptocurrency': '💰', 'Currency Exchange': '💱', 'Data Validation': '✅',
                    'Development': '👨‍💻', 'Email': '📧', 'Entertainment': '🎭',
                    'Environment': '🌍', 'Finance': '💵', 'Food & Drink': '🍽️',
                    'Games & Comics': '🎮', 'Geocoding': '🗺️', 'Government': '🏛️',
                    'Health': '💉', 'Jobs': '💼', 'Machine Learning': '🤖',
                    'Music': '🎵', 'News': '📰', 'Open Data': '📓',
                    'Open Source Projects': '👨‍💻', 'Patent': '📄', 'Personality': '😎',
                    'Phone': '📱', 'Photography': '📸', 'Science & Math': '🔬',
                    'Security': '🔒', 'Shopping': '🛍️', 'Social': '👥',
                    'Sports & Fitness': '⚽', 'Test Data': '📋', 'Text Analysis': '🔍',
                    'Tracking': '📍', 'Transportation': '🚌', 'URL Shorteners': '🖇️',
                    'Video': '🎥', 'Weather': '⛅'
                }
                
                # Get emoji for category or use a default
                category_emoji = category_emojis_unicode.get(category_name, '💯')
                
                # Add the category section with explicit HTML ID for reliable anchor links
                category_id = generate_anchor_id(category_name)
                updated_categories_content += f"<a id=\"{category_id}\"></a>\n### {category_emoji} {category_name}\n{category.get('description', f'APIs for {category_name.lower()} related services.')}\n\n{selected_message}\n\n{colorful_divider}"
                continue
            
            # Create the API table for this category with enhanced styling
            api_table = "| 🔌 API | 📝 Description | 🔑 Auth | 🔒 HTTPS | 🌐 CORS |\n"
            api_table += "| :--- | :--- | :---: | :---: | :---: |\n"
            
            # Add each API to the table (limit to 100 APIs per category)
            api_limit = 100
            limited_apis = category['apis'][:api_limit]
            
            for api in limited_apis:
                name = api.get('name', '')
                url = api.get('url', '')
                description = api.get('description', '')
                auth = api.get('auth', 'unknown')
                https = 'Yes' if api.get('https', False) else 'No'
                cors = api.get('cors', 'unknown')
                
                # Format the API row with HTML links that have target="_blank"
                if url:
                    link = f"<a href=\"{url}\" target=\"_blank\">{name}</a>"
                else:
                    link = name
                api_table += f"| {link} | {description} | {auth} | {https} | {cors} |\n"
            
            # Add emoji to category name based on category
            category_emojis_unicode = {
                'Authentication': '🔐', 'Blockchain': '🔗', 'Business': '💼',
                'Calendar': '📅', 'Cloud Storage': '💾', 'Communication': '💬',
                'Cryptocurrency': '💰', 'Currency Exchange': '💱', 'Data Validation': '✅',
                'Development': '👨‍💻', 'Email': '📧', 'Entertainment': '🎭',
                'Environment': '🌍', 'Finance': '💵', 'Food & Drink': '🍽️',
                'Games & Comics': '🎮', 'Geocoding': '🗺️', 'Government': '🏛️',
                'Health': '💉', 'Jobs': '💼', 'Machine Learning': '🤖',
                'Music': '🎵', 'News': '📰', 'Open Data': '📓',
                'Open Source Projects': '👨‍💻', 'Patent': '📄', 'Personality': '😎',
                'Phone': '📱', 'Photography': '📸', 'Science & Math': '🔬',
                'Security': '🔒', 'Shopping': '🛍️', 'Social': '👥',
                'Sports & Fitness': '⚽', 'Test Data': '📋', 'Text Analysis': '🔍',
                'Tracking': '📍', 'Transportation': '🚌', 'URL Shorteners': '🖇️',
                'Video': '🎥', 'Weather': '⛅'
            }
            
            # Get emoji for category or use a default
            category_emoji = category_emojis_unicode.get(category_name, '💯')
            
            # Add styled category header with emoji and count badge
            api_count = len(category['apis'])
            display_count = min(api_count, 100)  # Limit displayed count to 100
            badge = f"![{display_count} APIs](https://img.shields.io/badge/{display_count}-APIs-brightgreen)"
            category_id = generate_anchor_id(category_name)
            
            # Add the category section with explicit HTML ID for reliable anchor links
            category_description = category.get('description', f'APIs for {category_name.lower()} related services.')
            
            # Add a note about API limit when there are more than 100 APIs
            if api_count > 100:
                api_limit_note = f"*Note: Showing 100 of {api_count} APIs in this category.*\n\n"
                updated_categories_content += f"<a id=\"{category_id}\"></a>\n### {category_emoji} {category_name} {badge}\n{category_description}\n\n{api_limit_note}{api_table}\n\n{colorful_divider}"
            else:
                updated_categories_content += f"<a id=\"{category_id}\"></a>\n### {category_emoji} {category_name} {badge}\n{category_description}\n\n{api_table}\n\n{colorful_divider}"
            print(f"Added category section for {category_name} with {len(limited_apis)} APIs (out of {api_count} total)")
        
        # Add a 'Last updated' date and update schedules after the API categories section
        today = datetime.datetime.now().strftime('%B %d, %Y')
        
        # Calculate the next update dates
        now = datetime.datetime.now()
        
        # Next Sunday for Weekly API Status Checks
        days_until_sunday = (6 - now.weekday()) % 7
        if days_until_sunday == 0:
            days_until_sunday = 7  # If today is Sunday, get next Sunday
        next_sunday = now + datetime.timedelta(days=days_until_sunday)
        next_sunday_str = next_sunday.strftime('%B %d, %Y')
        
        # Next Monday for Enhanced API Discovery
        days_until_monday = (0 - now.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7  # If today is Monday, get next Monday
        next_monday = now + datetime.timedelta(days=days_until_monday)
        next_monday_str = next_monday.strftime('%B %d, %Y')
        
        # Next 1st of month for Monthly API Discovery
        if now.day == 1:
            # If today is the 1st, get 1st of next month
            next_month = now.replace(day=28) + datetime.timedelta(days=4)  # Move to next month
            next_first = next_month.replace(day=1)
        else:
            # Get 1st of next month
            if now.month == 12:
                next_first = now.replace(year=now.year + 1, month=1, day=1)
            else:
                next_first = now.replace(month=now.month + 1, day=1)
        next_first_str = next_first.strftime('%B %d, %Y')
        
        update_info = f"""_API Categories last updated: {today}_

**API Update Schedule:**
- Weekly API Status Checks (Next: {next_sunday_str})
- Enhanced API Discovery (Next: {next_monday_str})
- Monthly API Discovery (Next: {next_first_str})

"""        
        updated_categories_content += update_info
        
        # Combine all parts to create the updated README content
        updated_readme_content = content_before + updated_categories_content + content_after
        
        # Update the README file with the new content
        with open(README_FILE, 'w', encoding='utf-8') as file:
            file.write(updated_readme_content)
        print(f"README.md has been successfully updated with {len(data['categories'])} categories.")
    except Exception as e:
        print(f"Error updating README with APIs: {e}")
        raise

def main():
    """Main function to update README with APIs."""
    print("Starting README update with APIs...")
    try:
        update_readme_with_apis()
        print("README update completed.")
    except Exception as e:
        print(f"Error in main function: {e}")
        exit(1)

if __name__ == "__main__":
    main()
