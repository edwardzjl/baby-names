# -*- coding: utf-8 -*-

import unittest

from babynames.scoring import *


class ScoringTest(unittest.TestCase):
    # TODO: this could be unstable
    def test_wx_score(self):
        res = get_score(
            last_name="周俊林",
            gender="male",
            province="浙江",
            city="杭州",
            born_at=datetime.fromisoformat("1990-03-15T01:37"),
        )
        expected: dict = {
            "wuxing_score": {"水": 8.0, "木": 192.0, "火": 45.0, "土": 49.0, "金": 30.0},
            "wuge_score": 71.0,
            "bazi_score": 56.0,
            "total_score": 127.0,
            "minggong": "坎宫（东四命）",
            "mingzhuxingxiu": "（井）宿",
        }
        self.assertDictEqual(res, expected)


if __name__ == "__main__":
    unittest.main()
