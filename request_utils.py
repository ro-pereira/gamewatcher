import requests
from bs4 import BeautifulSoup

def request_page_content(initialUrl):
    response = requests.get(initialUrl)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    else:
        print(f"Error occurred. Status code: {response.status_code}")