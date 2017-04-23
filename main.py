#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This module does
    Date created: 4/20/2017
    Date last modified: 4/25/2017
    Python Version: 2.7.10
    这速度也太他妈慢了！

"""

__author__ = "pengwk"
__copyright__ = "Copyright 2017, pengwk"
__credits__ = [""]
__license__ = "Private"
__version__ = "0.1"
__maintainer__ = "pengwk"
__email__ = "pengwk2@gmail.com"
__status__ = "BraveHeart"

from transcript import get_clean_transcript

import nltk

debug = False


def break_passage():
    [text, lines] = get_clean_transcript()
    # todo 提取单词，处理掉句子间的标点
    print text.split()
    print get_single_word(text)
    print len(lines)


def get_single_word(text):
    import nltk
    pattern = r'''(?x)   # set flag to
      ([A-Z]\.])+
    | \w+(-\w+)*
    | \$?\d+(\.\d+)?%?
    | \.\.\.
    | [][.,;"'?():-_`]
    '''
    pattern = r'''(?x)          # set flag to allow verbose regexps
            (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
          | \w+(?:-\w+)*        # words with optional internal hyphens
          | \$?\d+(?:\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
          | \.\.\.              # ellipsis
          | [][.,;"'?():_`-]    # these are separate tokens; includes ], [
        '''
    my_pattern = r'''(?x)          # set flag to allow verbose regexps
            (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
          | \w+(?:-\w+)*        # words with optional internal hyphens
          | \$?\d+(?:\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
          | \.\.\.              # ellipsis
          | [][.,;"?():_-]    # these are separate tokens; includes ], [
        '''
    return nltk.regexp_tokenize(text, my_pattern)


def simple_token(text):
    # type: (object) -> list
    """
    将部分字符替换成空格，按空格分词,
    :rtype: object
    :param text:
    :return: a list contains words, e.g. ['In', 'ok']
    """
    _text = text
    # 中文标点符号的去处
    punctuations = [',',
                    '.',
                    '!',
                    ';',
                    '?',
                    '"',
                    ]

    for punctuation in punctuations:
        _text = _text.replace(punctuation, ' ')

    if debug is True:
        print _text
        print _text.split()

    return _text.split()


def main():
    return None


def ana():
    # todo 提速 使用多线程，多进程 分析性能的瓶颈
    from query_api import get_videos
    debug = True
    if debug is True:
        for index, video in enumerate(get_videos()):
            print index
            some(video)
    else:
        [some(video) for video in get_videos()]
    return "all be ok!"


def some(video):
    from database import Word, Video, get_or_create
    from query_api import ses
    # 一个Video的字幕分析，分析出每一个单词，建立对应的关系
    # video = session.query(Video)[480]
    clean_transcript = get_clean_transcript(video.raw_transcript)[0]
    # 分析出单词
    words = simple_token(clean_transcript)
    # 将单词加入数据库
    # todo 处理大小写 ''.lower() islower() upper()
    for word in words:
        if len(word) > 30:
            print word
            break
        word_instance, flag = get_or_create(ses, Word, text=word)
        ses.commit()
        #  添加关系
        video.words.append(word_instance)
        ses.commit()

    return None


# 词频统计
def word_count(text, is_json=True):
    """

    :param text:
    :param is_json:
    :return:
    """
    import json
    data = {}
    for word in simple_token(text):
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


def test_word_count():

    from transcript import get_test_transcript,get_clean_transcript
    import pprint
    clean_transcript = get_clean_transcript(get_test_transcript())[0]
    print total_word(clean_transcript)
    pprint.pprint(word_count(clean_transcript))



if __name__ == "__main__":
    # break_passage()
    # print simple_token(get_clean_transcript()[0])
    # ana()
    test_word_count()
# 数据库连接
def create_session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    eng = create_engine('mysql://root:nopassword@localhost/youtube_videos?charset=utf8', 
                        encoding='utf-8')

    session = sessionmaker(bind=eng)
    return session()

# 首先，定义一个频道列表
# 获取单个频道里的上传列表

# 获取列表中所有的视频id，将上传列表与视频存入数据库，加入外键关系

# 将频道列表中的所有频道完成这一步
def download_channel_video_list(channel_id):
    # 获取上传列表Id
    from youtube import get_upload_list_id,get_playlist_items

    upload_list_id = get_upload_list_id(channel_id)
    video_id_list = get_playlist_items(upload_list_id)
    # 将上传列表加入数据库
    from models import Video, Playlist
    playlist = Playlist(playlist_id=upload_list_id)
    session = create_session()
    session.add(playlist)
    session.commit()
    # 将视频与上传列表建立关系，并加入数据库
    def _add_video(video_id):
        # todo 复习闭包
        session = create_session()
        video = Video(video_id=video_id)
        video.playlists.append(playlist)
        session.add(video)
        session.commit()
        session.close()

    [_add_video(video_id) for video_id in video_id_list]
    session.close()
    return None


# 获取视频相关信息，并加入数据库，如：xml版的字幕文件
def download_video_detail(video):
    """
    """
    from youtube import get_video_detail
    detail = get_video_detail(video.id)
    
    session = create_session()
    # 获取video对象
    from models import Video, VideoTag, Channel
    # 填入数据
    snippet = detail["snippet"]
    contentDetails = detail["contentDetails"]
    statistics = detail["statistics"]
    status = detail["status"]
    # status
    video.license = status["license"]
    video.embebable = status["embedable"]
    # iframe播放器URL
    video.player_url = detail["player"]["embedHtml"]
    # 统计 statistics
    video.view_count = int(statistics["viewCount"])
    video.like_count = int(statistics["likeCount"])
    video.dislike_count = int(statistics["dislikeCount"])
    video.favorite_count = int(statistics["favoriteCount"])
    video.comment_count = int(statistics["commentCount"])
    # 内容细节 contentDetails
    video.duration = contentDetails["duration"]
    video.dimension = contentDetails["dimension"]
    video.definition = contentDetails["definition"]
    # todo 会自动转换false吗？
    video.has_caption = contentDetails["caption"]
    video.is_licensed_content = contentDetails["licensedContent"]
    video.projection = contentDetails["projection"]
    # snippet
    video.title  = snippet["title"]
    video.description  = snippet["description"]
    video.published_at  = snippet["publishedAt"]
    # todo 会自动转换成json吗？
    video.thumbails  = snippet["thumbails"]
    video.category_id  = int(snippet["categoryId"])

    session.commit()
    # 处理tag
    tags = snippet["tags"]
    for tag in tags:
        _tag = VideoTag(name=tag)
        session.add(_tag)
        session.commit()
        video.tags.append(_tag)
    # 处理channel
    channel = Channel(channel_title=snippet["channelTitle"], 
                    channel_id=snippet["channelId"])
    session.add(channel)
    session.commit()
    session.close()    

def download_transcript(video):
    from transcript import download_transcript as dt
    session = create_session()
    video.xml_transcript = dt.(video.id)
    session.commit()
    session.close()
    return None

# 分析字幕文件 转为text，统计每个视频的词频，建立词与视频的对应关系 
def analysis_transcript(video):
    session = create_session()
    # 转换字幕成text
    from transcript import get_clean_transcript, simple_token
    clean_transcript = get_clean_transcript(video.xml_transcript)
    video.clean_transcript = clean_transcript
    # 分词
    tokens = simple_token(clean_transcript)
    import logging
    logging.basicConfig(filename='example.log',level=logging.DEBUG)
    # 将词汇与视频建立关系，加入数据库
    for word in tokens:
        # 记录非全数字，全字母，长度超过15的词
        if len(word) > 15 or not word.isalpha() or not word.isalnum():
            logging.debug(word)
            break
        if word.istitle() is False:
            word_instance, flag = get_or_create(session, Word, text=word)
        else:
            word_instance, flag = get_or_create(session, Word, text=word.lower())
        session.commit()
        #  添加关系
        video.words.append(word_instance)
        sesssion.commit()    
    # 统计词频，总字数，加入数据库，计算语速
    word_number = len(tokens)
    video.word_number = word_number
    video.speed = word_number / duration_to_min(video.duration)
    from transcript import statistic_frequency
    video.word_frequency = statistic_frequency(tokens)
    session.commit()
    session.close()

def duration_to_min(duration, ):
    """
    duration的例子PT3M32S,返回分钟数
    """
    _min = duration.split("M")[0][2:]
    second = duration.split("M")[1][:-1]
    return int(_min) + int(second)/60.0

# 获取所有词的原形，检查包含符号的词，并输出到文件中
def load_word_list(filename):
    import json
    with open(filename, "r") as f:
        _list = json.load(f)
    return set(_list)

# 根据CET6单词表，统计每个视频包含的CET6单词，统计总个数，存入数据库
def statistics_for_cet_six(video):
    #加载单词表到内存 数据结构set
    word_set = load_word_list("cet_clean.json")
    from models import CetSixWordList, Video
    from transcript import get_word_baseform
    import json
    # 获取单个视频的所有词
    session = create_session()
    word_list = []
    for word in video.words:
        baseform = get_word_baseform(word.text)
        if baseform in word_set:
            word_list.append(baseform)
    cet_word = CetSixWordList(total_number=len(word_list),
                                word_list=json.dumps(word_list))
    session.add(cet_word)
    video.cet_six_word_list = cet_word
    session.commit()
    session.close()
    return None
    # 词性还原





def main():
    from multiprocessing import Pool
    from multiprocessing.dummy import Pool as ThreadPool

    channels = {"NowThis": "UCgRvm1yLFoaQKhmaTqXk9SA",
                "Stories": "UCJsSEDFFnMFvW9JWU6XUn0Q",
                "Fox News Insider": "UCqlYzSgsh5jdtWYfVIBoTDw"
                }
    channel_id_list = channels.values()
    # 下载视频id
    pool = ThreadPool(5)
    result = pool.map(download_channel_video_list, channel_id_list)
    pool.close() 
    pool.join()
    print "video_id done"
    # 基本信息
    video_list = session.query(Video).all()
    pool = ThreadPool(5)
    result = pool.map(download_video_detail, video_list)
    pool.close() 
    pool.join()
    print "basic detail done"
    # 下载字幕
    video_list = session.query(Video).all()
    pool = ThreadPool(5)
    result = pool.map(download_transcript, video_list)
    pool.close() 
    pool.join()
    print "download transcript done"
    # 分析
    video_list = session.query(Video).all()
    pool = Pool()
    pool.map(analysis_transcript, video_list)
    pool.close()
    pool.join()
    print "analysis done"
    # 统计词汇 
    video_list = session.query(Video).all()
    pool = Pool()
    pool.map(statistics_for_cet_six, video_list)
    pool.close()
    pool.join() 
    print "statistic done"

if __name__ == '__main__':
    main()