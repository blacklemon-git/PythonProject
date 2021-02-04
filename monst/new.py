# -*- coding: utf-8 -*-
import csv
import bs4

soup = bs4.BeautifulSoup(open('./download/appbanknet1.html', encoding = 'utf-8'), 'lxml')
soup.encoding = soup.apparent_encoding

# print(soup)

monster_number = soup.select('body > div > div.monster-container > div.monster-sp-status > div.status-table > table > tbody > tr:nth-child(1) > td:nth-child(2) > a')
monster_number = [monster_number.get_text() for monster_number in monster_number]
print(monster_number)