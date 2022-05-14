# -*- coding: utf-8 -*-

import unittest
from datetime import datetime

from pypinyin import pinyin, Style

from babynames.utils import *


@func_timer
def foo():
    pass

wx_dict: dict = {
    "火"
}

def cn_sort(ch_char: str):
    if ch_char == "周": # mock specific char
        return ["a"] + pinyin(ch_char, style=Style.TONE3)
    if ch_char in wx_dict:
        return ["b"] + pinyin(ch_char, style=Style.TONE3)
    return ["z"] + pinyin(ch_char, style=Style.TONE3)


class WordAnalyzerTest(unittest.TestCase):

    def test_timer(self):
        foo()

    def test_cn_sort(self):
        chars = ["不是", "不对", "周", "啊", "火"]
        result: list = sorted(chars, key=cn_sort)
        expected: list = ["周", "火", "啊", "不对", "不是"]
        self.assertListEqual(result, expected)
    
    def test_dt(self):
        dt = datetime.fromisoformat("2011-11-04T00:05:23")
        self.assertEqual(dt.year, 2011)
        self.assertEqual(dt.month, 11)
        self.assertEqual(dt.day, 4)
        self.assertEqual(dt.hour, 0)
        self.assertEqual(dt.minute, 5)
        self.assertEqual(dt.second, 23)
    
    def test_cn_time(self):
        self.assertEqual(time_cn(0), "子时")
        self.assertEqual(time_cn(1), "丑时")
        self.assertEqual(time_cn(2), "丑时")
        self.assertEqual(time_cn(3), "寅时")
        self.assertEqual(time_cn(4), "寅时")
        self.assertEqual(time_cn(5), "卯时")
        self.assertEqual(time_cn(6), "卯时")
        self.assertEqual(time_cn(7), "辰时")
        self.assertEqual(time_cn(8), "辰时")
        self.assertEqual(time_cn(9), "巳时")
        self.assertEqual(time_cn(10), "巳时")
        self.assertEqual(time_cn(11), "午时")
        self.assertEqual(time_cn(12), "午时")
        self.assertEqual(time_cn(13), "未时")
        self.assertEqual(time_cn(14), "未时")
        self.assertEqual(time_cn(15), "申时")
        self.assertEqual(time_cn(16), "申时")
        self.assertEqual(time_cn(17), "酉时")
        self.assertEqual(time_cn(18), "酉时")
        self.assertEqual(time_cn(19), "戌时")
        self.assertEqual(time_cn(20), "戌时")
        self.assertEqual(time_cn(21), "亥时")
        self.assertEqual(time_cn(22), "亥时")
        self.assertEqual(time_cn(23), "子时")
        


if __name__ == "__main__":
    unittest.main()