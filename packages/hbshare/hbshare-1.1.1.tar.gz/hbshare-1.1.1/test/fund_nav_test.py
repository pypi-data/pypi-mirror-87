#!/usr/bin/python
#coding:utf-8

"""
@author: Meng.lv
@contact: meng.lv@howbuy.com
@software: PyCharm
@file: fund_nav_test.py
@time: 2020/6/15 10:50
"""

import hbshare as hbs
import time

def test_get_fund_newest_nav():
    hbs.set_token("qwertyuisdfghjkxcvbn1000")
    data = hbs.get_fund_newest_nav_by_code('000004')
    print(data)

def get_simu_corp_list_by_keyword():
    hbs.set_token("qwertyuisdfghjkxcvbn1000")
    # data = hbs.get_simu_corp_list_by_keyword('黑石')
    data = hbs.get_prod_list_by_corp_code(80535346)
    print(data)


def get_simu_nav_by_code():
    hbs.set_token("qwertyuisdfghjkxcvbn1000")
    data, total_count = hbs.get_simu_nav_by_code("P0010", "20190101", "20191231")
    print(data)
    print(total_count)


def test_get_fund_holding():
    hbs.set_token("qwertyuisdfghjkxcvbn1000")
    data = hbs.get_fund_holding('200016', '2020-09-30')
    print(data)

def get_fund_holding_publish_date():
    hbs.set_token("qwertyuisdfghjkxcvbn1000")
    data = hbs.get_fund_holding_publish_date('200016')
    print(data)


if __name__ == "__main__":
    get_fund_holding_publish_date()

