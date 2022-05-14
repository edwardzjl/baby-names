# -*- coding: utf-8 -*-

import csv
import logging
import json

from timeit import default_timer as timer
from datetime import timedelta

logger = logging.getLogger(__name__)

def func_timer(func):
    """Decorator to audit function execution time, in DEBUG level

    Args:
        func: function to audit
    Returns:
        function output
    """
    def inner(*args, **kwargs):
        start = timer()
        res = func(*args, **kwargs)
        end = timer()
        logger.debug(f"{func} finished in {timedelta(seconds=end - start)}")
        return res
    return inner

@func_timer
def load_dict(dict_path: str) -> dict:
    logger.info(f"Loading dict: {dict_path}")
    with open(dict_path, encoding="UTF-8") as f:
        res = json.load(f)
    return res

def csv2json(input, output):
    with open(input, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        dictionary = {line[0] : line[1] for line in reader}

    with open(output, "w", encoding="utf-8") as fp:
        json.dump(dictionary, fp, ensure_ascii=False, indent=4)

def time_cn(hour: int, unit: bool = True) -> str:
    """Convert input hour to Chinese time (时辰)

    Args:
        hour (int): standard hour, [0, 24)
        unit (bool): whether to include unit ("时")
    Returns:
        str: Chinese time (时辰), one of ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"](时)
    
    Example:
        input: "1"
        output: 丑时
    """
    times: list = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    time_cn: str = times[((hour + 1) % 24) // 2]
    if unit:
        time_cn = f"{time_cn}时"
    return time_cn
