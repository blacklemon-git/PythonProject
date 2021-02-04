#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import time
import random
import urllib.request
import sys

# ページ数(キャラ数)
pages = 5300
# 待機時間
bt = 2
# 待機時間＋ランダム
bt_random = random.uniform(0.2, 3)

# 欠番メモ
# 46-55
# 211-215
# 785,786
# 1884,1875

for i in range(1, pages + 1):

    try:
        time.sleep(bt + bt_random)
        res = requests.get('https://monst.appbank.net/monster/' + str(i) + '.html')
        res.raise_for_status()
    except   requests.exceptions.RequestException as e:
        print('エラー : ', e)
        i= i + 1
    else:
        url = 'https://monst.appbank.net/monster/' + str(i) + '.html'
        urllib.request.urlretrieve(url, './download/appbanknet' + str(i) + '.html')
    if i == pages:
        print('処理が終了しました。')
