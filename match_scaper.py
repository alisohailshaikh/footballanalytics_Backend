import requests
from bs4 import BeautifulSoup
import datetime

class MatchIDFinder:

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.headers['If-Modified-Since'] = datetime.datetime.now().isoformat()
        

    def find_match_id(self,search_query):
        search_results = None
        while search_results is None:
            search_url = f"https://www.bing.com/search?q={search_query}"
            response = requests.get(search_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            search_results = soup.find('li', class_='b_algo')
        i=0
        for search_result in search_results:
            if (i==0):
                match_url= search_result.find('a')['href']
                i=i+1  
            print(match_url)
        i=0

        match_response = requests.get(match_url, headers=self.headers)
        match_soup = BeautifulSoup(match_response.text, 'html.parser')
        links = match_soup.find_all('link', href=True)
        for link in links:
            href = link['href']
            print(href)
            if 'android-app://com.sofascore.results/https/www.sofascore.com/event/' in href:
                last_part = href.split('/')[-1]
                return last_part

        return None


