# -*- coding: utf-8 -*-

import logging
import re
import requests
import unicodedata

from datetime import datetime

from bs4 import BeautifulSoup

from babynames.utils import time_cn

logger = logging.getLogger(__name__)


__gender_dict: dict = {"male": "1", "female": "0"}


def get_score(
    born_at: datetime,
    first_name: str = None,
    last_name: str = None,
    gender: str = None,
    province: str = None,
    city: str = None,
) -> dict:
    """Analyze a person based on his / her name, birth time and location
    Analyze was done by crawling <https://www.threetong.com/ceming/baziceming/xingmingceshi.php>

    Args:
        born_at (datetime): 生辰
        first_name (str): 名
        last_name (str): 姓
        gender (str): 性别
        province (str): 省
        city (str): 市
    Returns:
        dict:
    """
    url: str = "https://www.threetong.com/ceming/baziceming/xingmingceshi.php"
    request_data: dict = {
        "txtName": last_name,  # 姓
        "name": first_name,  # 名
        "rdoSex": __gender_dict.get(gender),  # 性别
        "cboYear": born_at.year,
        "cboMonth": born_at.month,
        "cboDay": born_at.day,
        "cboHour": f"{born_at.hour}-{time_cn(born_at.hour)}时",
        "cboMinute": f"{born_at.minute}分",
        "pid": province,  # 省
        "cid": city,  # 市
        "isbz": 1,  # 结合生辰八字
        "data_type": 0,
        "zty": 0,  # 真太阳时
    }
    raw_html: bytes = requests.post(url=url, data=request_data).content
    soup = BeautifulSoup(raw_html, "html.parser")

    sm_wuxing: list = soup.find_all("div", class_="sm_wuxing")
    node_texts: list = [x.get_text(strip=True) for x in sm_wuxing]
    res: dict = {
        "wuxing_score": __wuxing_score(node_texts=node_texts),
        "wuge_score": __wuge_score(node_texts=node_texts),
        "bazi_score": __bazi_score(node_texts=node_texts),
    }
    res["total_score"] = (res["wuge_score"] or 0) + (res["bazi_score"] or 0)

    bazi_box_contents: list = soup.find("ul", class_="bazi_box1").extract().contents
    bazi_dict: dict = __bazi_analyze(bazi_box_contents=bazi_box_contents)
    res["minggong"] = bazi_dict["命宫分析"]
    res["mingzhuxingxiu"] = bazi_dict["命主星宿"]
    return res


def __wuxing_score(node_texts: list) -> dict:
    wuxing_powers: list = [
        unicodedata.normalize("NFKD", node_text.split(":")[1])
        for node_text in node_texts
        if "五行力量:" in node_text
    ]
    # there should be only one wuxing power
    if len(wuxing_powers) > 0:
        wuxing_power = wuxing_powers[0]
        scores: list = [x.strip() for x in wuxing_power.split(";") if x.strip()]
        match_objs: list = [re.match(r"([金木水火土])\s*(\d+)\s*分", score) for score in scores]
        wuxing_score: dict = {
            match_obj.group(1): float(match_obj.group(2)) for match_obj in match_objs
        }
        return wuxing_score


def __wuge_score(node_texts: list) -> float:
    wuge_score: list = [
        unicodedata.normalize("NFKD", node_text)
        for node_text in node_texts
        if "姓名五格评分" in node_text
    ]
    wuge_re: str = r".*?姓名五格评分.*?(\d+)分"
    wuge_pattern = re.compile(wuge_re)
    # there should be only one bazi score
    if len(wuge_score) > 0:
        wuge_match = wuge_pattern.match(wuge_score[0])
        return float(wuge_match.group(1))


def __bazi_score(node_texts: list) -> float:
    bazi_score: list = [
        unicodedata.normalize("NFKD", node_text)
        for node_text in node_texts
        if "姓名八字评分" in node_text
    ]
    bazi_re: str = r".*?姓名八字评分.*?(\d+)分"
    bazi_pattern = re.compile(bazi_re)
    # there should be only one bazi score
    if len(bazi_score) > 0:
        bazi_match = bazi_pattern.match(bazi_score[0])
        return float(bazi_match.group(1))


def __bazi_analyze(bazi_box_contents: list) -> dict:
    return {
        x[0]: x[1]
        for x in (
            x.split(":")
            for x in (
                node_content.get_text(strip=True) for node_content in bazi_box_contents
            )
        )
    }
