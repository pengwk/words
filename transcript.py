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
	视频没有字幕时，返回""
	"""
	import requests
	api_url = "http://video.google.com/timedtext"
	_raw_response = requests.get(api_url, 
		params={"lang": lang, "v": video_id})
	return _raw_response.content


def get_word_baseform(word):
	from nltk.stem.wordnet import WordNetLemmatizer
	# from nltk.corpus import wordnet
	return WordNetLemmatizer().lemmatize(word)


def simple_token(text, to_lowcase):
    """
    # 将部分字符替换成空格，按空格分词
    :param text:
    :return: a list contains words, e.g. ['In', 'ok']
    """
    _text = text
    punctuations = [',',
                    '.',
                    '!',
                    ';',
                    '?',
                    '"',
                    ]
    for punctuation in punctuations:
        _text = _text.replace(punctuation, ' ')

    return _text.split()


def get_clean_transcript(xml_transcript):
    """

    :param xml_transcript:
    :return: [clean_transcript, list_contains_lines]
    """
    text_transcript = remove_xml_tag(xml_transcript)
    no_break = remove_line_break(text_transcript)
    return no_break

def remove_xml_tag(xml_text):
    # todo 问题 xml去掉后没有空格造成 两个词连接在一起 ok
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

    :param text:
    :param is_json:
    :return:
    """
    import json
    data = {}
    if tokens is None:
    	tokens = simple_token(text)
    for word in tokens:
        if word not in data:
            data[word] = 1
        else:
            data[word] += 1
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

    return float(word_count)/float(time)


# def test_word_count():
#
#     from transcript import get_test_transcript,get_clean_transcript
#     import pprint
#     clean_transcript = get_clean_transcript(get_test_transcript())[0]
#     print total_word(clean_transcript)
#     pprint.pprint(word_count(clean_transcript))