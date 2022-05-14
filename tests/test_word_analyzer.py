# -*- coding: utf-8 -*-

import unittest

from babynames.word_analyzer import *


class WordAnalyzerTest(unittest.TestCase):

    def test_get_pinyin(self):
        result: list = get_pinyin("付吧儿")
        expected: list = ["fù", "ba", "ér"]
        self.assertListEqual(result, expected)

    def test_get_bihua(self):
        result: list = get_bihua("付吧儿")
        expected: list = [5, 7, 2]
        self.assertListEqual(result, expected)



if __name__ == "__main__":
    unittest.main()