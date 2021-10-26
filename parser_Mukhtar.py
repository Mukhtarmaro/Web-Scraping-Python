import requests
from bs4 import BeautifulSoup
import pprint as pp
import pandas as pd


def get_soup(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'lxml')
    else:
        raise Exception('Request error!')


def get_items(soup):
    container = soup.find('table', class_='itemlist')
    items = container.find_all('tr', class_='athing')
    # points = container.find_all('tr',class_='score')
    ml = list()

    for item in items:
        md = dict()
        extras = item.find_next_sibling('tr')
        # print(extras)
        item1 = item.find('a', class_='titlelink')
        item2 = item.find('span', class_='sitestr')
        points = extras.find('span', class_='score')
        time = extras.find('span', class_='age')
        comments = extras.find_all('a')[-1]
        if item1:
            md['title'] = item1.text
        if item2:
            md['site'] = item2.text
        if item1.has_attr('href'):
            md['url'] = item1['href']
        if points:
            md['points'] = points.text
        if time.has_attr('title'):
            md['time'] = time['title']
        if comments:
            md['comments'] = comments.text.replace('\xa0', ' ')
        ml.append(md)
        # print(item1_text)
        # print(item2_text)

    return ml


def main():
    items_main = list()
    for i in range(1, 23):
        soup = get_soup(f'https://news.ycombinator.com/news?p={i}')
        items = get_items(soup)
        items_main.extend(items)
    df = pd.DataFrame(items_main)
    df.to_excel('data.xlsx', index=False)


# print(soup)

main()
