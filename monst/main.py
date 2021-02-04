# -*- coding: utf-8 -*-
import monsterinfo
from time import sleep
# モンスター図鑑
# for i in range(0, 53):

# ページ数(キャラ数)
pages = 5300
# 待機時間
bt = 0.5

# テスト用
for i in range(5000, pages + 1):
    # print("ページ数 = " + str(i))
    sleep(bt)

    Monstarbook = monsterinfo.get_monstappbanknet('https://monst.appbank.net/monster/' + str(i) + '.html')
