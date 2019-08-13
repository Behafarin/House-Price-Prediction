import mysql.connector
import re
from bs4 import BeautifulSoup
import requests


def save_to_table(location, area, room, price):
    cnx = mysql.connector.connect(user='behafarin', password='127281', host='localhost'
                                  , database='shabesh', charset='utf8')
    cursor = cnx.cursor()
    query = 'insert into Tehran (location, area, room, price) values(%s, %s, %s, %s)'
    val = (location.encode('utf-8'), area, room, price)
    print(type(location),type(area),type(room),type(price))
    print(query)
    print(val)
    cursor.execute(query, val)
    cnx.commit()
    cnx.close()


page = 0
while page < 250:
    page += 1
    r = requests.get('https://shabesh.com/search/خرید-فروش/آپارتمان/تهران/' + str(page))
    print(r)
    soup = BeautifulSoup(r.text, 'html.parser')
    elements = soup.find_all('div', attrs={'class': 'announce_info col-7 px-4'})
    for element in elements:
        price = element.find('span', attrs={'class': 'rent pb-2'})
        if price and 'تومان' in price.text:
            p = re.sub(r'\,', '', price.text)
            p = re.findall(r'\d+', p)
            print(p[0])
            location = element.find('h2', attrs={'class': 'announce-desc medium-sans pb-2'})
            loc = re.findall(r'در (.*) \،', location.text)
            print(loc[0])
            detail = element.find('ul', attrs={'class': 'clearfix'})
            room = re.findall(r'(\d+) خواب', detail.text)
            area = re.findall(r'(\d+) متر', detail.text)
            print(area[0])
            if room:
                print(room[0])
                save_to_table(loc[0], int(area[0]), int(room[0]), int(p[0]))
            else:
                save_to_table(loc[0], int(area[0]), 0, int(p[0]))