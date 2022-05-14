# -*- coding: utf-8 -*-

import re
import requests

from bs4 import BeautifulSoup


def check_duplication(name: str):
    url: str = "http://name.renren.com/tongMing/search"
    params: dict = {"q": name, "cx": "014540359382904656588:9tf8clwp-ki", "ie": "UTF-8"}

    resp = requests.post(
        url=url,
        data=params,
        allow_redirects=False,
    )
    if resp.status_code == 301:
        next_url = resp.__dict__["headers"]["location"]
        body = requests.get(url=next_url).content

        # 解析同名数量
        soup = BeautifulSoup(body, "html.parser")
        duplicate_result = soup.find_all("p", class_="search_tip")

        if duplicate_result:
            for node in duplicate_result:
                names_total = node.find_all("font")[1].get_text()
                girls_total = node.find_all("font")[2].get_text()
                boys_total = node.find_all("font")[3].get_text()
        else:
            names_total = "0人"
            girls_total = "女生0.00%"
            boys_total = "男生0.00%"
    else:
        names_total = "0人"
        girls_total = "女生0.00%"
        boys_total = "男生0.00%"

    girls_num = re.findall("\d*\.\d*", girls_total)[0]
    boys_num = re.findall("\d*\.\d*", boys_total)[0]

    # 名字性别偏向
    name_sex = ""
    if int(float(girls_num)) > int(float(boys_num)):
        name_sex = "女"
    elif int(float(boys_num)) > int(float(girls_num)):
        name_sex = "男"
    else:
        name_sex = "中性"

    return names_total, girls_total, boys_total, name_sex
