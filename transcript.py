#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This module does
    Date created: 4/20/2016
    Date last modified: 4/25/2016
    Python Version: 2.7.10
    这速度也太他妈慢了！

"""

__author__ = "pengwk"
__copyright__ = "Copyright 2016, pengwk"
__credits__ = [""]
__license__ = "Private"
__version__ = "0.1"
__maintainer__ = "pengwk"
__email__ = "pengwk2@gmail.com"
__status__ = "BraveHeart"


def download_transcript(video_id, lang="en"):
    """
    视频没有字幕时，返回
    """
    # 查看transcript_list
    # 有英文字幕时，下载
    import requests
    from bs4 import BeautifulSoup
    _result = requests.get('https://video.google.com/timedtext?hl=en&type=list&v={}'.format(video_id))
    _soup = BeautifulSoup(_result.content, "lxml")
    _en_track = _soup.find_all(lang_code="en")
    if not _en_track:
        return ""
    _name = _en_track[0]["name"]
    _raw_response = requests.get("http://video.google.com/timedtext",
                                 params={"lang": lang,
                                         "v": video_id,
                                         "name": _name})
    import HTMLParser
    return HTMLParser.HTMLParser().unescape(_raw_response.content.decode("utf-8")).encode("utf-8")


def get_word_baseform(word):
    from nltk.stem.wordnet import WordNetLemmatizer
    return WordNetLemmatizer().lemmatize(word)


def simple_token(text, ):
    """
    # 将部分字符替换成空格，按空格分词
    :param text:
    :return: a list contains words, e.g. ['In', 'ok']
    例外：11th That&#39缺少分号
    """
    _text = text
    punctuations = (',',
                    '.',
                    '!',
                    ';',
                    '?',
                    '"',
                    ":",
                    "[",
                    "]",
                    "{",
                    "}",
                    u"“",  #
                    u"”",  # 中文引号
                    u"‘",  # 中文单引号
                    # "’",  不能替换成空格 world’s world's
                    u"。",  # 句号
                    u"，",  # 逗号
                    u"…",   # 英文省略号
                    u"……",  #
                    )

    for punctuation in punctuations:
        _text = _text.replace(punctuation, ' ')
    _text = _text.replace(u"’", "'")
    return _text.split()


def get_clean_transcript(xml_transcript):
    """

    :param xml_transcript:
    :return: [clean_transcript, list_contains_lines]
    """
    text_transcript = remove_xml_tag(xml_transcript)
    return remove_line_break(text_transcript)


def remove_xml_tag(xml_text):
    # xml去掉后没有空格造成 两个词连接在一起 ok
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(xml_text, 'lxml')
    # 直接使用soup.text会使得 两个tag之间文本没有空格，让两个单词连成一个，这个参数指定了tag之间的文本用空格连接起来
    text = soup.get_text(" ")
    return text


def remove_line_break(text):
    return text.replace('\n', ' ')


# 词频统计
def statistic_frequency(tokens=None, text=None, is_json=True):
    """

    :param tokens:
    :param text:
    :param is_json:
    :return:
    """
    import json
    data = {}
    if tokens is None:
        tokens = simple_token(text)
    import collections
    data = collections.Counter(tokens)
    if is_json is True:
        return json.dumps(data)
    else:
        return data


def total_word(text):
    return len(simple_token(text))


def speech_speed(word_count, time):
    """

    :param word_count:
    :param time:
    :return:
    """

    return float(word_count) / float(time)


if __name__ == "__main__":
    import requests

    print download_transcript("Mo6_u7r6f3Q")
