import requests
from bs4 import BeautifulSoup
import pandas as pd

# Globals
url = 'http://quotes.toscrape.com'
url_list = [url,]
pages = []
soup_list = []
not_last_page = True

#1: Pull the requests
def pullUrl(func):
    def inner(*args, **kwargs):
        page = requests.get(url_list[-1])
        if page.status_code == 200:
            pages.append(page)
            func(*args, **kwargs)
        else:
            print(f'The url {url} returned a status of {page.status_code}')
    return inner
    
#2: Make some soup
def makeSoup(func):
    def inner(*args, **kwargs):
        soup = BeautifulSoup(pages[-1].content, 'html.parser')
        soup_list.append(soup)
        func(*args, **kwargs)
    return inner
    
#3: Parse the URLs
@pullUrl
@makeSoup
def getURLs():
    global not_last_page
    try:
        next_page = url+soup_list[-1].find('li', {'class': 'next'}).find('a')['href']
        print(next_page)
        url_list.append(next_page)
    except:
        not_last_page = False

## Syntax and example output for page 1:
# next_page = url+soup.find('li', {'class': 'next'}).find('a')['href']
# print(next_page)

while not_last_page:
    getURLs()

# Start with an empty Data Frame:
quotes_df = pd.DataFrame(columns=['Author', 'Quote'])

# Add in the quotes dictionary:
quotes_dict = {}

try:
    for i in range(len(soup_list)):
        quotes = soup_list[i].find_all('div', {'class': 'quote'})
        for j in range(len(quotes)):
            v = quotes[j].find('small', {'class': 'author'}).text
            k = quotes[j].find('span', {'class': 'text'}).text
            quotes_dict[k] = v
except: print('issue with', {i, j})

quotes_df = pd.DataFrame(list(quotes_dict.items()), columns=['Quote', 'Author'])[['Author', 'Quote']].sort_values('Author')

print(quotes_df)