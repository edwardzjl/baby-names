#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging

import pandas as pd

from datetime import datetime

from babynames.scoring import get_score
from babynames.name_generator import NameGenerator
from babynames.word_analyzer import *
from babynames.utils import load_dict, func_timer

logger = logging.getLogger(__name__)


input = {
    "limit_word": "",  # 限定文字(设置后，生成的名字中将固定增加该字)
    "last_name": "周",
    "gender": "female",
    "province": "浙江",
    "city": "杭州",
    "born_at": "2022-04-27T01:37",
    "is_check_component": True,
    "name_length": 3,
}


def summarize(
    first_name: str,
    last_name: str,
    gender: str,
    province: str,
    city: str,
    born_at: datetime,
) -> dict:
    score: dict = get_score(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        province=province,
        city=city,
        born_at=born_at,
    )
    fullname: str = f"{last_name}{first_name}"

    return {
        "姓名": fullname,
        "拼音": " ".join(get_pinyin(fullname)),
        "笔划数": sum(get_bihua(fullname)),
        "八字评分": score["bazi_score"],
        "五格评分": score["wuge_score"],
        "命主星宿": score["mingzhuxingxiu"],
        "命宫": score["minggong"],
        "总分": score["total_score"],
    }


@func_timer
def main(args: dict):
    logger.info("Calculating wuxing score")
    input_file: str = args.input
    input: dict = load_dict(input_file)
    wuxing_score = get_score(
        born_at=datetime.fromisoformat(input["born_at"]),
    )["wuxing_score"]
    wuxing_shortage: str = min(wuxing_score, key=wuxing_score.get)
    overview: dict = {
        "姓": input["last_name"],
        "性别": input["gender"],
        "出生地(省)": input["province"],
        "出生地(市)": input["city"],
        "出生时辰": input["born_at"],
        "命中缺": wuxing_shortage,
        "五行得分": wuxing_score,
    }
    logger.info(overview)

    logger.info("Generating names")
    wuxing_replenish: str = wuxing_shortage if input["is_check_component"] else None
    name_generator = NameGenerator(
        name_length=input["name_length"],
        gender=input["gender"],
        wuxing_replenish=wuxing_replenish,
    )
    names: list = name_generator.generate(number=100)

    logger.info("Calculating name scores")
    scores: list = [
        pd.Series(
            data=summarize(
                first_name=name,
                last_name=input["last_name"],
                gender=input["gender"],
                province=input["province"],
                city=input["city"],
                born_at=datetime.fromisoformat(input["born_at"]),
            )
        )
        for name in names
    ]
    df = pd.concat(scores, axis=1).T
    df = df.sort_values(by=["总分"], ascending=False)
    logger.info("Writing results")
    output: str = args.output
    df.to_csv(output, index=False)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-i", "--input", dest="input", help="input file path")
    parser.add_argument("-o", "--output", dest="output", help="output file path")
    args = parser.parse_args()

    main(args=args)
