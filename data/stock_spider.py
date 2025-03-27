# -*- coding: utf-8 -*-
import json
import os
import random
from random import randint

import pandas as pd
import requests
import io
from bs4 import BeautifulSoup as BS
import time
import re
import re

"""爬取东方财富网的股票数据"""


# 根据股票代码判断证券交易所
def get_address(code):
    # 上海
    if code.startswith('6'):
        return 'SH'
    # 深圳
    if code.startswith('002') or code.startswith('000') or code.startswith('3'):
        return 'SZ'
    # 北京
    if code.startswith('8') or code.startswith('4'):
        return 'BJ'

# 根据股票代码判断股票类型
def get_category(code):
    if code.startswith('6'):
        return '上证A股'
    if code.startswith('002'):
        return '深圳中小板'
    if code.startswith('000'):
        return '深圳主板'
    if code.startswith('3'):
        return '深圳创业板'
    if code.startswith('8') or code.startswith('4'):
        return '北证A股'

headers = {
    "Origin": "http://9.push2.eastmoney.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
}

categorys = ["股票数据"]
names = ["股票数据"]
base = "http://9.push2.eastmoney.com/api/qt/clist/get?";
base2 = "https://datacenter.eastmoney.com/securities/api/data/v1/get?reportName=RPT_F10_BASIC_ORGINFO&columns" \
        "=SECUCODE%2CSECURITY_CODE%2CSECURITY_NAME_ABBR%2CORG_CODE%2CORG_NAME%2CORG_NAME_EN%2CFORMERNAME%2CSTR_CODEA" \
        "%2CSTR_NAMEA%2CSTR_CODEB%2CSTR_NAMEB%2CSTR_CODEH%2CSTR_NAMEH%2CSECURITY_TYPE%2CEM2016%2CTRADE_MARKET" \
        "%2CINDUSTRYCSRC1%2CPRESIDENT%2CLEGAL_PERSON%2CSECRETARY%2CCHAIRMAN%2CSECPRESENT%2CINDEDIRECTORS%2CORG_TEL" \
        "%2CORG_EMAIL%2CORG_FAX%2CORG_WEB%2CADDRESS%2CREG_ADDRESS%2CPROVINCE%2CADDRESS_POSTCODE%2CREG_CAPITAL" \
        "%2CREG_NUM%2CEMP_NUM%2CTATOLNUMBER%2CLAW_FIRM%2CACCOUNTFIRM_NAME%2CORG_PROFILE%2CBUSINESS_SCOPE" \
        "%2CTRADE_MARKETT%2CTRADE_MARKET_CODE%2CSECURITY_TYPEE%2CSECURITY_TYPE_CODE%2CEXPAND_NAME_ABBR" \
        "%2CEXPAND_NAME_PINYIN&quoteColumns=&filter=(SECUCODE%3D%22";
requestlist = []
prev_cat = ""
for j in range(len(categorys)):
    for i in range(1, 281):
        tmp = base + "pn="+str(i)+"&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0" \
                                  "|web&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3," \
                                  "f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62," \
                                  "f128,f136,f115,f152&_=1707973229200";
        requestlist.append({"url": tmp, "category": names[j]});
# 对应的url地址和所查询的位置
print(requestlist)
l = []
count = 1;
list = list()
for k in range(len(requestlist)):
    response = requests.get(requestlist[k]["url"], headers=headers)
    # print(response)
    html = response.text
    #print(html)
    soup = BS(html, 'html.parser')

    vs = json.loads(soup.text)

    diff_array = vs.get('data').get('diff')

    for item in diff_array:
        try:
            tmp = {};
            obj = item

            # 解析股票数据

            # 股票名称
            name = obj['f14']
            # 股票代码
            code = obj['f12']
            # 获取证券交易所简称
            address_code = get_address(code)
            # 获取股票类型
            stock_category = get_category(code)

            # 爬取公司简介详情页
            links = base2+code+"."+address_code+"%22)&pageNumber=1&pageSize=1&sortTypes=&sortColumns=&source=HSF10&client=PC&v=09296781112455792"
            res = requests.get(links, headers=headers)
            soupi = BS(res.text, "html.parser")  # 该网页的html代码

            vs2 = json.loads(soupi.text)

            company_info = vs2.get('result').get('data')[0]

            # 公司名称
            company = company_info['ORG_NAME']
            # 公司省份
            province = company_info['PROVINCE']
            # 所属行业
            industry = company_info['EM2016']
            # 公司地址
            address = company_info['ADDRESS']
            # 公司简介
            content = company_info['ORG_PROFILE']

            tmp["name"] = name
            tmp["code"] = code
            tmp["address_code"] = address_code
            tmp["stock_category"] = stock_category
            tmp["company"] = company
            tmp["province"] = province
            tmp["industry"] = industry
            tmp["address"] = address
            tmp["content"] = content
            tmp["category"] = requestlist[k]["category"]

            if tmp["category"] != prev_cat:
                list.clear()
            prev_cat = tmp["category"]

            count = count + 1;
            l.append(tmp);

            dic = {"股票名称": tmp["name"], '股票代码': tmp["code"],
                   '交易所简称': tmp["address_code"], '股票市场类型': tmp["stock_category"], '公司名称': tmp["company"], '省份': tmp['province'],
                   '行业': tmp['industry'], '公司地址': tmp['address'], '公司简介': tmp['content']}
            list.append(dic)

            time.sleep(1);
        except Exception as e:
            print(e)
            continue
        print("爬取数据", tmp)


        try:
            data = pd.DataFrame(list)
            data.to_excel('stock/' + tmp["category"] + '.xlsx', index=None)
        except Exception as e:
            print(e)
            continue




