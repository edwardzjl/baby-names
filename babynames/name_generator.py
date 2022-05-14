# -*- coding: utf-8 -*-

import logging
import os

from pypinyin import pinyin, Style
from babynames.utils import load_dict, func_timer

logger = logging.getLogger(__name__)


class NameGenerator(object):
    def __init__(
        self,
        name_length: int,
        gender: str = None,
        name_dict_path: str = None,
        fixed_word: str = None,
        wuxing_dict_path: str = None,
        wuxing_replenish: str = None,
    ):
        """姓名生成器

        Args:
            name_length (int): 姓名长度
            gender (str): 性别偏好
            name_dict_path (str): 预定义姓名字典路径
            fixed_word (str): 姓名中固定字
            wuxing_dict_path (str): 预定义五行补全字典路径
            wuxing_replenish (str): 五行缺 *
        """
        self.name_length = name_length
        self.gender = gender
        self.name_dict_path = name_dict_path
        self.fixed_word = fixed_word
        self.wuxing_dict_path = wuxing_dict_path
        self.wuxing_replenish = wuxing_replenish

    @func_timer
    def generate(self, number: int = -1) -> list:
        """_summary_

        Args:
            number (int): number of names to generate

        Returns:
            list: generated names
        """
        logger.info("Generating names")

        if self.name_length == 2:
            if self.fixed_word:
                return [self.fixed_word]
            res: list = self.__name_list("single")
        else:
            res = (
                self.__generate_with_fixed_word()
                if self.fixed_word
                else self.__generate()
            )
        res = list(set(res))
        res.sort(key=self.__cn_sort)
        del self.wx_dict  # release wx_dict from memory
        return res[:number]

    @func_timer
    def __generate_with_fixed_word(self):
        names = self.__name_list("single")
        fixed_first = [f"{self.fixed_word}{name}" for name in names]
        fixed_last = [f"{name}{self.fixed_word}" for name in names]
        return fixed_first + fixed_last

    @func_timer
    def __generate(self):
        single_names = self.__name_list("single")
        double_names = self.__name_list("double")
        redup_names = [f"{x}{x}" for x in single_names] # 叠词
        return double_names + redup_names

    def __name_list(self, type: str) -> list:
        """Get predefined name list

        Args:
            type (str): common Chinese name type, one of "single" or "double"

        Returns:
            list: predefined name list
        """
        dict_path: str = self.name_dict_path or os.path.join(".", "dicts", "names.json")
        name_dict: dict = load_dict(dict_path=dict_path)
        return (
            name_dict[self.gender][type]
            if self.gender
            else name_dict["male"][type] + name_dict["female"][type]
        )

    def __cn_sort(self, name: str):
        if self.fixed_word and name == self.fixed_word:
            name = "a" + name
        if self.wuxing_replenish:
            if (not hasattr(self, "wx_dict")) or (not self.wx_dict):
                dict_path: str = self.wuxing_dict_path or os.path.join(
                    ".", "dicts", "wuxing_components.json"
                )
                self.wx_dict: dict = load_dict(dict_path=dict_path)
            if name in self.wx_dict[self.wuxing_replenish]:
                name = "b" + name
        name = "z" + name
        return [ord(char) for char in name]

    # sorting by pinyin on large list is very slow, use __cn_sort instead
    def __cn_sort_py(self, name: str):
        if self.fixed_word and name == self.fixed_word:
            return ["a"] + pinyin(name, style=Style.TONE3)
        if self.wuxing_replenish:
            dict_path: str = self.wuxing_dict_path or ".\\dicts\\wuxing_components.json"
            wx_dict: dict = load_dict(dict_path=dict_path)
            if name in wx_dict[self.wuxing_replenish]:
                return ["b"] + pinyin(name, style=Style.TONE3)
        return ["z"] + pinyin(name, style=Style.TONE3)
