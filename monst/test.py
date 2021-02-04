import requests
from bs4 import BeautifulSoup

r = requests.get('https://monst.appbank.net/monster/1.html')
r.encoding = r.apparent_encoding
soup = BeautifulSoup(r.text, "html.parser")
found_rows = soup.select('.monster-sp-status')
# found_list = []

# for item in found_rows:
#    list(found_rows.append(item.text[0:]))


# print(item.stripped_strings)

# found = soup.select('body > div > div.monster-container > div.monster-sp-status > div.status-table')
# print(found)


print(list(found_rows.stripped_strings))
