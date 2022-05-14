# -*- coding: utf-8 -*-

import json
import requests
from bs4 import BeautifulSoup, PageElement


class Component(object):
    """偏旁"""

    def __init__(self, dictionary_filepath: str = None):
        if dictionary_filepath:
            with open(dictionary_filepath, encoding="UTF-8") as f:
                self.dictionary = json.load(f)
        else:
            self.dictionary = {}

    def get_component(self, word: str) -> str:
        component: str = self.dictionary.get(word)
        if not component:
            component = self.__get_component_from_baidu(word=word)
            self.dictionary[word] = component
        return component

    def __get_component_from_baidu(self, word: str) -> str:
        url: str = f"https://hanyu.baidu.com/zici/s?ptype=zici&wd={word}"
        html: bytes = requests.post(url=url).content
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
        li: PageElement = soup.find(id="radical")
        return li.span.contents[0]
