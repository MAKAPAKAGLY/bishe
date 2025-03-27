# -*- coding: utf-8 -*-
import json

import pandas as pd
import requests
from bs4 import BeautifulSoup as BS

"""爬取股票网的价格数据"""

headers = {
    "Origin": "http://9.push2.eastmoney.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
}

categorys = ["2025-03-25"]

names = ["2025-03-25"]
base = "http://9.push2.eastmoney.com/api/qt/clist/get?"

requestlist = []
prev_cat = ""
for j in range(len(categorys)):
    for i in range(1, 281):
        tmp = base + "pn=" + str(
            i) + "&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:0+t" \
                 ":6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15," \
                 "f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1707973229200";
        requestlist.append({"url": tmp, "category": names[j]})
# 对应的url地址和所查询的位置
print(requestlist)
l = []
count = 1
list = list()
for k in range(len(requestlist)):
    response = requests.get(requestlist[k]["url"], headers=headers)
    # print(response)
    html = response.text
    # print(html)
    soup = BS(html, 'html.parser')

    vs = json.loads(soup.text)

    diff_array = vs.get('data').get('diff')

    for item in diff_array:
        try:
            tmp = {}
            obj = item

            # 解析股票数据

            # 股票名称
            name = obj['f14']
            # 股票代码
            code = obj['f12']
            # 最新价
            newprice = obj['f2']
            # 开盘价
            openprice = obj['f17']
            # 最低价
            lowprice = obj['f16']
            # 最高价
            highprice = obj['f15']
            # 成交量
            turnover = obj['f5']
            # 成交额
            amount = obj['f6']
            # 涨跌幅
            chg = obj['f3']

            tmp["name"] = name
            tmp["code"] = code
            tmp["newprice"] = newprice
            tmp["openprice"] = openprice
            tmp["lowprice"] = lowprice
            tmp["highprice"] = highprice
            tmp["turnover"] = turnover
            tmp["amount"] = amount
            tmp["chg"] = chg
            tmp["category"] = requestlist[k]["category"]

            if tmp["category"] != prev_cat:
                list.clear()
            prev_cat = tmp["category"]

            count = count + 1;
            l.append(tmp);

            dic = {"股票名称": tmp["name"], '股票代码': tmp["code"],
                   '最新价': tmp["newprice"], '开盘价': tmp["openprice"], '最低价': tmp["lowprice"],
                   '最高价': tmp['highprice'],
                   '成交量': tmp['turnover'], '成交额': tmp['amount'], '涨跌幅': tmp['chg']}
            list.append(dic)

            # time.sleep(1);
        except Exception as e:
            print(e)
            continue
        print("爬取数据", tmp)

        try:
            data = pd.DataFrame(list)
            data.to_excel('stockdata/' + tmp["category"] + '.xlsx', index=None)
        except Exception as e:
            print(e)
            continue
