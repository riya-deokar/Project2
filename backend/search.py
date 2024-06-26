import wikipedia
import requests
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Retrieve the NYT API key from the environment
NYT_API_KEY = os.getenv('NYT_API_KEY')
NYT_BASE_URL = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'

def search_wikipedia(keyword):
    try:
        search_results = wikipedia.search(keyword)
        if search_results:
            page = wikipedia.page(search_results[0], auto_suggest=False)
            return page.url
        else:
            return None
    except wikipedia.exceptions.DisambiguationError as e:
        try:
            page = wikipedia.page(e.options[0], auto_suggest=False)
            return page.url
        except Exception as e:
            print(f"Error: {e}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def search_nytimes(keyword):
    params = {
        'q': keyword,
        'api-key': NYT_API_KEY
    }
    response = requests.get(NYT_BASE_URL, params=params)
    if response.status_code == 200:
        articles = response.json()['response']['docs']
        if articles:
            return articles[0]['web_url']
        else:
            return None
    else:
        print(f"Error: {response.status_code}")
        return None
