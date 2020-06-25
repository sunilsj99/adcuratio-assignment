import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


class Scrapper:
    def __init__(self, url="", dbCon=""):
        self.url = url
        self.dbCon = dbCon
        self.R1 = []
        self.R2 = []

    def mongoCon(self):
        client = MongoClient(self.dbCon)
        db = client['scrapped_data']
        r1 = db.url_heading_relation
        r1.insert_many(self.R1)
        r2 = db.url_metadata_relation
        r2.insert_many(self.R2)
        print('Database insertion completed !!')

    def scrapper(self):
        print('Getting the Webpage...')
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        res = soup.find_all('tr', class_='athing')
        print('Scrapping started...')
        for i in res:
            a = i
            b = i.find_next_sibling('tr')

            d = {}
            d['link'] = a.find("a", class_='storylink').get('href')
            d['heading'] = a.find("a", class_='storylink').text
            self.R1.append(d)

            d = {}
            d['link'] = a.find("a", class_='storylink').get('href') if a.find(
                "a", class_='storylink') is not None else 'None'
            d['Title'] = a.find("a", class_='storylink').text if a.find(
                "a", class_='storylink') is not None else 'None'
            d['Votes'] = b.find("span", class_='score').text if b.find(
                "span", class_='score') is not None else 'None'
            d['Author'] = b.find("a", class_='hnuser').text if b.find(
                "a", class_='hnuser') is not None else 'None'
            self.R2.append(d)
            print('.', end='')
        print('')
        print('data scrapping completed !!')


url = 'https://news.ycombinator.com/'
dbCon = 'mongodb://localhost:27017'

s = Scrapper(url, dbCon)

s.scrapper()

s.mongoCon()
