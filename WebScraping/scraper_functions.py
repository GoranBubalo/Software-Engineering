import requests
from bs4 import BeautifulSoup

# Getting details 
def scrape_dom_details(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        nursing_home_details = {}
        nursing_home_details['URL'] = url