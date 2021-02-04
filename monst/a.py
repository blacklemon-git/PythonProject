# -*- coding: utf-8 -*-
import csv
import requests
from time import sleep
from bs4 import BeautifulSoup as bs4
import re
import urllib, http.cookiejar


# ページ数(キャラ数)(本番環境)
pages = 5300
# 待機時間
bt = 0.5


for i in range(5000,5100):

    sleep(bt)

    res = requests.get('https://monst.appbank.net/monster/' + str(i) + '.html')
    res.encoding = res.apparent_encoding
    res.raise_for_status()
    soup = bs4(res.content, 'lxml')

    monster_number = soup.select('body > div > div.monster-container > div.monster-detail > div.monster-mobiledetail > p')
    monster_number = [monster_number.get_text() for monster_number in monster_number]
    monster_name = soup.select('body > div > div.monster-container > div.monster-detail > div.monster-mobiledetail > div.monster-name')
    monster_name = [monster_name.get_text() for monster_name in monster_name]

    # レア度

    # found = soup.select('body > div > div.monster-container > div.monster-sp-status > div.status-table > table > tbody > tr:nth-child(1) > td:nth-child(2) > a')
    # print(found)


    monster_rarity = soup.select('body > div > div.monster-container > div.monster-sp-status > div.status-table > table > tbody > tr:nth-child(1) > td:nth-child(2)')
    monster_rarity = [monster_rarity.get_text() for monster_rarity in monster_rarity]


    # 属性
    monster_attribute = soup.select('body > div > div.monster-container > div.monster-sp-status > div.status-table > table > tbody > tr:nth-child(2) > td:nth-child(2)')
    # monster_attribute = [monsterinfo_attribute.text for monsterinfo_attribute in monster_attribute]

    monster_family = soup.select('body > div > div.monster-container > div.monster-detail > div.monster-pcdetail > div.monster-title > div.monster-substatus > p.species')
    monster_battle_type = soup.select('body > div > div.monster-container > div.monster-detail > div.monster-pcdetail > div.monster-title > div.monster-substatus > p:nth-child(3)')

    monster_family = [monsterinfo_family.get_text() for monsterinfo_family in monster_family]
    # monster_battle_type = [monsterinfo._attle_type.text for monsterinfo_battle_type in monster_battle_type]

    # 撃種判定(4パターン)
    # https://img-monst.appbank.net/images/attacktype/attacktype_0.png  反射
    # https://img-monst.appbank.net/images/attacktype/gaugeattacktype_0.png 反射＆ゲージ
    # https://img-monst.appbank.net/images/attacktype/attacktype_1.png  貫通
    # https://img-monst.appbank.net/images/attacktype/gaugeattacktype_1.png 貫通＆ゲージ

    monster_type_of_attack = soup.select('body > div > div.monster-container > div.monster-detail > div.monster-pcdetail > div.monster-title > div.monster-substatus > img')

    for img in monster_type_of_attack:

        if 'https://img-monst.appbank.net/images/attacktype/attacktype_0.png' == img['data-original']:
            monster_type_of_attack = '反射'
            # print('反射')
        elif 'https://img-monst.appbank.net/images/attacktype/gaugeattacktype_0.png' == img['data-original']:
            monster_type_of_attack = '反射＆ゲージ'
            # print('反射＆ゲージ')
        elif 'https://img-monst.appbank.net/images/attacktype/attacktype_1.png' == img['data-original']:
            monster_type_of_attack = '貫通'
            # print('貫通')
        elif 'https://img-monst.appbank.net/images/attacktype/gaugeattacktype_1.png' == img['data-original']:
            monster_type_of_attack = '貫通＆ゲージ'
            # print('貫通＆ゲージ')
        else:
            monster_type_of_attack = 'その他'
            # print('その他')

    monster_ability = soup.select('body > div > div.monster-container > div.monster-detail > div.monster-pcdetail > div.pcdetail > div > div.monster-status')

    if not monster_ability:
        monster_ability = soup.select('body > div > div.monster-container > div.monster-detail > div.monster-pcdetail > div.pcdetail > div > div.monster-status-many')

    # monsterinfo.ability = [monsterinfo.ability.text for monsterinfo.ability in monster_ability]

    # データセット
    # dataList = [monsterinfo.number, monsterinfo.name, monsterinfo.rarity, monsterinfo.attribute,
    # monsterinfo.family, monsterinfo.battle_type, monsterinfo.type_of_attack,
    # monsterinfo.ability]

    dataList = [monster_number, monster_name, monster_rarity]


    # CSV書き込み
    with open('test.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(dataList)
