# -*- coding: utf-8 -*-

from cjklib.characterlookup import CharacterLookup
from pypinyin import pinyin, Style

cjk = CharacterLookup("C")

def get_pinyin(words: str, style: Style = Style.TONE) -> list:
    """Get the pinyin of each word in input words, return as a list

    Args:
        words (str): input words that needs analyze

    Returns:
        list: pinyin of each word
    
    Example:
        input: "付吧儿"
        output: ["fù", "ba", "ér"]
    """
    return [item[0] for item in pinyin(words, style)]

def get_bihua(words: str) -> list:
    """Get the bihua of each word in input words, return as a list

    Args:
        words (str): input words that needs analyze

    Returns:
        list: bihua of each word
    
    Example:
        input: "付吧儿"
        output: [5, 7, 2]
    """
    return [cjk.getStrokeCount(word) for word in words]
