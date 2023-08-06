'''
Plugin which searches query using Google and Stackoverflow
'''
import re
import requests
from bs4 import BeautifulSoup

from howcani.plugins import Plugin

# Used for registering with howcani module
TYPE_STACKOVERFLOW="stackoverflow"

# Constants used while performing search
NUMBER_OF_GOOGLE_LINKS = 1
NUMBER_OF_ANSWERS_PER_LINK = 1

GOOGLE_SEARCH = "https://www.google.com/search"
STACKOVERFLOW = "stackoverflow.com"

class StackOverflowPlugin(Plugin):

    @staticmethod
    def fetch_links_from_google(query):
        params = {"q":query, "as_sitesearch": STACKOVERFLOW }
        page = requests.get(GOOGLE_SEARCH, params=params)
        soup = BeautifulSoup(page.text, 'html.parser')
        links = soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)"))

        results = []
        for link in links:
            url = re.split(":(?=http)",link["href"].replace("/url?q=",""))[0]
            if TYPE_STACKOVERFLOW.lower() in url.lower():
                results.append(url)
        return results[:NUMBER_OF_GOOGLE_LINKS]
        

    @staticmethod
    def fetch_answers_from_stackoverflow(link):
        results = []

        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')

        answer_cells = soup.findAll("div", {"class": "answercell"})
        
        for answer in answer_cells:
            message = answer.find("div", {"class": "js-post-body"})
            results.append(message.text)
        
        return results[:NUMBER_OF_ANSWERS_PER_LINK]

    def _get_results(self, query, n=1):
        answers = []
        
        # Fetch all google links
        links = StackOverflowPlugin.fetch_links_from_google(query=query)

        for link in links:
            answers += StackOverflowPlugin.fetch_answers_from_stackoverflow(link)

        return answers[:n]


# if __name__ == "__main__":
#     stack = StackOverflowPlugin()
#     print(stack.get_results(query="how to upgrade pip"))