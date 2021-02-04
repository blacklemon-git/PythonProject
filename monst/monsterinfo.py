# -*- coding: utf-8 -*-
# BeautifulSoup4を使用したスクレイピング
import csv
import requests
import time
from bs4 import BeautifulSoup as bs4
import re
import urllib, http.cookiejar

# モンスター名前クラス
class MonsterInfo:
    def __init__(self):
        self.number = ''  # 図鑑No
        self.name = ''  # キャラクター名
        self.rarity = ''  # レア度
        self.attribute = ''  # 属性
        self.family = ''  # 種族
        self.battle_type = ''  #戦型
        self.type_of_attack = ''  # 撃種
        self.ability = ''  # アビリティ
        self.gauge_ability = ''  # ゲージアビリティ
        self.connect_skill = ''  # コネクトスキル
        self.connect_terms = ''  # コネクトスキル条件
        self.rack_skill = ''  # ラックスキル
        self.evolutionary_form = ''  # 進化形態
        self.max_level = ''  # 最大レベル
        self.hp = ''  # HP
        self.attack = ''  # 攻撃力
        self.gauge_attack = ''  # ゲージ成功時攻撃力
        self.speed = ''  # スピード
        self.tas_hp = ''  # タス値最大HP
        self.tas_attack = ''  # タス値最大攻撃力
        self.tas_gauge_attack = ''  # タス値最大ゲージ成功時攻撃力
        self.tas_speed = ''  # タス値最大スピード
        self.ss_name = ''  # ストライクショット名
        self.ss_turns = ''  # ストライクショットターン数
        self.ss_explanation = ''  # ストライクショット説明
        self.main_friendship_combo_name = ''  # メイン友情コンボ名
        self.main_friendship_combo_power = ''  # メイン友情コンボ威力
        self.main_friendship_combo_explanation = ''  # 副友情コンボ説明
        self.deputy_friendship_combo_name = ''  # 副友情コンボ名
        self.deputy_friendship_combo_power = ''  # 副友情コンボ威力
        self.deputy_friendship_combo_explanation = ''  # 副友情コンボ説明


# monst.appbank.net
def get_monstappbanknet(url):

    # ステータス情報のリンクのスクレイピング
    res2 = requests.get(url2)
    res2.encoding = res2.apparent_encoding
    res2.raise_for_status()
    soup2 = bs4(res2.content, 'lxml')

    monsterinfo = MonsterInfo()

    for i in range(1, 100):

        monster_number = soup.select('body > div > div:nth-child(6) > div:nth-child(5) > div > ul > li:nth-child(' + str(i) + ') > a > div')
        monster_name = soup.select('body > div > div:nth-child(6) > div:nth-child(5) > div > ul > li:nth-child(' + str(i) + ') > a > p')

        # 図鑑Noが空なら飛ばす
        if not monster_number:
            i = i + 1
            continue
        else:
            monsterinfo_number = [monsterinfo_number.text for monsterinfo_number in monster_number]
            monsterinfo_name = [monsterinfo_name.text for monsterinfo_name in monster_name]

            # キャラクター個別ページを取得
            # ページパターン
            monsterinfo_number = map(str, monsterinfo.number)
            monsterinfo_number = ','.join(monsterinfo_number)

            pattern = '.*?(\d+)'
            result =  re.match(pattern, monsterinfo_number)

            # レア度
            monster_rarity = soup2.select(body > div > div.monster-container > div.monster-detail > div.monster-pcdetail > div.monster-title > div.monster-name > p.rarity')

            monsterinfo_rarity = [monsterinfo_rariry.text for monsterinfo_rarity in monster_rarity]

            # 属性
            monster_attribute = soup2.select('body > div > div.monster-container > div.monster-sp-status > div.status-table > table > tbody > tr:nth-child(2) > td:nth-child(2)')
            monsterinfo.attribute = [monsterinfo.attribute.text for monsterinfo.attribute in monster_attribute]

            monster_family = soup2.select('body > div > div.monster-container > div.monster-detail > div.monster-pcdetail > div.monster-title > div.monster-substatus > p.species')
            monster_battle_type = soup2.select('body > div > div.monster-container > div.monster-detail > div.monster-pcdetail > div.monster-title > div.monster-substatus > p:nth-child(3)')

            monsterinfo.family = [monsterinfo.family.text for monsterinfo.family in monster_family]
            monsterinfo.battle_type = [monsterinfo.battle_type.text for monsterinfo.battle_type in monster_battle_type]

            # 撃種判定(4パターン)
            # https://img-monst.appbank.net/images/attacktype/attacktype_0.png  反射
            # https://img-monst.appbank.net/images/attacktype/gaugeattacktype_0.png 反射＆ゲージ
            # https://img-monst.appbank.net/images/attacktype/attacktype_1.png  貫通
            # https://img-monst.appbank.net/images/attacktype/gaugeattacktype_1.png 貫通＆ゲージ

            monster_type_of_attack = soup2.select('body > div > div.monster-container > div.monster-detail > div.monster-pcdetail > div.monster-title > div.monster-substatus > img')

            for img in monster_type_of_attack:

                if 'https://img-monst.appbank.net/images/attacktype/attacktype_0.png' == img['data-original']:
                    monsterinfo.type_of_attack = '反射'
                    # print('反射')
                elif 'https://img-monst.appbank.net/images/attacktype/gaugeattacktype_0.png' == img['data-original']:
                    monsterinfo.type_of_attack = '反射＆ゲージ'
                    # print('反射＆ゲージ')
                elif 'https://img-monst.appbank.net/images/attacktype/attacktype_1.png' == img['data-original']:
                    monsterinfo.type_of_attack = '貫通'
                    # print('貫通')
                elif 'https://img-monst.appbank.net/images/attacktype/gaugeattacktype_1.png' == img['data-original']:
                    monsterinfo.type_of_attack = '貫通＆ゲージ'
                    # print('貫通＆ゲージ')
                else:
                    monsterinfo.type_of_attack = 'その他'
                    # print('その他')

            monster_ability = soup2.select('body > div > div.monster-container > div.monster-detail > div.monster-pcdetail > div.pcdetail > div > div.monster-status')

            if not monster_ability:
                monster_ability = soup2.select('body > div > div.monster-container > div.monster-detail > div.monster-pcdetail > div.pcdetail > div > div.monster-status-many')

            monsterinfo.ability = [monsterinfo.ability.text for monsterinfo.ability in monster_ability]

            # データセット
            dataList = [monsterinfo.number, monsterinfo.name, monsterinfo.rarity, monsterinfo.attribute,
            monsterinfo.family, monsterinfo.battle_type, monsterinfo.type_of_attack,
            monsterinfo.ability]

            # CSV書き込み
            with open('test.csv', mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(dataList)

    return monsterinfo
