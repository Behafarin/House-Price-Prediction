import mysql.connector
import re
from bs4 import BeautifulSoup
import requests


def save_to_table(location, area, room, price):
    cnx = mysql.connector.connect(user='behafarin', password='127281', host='localhost'
                                  , database='shabesh', charset='utf8', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = 'insert into Tehran (location, area, room, price) values(%s, %s, %s, %s)'
    val = (location.encode('utf-8'), area, room, price)
    # print(type(location), type(area), type(room), type(price))
    # print(query)
    # print(val)
    cursor.execute(query, val)
    cnx.commit()
    cnx.close()

page = 0
while page < 250:
    page += 1
    r = requests.get('https://shabesh.com/search/خرید-فروش/آپارتمان/تهران/' + str(page))
    print(r)
    soup = BeautifulSoup(r.text, 'html.parser')
    elements = soup.find_all('div', attrs={'class': 'announce-list-mode mt-2 col-12'})
    for element in elements:
        price = element.find('span', attrs={'class': 'info-item info-price d-block'})
        if price and 'تومان' in price.text:
            p = re.sub(r'\,', '', price.text)
            p = re.findall(r'\d+', p)
            location = element.find('span', attrs={'class': 'info-item ellipsis d-block'})
            loc = location.text.replace('تهران','')
            detail = element.find('div', attrs={'class': 'info-item d-flex info-specs'})
            room = re.findall(r'(\d+) خواب', detail.text)
            area = re.findall(r'(\d+) متر', detail.text)
            if room:
                save_to_table(loc, int(area[0]), int(room[0]), int(p[0]))
            else:
                save_to_table(loc, int(area[0]), 0, int(p[0]))