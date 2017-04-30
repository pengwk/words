#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This module does
    Date created: 4/20/2017
    Date last modified: 4/25/2017
    Python Version: 2.7.10
    这速度也太他妈慢了！

"""

# from models import db

# _session = db.session
# print "_session", _session

__author__ = "pengwk"
__copyright__ = "Copyright 2017, pengwk"
__credits__ = [""]
__license__ = "Private"
__version__ = "0.1"
__maintainer__ = "pengwk"
__email__ = "pengwk2@gmail.com"
__status__ = "BraveHeart"


# 首先，定义一个频道列表
# 获取单个频道里的上传列表

# 获取列表中所有的视频id，将上传列表与视频存入数据库，加入外键关系


def download_channel_details(channel_id):
    from youtube import get_channel_details
    from models import Channel
    from models import db
    session = db.session
    details = get_channel_details(channel_id)
    snippet = details["snippet"]
    statistics = details["statistics"]
    related_playlists = details["contentDetails"]["relatedPlaylists"]
    if Channel.query.filter_by(channel_id=channel_id).count():
        return None
    channel = Channel(channel_id=channel_id)
    session.add(channel)

    channel.channel_title = snippet.get("title")
    channel.description = snippet.get("description")
    # 2009-10-01T17:49:50.000Z
    channel.published_at = snippet.get("publishedAt")
    channel.thumbails = snippet.get("thumbails")
    # contentDetails
    channel.playlist_likes = related_playlists.get("likes")
    channel.playlist_uploads = related_playlists.get("uploads")
    # topicDetails
    channel.topic_details = details.get("topicDetails")
    # topicCategories
    channel.topic_categories = details.get("topicCategories")
    # branding_settings
    channel.branding_settings = details.get("brandingSettings")
    channel.status = details.get("status")
    # statistics
    channel.view_count = statistics.get("viewCount")
    channel.comment_count = statistics.get("commentCount")
    channel.subscriber_count = statistics.get("subscriberCount")
    channel.hidden_subscriber_count = statistics.get("hiddenSubscriberCount")
    channel.video_count = statistics.get("videoCount")

    session.commit()
    return None


# 将频道列表中的所有频道完成这一步
def download_channel_video_list(channel):
    """

    :param channel: Channel object
    :return: a list contains video id
    """
    # 获取上传列表Id
    from youtube import get_playlist_items
    from models import db
    session = db.session

    upload_list_id = channel.playlist_uploads
    video_id_list = get_playlist_items(upload_list_id)
    # 将上传列表加入数据库
    from models import Video, Playlist
    from database import get_or_create
    playlist, flag = get_or_create(session, Playlist, playlist_id=upload_list_id)

    session.add(playlist)
    session.commit()

    # 将视频与上传列表建立关系，并加入数据库

    def _add_video(_video_id, _session):
        # todo 复习闭包
        video, flag = get_or_create(_session, Video, video_id=_video_id)
        video.playlists.append(playlist)
        _session.add(video)
        _session.commit()

    [_add_video(video_id, session) for video_id in video_id_list]
    return None


def _smart_int(_str):
    # _str 有可能是None
    if _str is not None:
        return int(_str)
    else:
        return -1


# 获取视频相关信息，并加入数据库，如：xml版的字幕文件
def download_video_detail(video):
    """
    """
    from youtube import get_video_detail
    detail = get_video_detail(video.video_id)
    # 获取video对象
    from models import db, Video
    session = db.session
    video = session.query(Video).filter(Video.video_id == video.video_id).one()
    # 填入数据
    # 解决field不存在报KeyError的问题 ok
    # sqlalchemy.exc.OperationalError
    import sqlalchemy
    try:
        snippet = detail["snippet"]
        content_details = detail["contentDetails"]
        statistics = detail["statistics"]
        status = detail["status"]
        # status
        video.license = status.get("license")
        video.embedable = status.get("embedable")
        # iframe播放器URL
        video.player_url = detail["player"]["embedHtml"]
        # 统计 statistics
        video.view_count = _smart_int(statistics.get("viewCount"))
        video.like_count = _smart_int(statistics.get("likeCount"))
        video.dislike_count = _smart_int(statistics.get("dislikeCount"))
        video.favorite_count = _smart_int(statistics.get("favoriteCount"))
        video.comment_count = _smart_int(statistics.get("commentCount"))
        # 内容细节 contentDetails
        video.duration = content_details.get("duration")
        video.dimension = content_details.get("dimension")
        video.definition = content_details.get("definition")
        video.has_caption = content_details.get("caption")
        video.is_licensed_content = content_details.get("licensedContent")
        video.projection = content_details.get("projection")
        # snippet
        video.title = snippet.get("title")
        video.description = snippet.get("description")
        video.published_at = snippet.get("publishedAt")
        video.thumbails = snippet.get("thumbails")
        video.category_id = _smart_int(snippet.get("categoryId"))
        video._tags = snippet.get("tags")
        # session.add(video)
        session.commit()
    except sqlalchemy.exc.OperationalError as e:
        session.rollback()
        print snippet.get("description")
        # todo log
        print e
        pass

    # 处理tag

    # try:
    #     tags = snippet["tags"]
    #     for tag in tags:
    #         _tag, flag = get_or_create(session, VideoTag, name=tag)
    #         session.commit()
    #         video.tags.append(_tag)
    # except KeyError:
    #     pass
    # 处理channel 暂时放弃
    # query = Channel.query.filter_by(channel_id=snippet.get("channelId"))
    # if query.count():
    #     channel = query.one()
    # else:
    #     channel = Channel(channel_id=snippet.get("channelId"), channel_title=snippet["channelTitle"])
    #     session.commit()
    # video.channel = channel
    # session.commit()
    return None


def download_transcript(video):
    from transcript import download_transcript as dt
    from models import db
    from models import Video
    session = db.session
    video = session.query(Video).filter(Video.video_id==video.video_id).one()
    video.xml_transcript = dt(video.video_id)
    print "{}:{}".format(video.video_id, video.xml_transcript[0:10])
    # session.add()

    session.commit()
    return None


# 分析字幕文件 转为text，统计每个视频的词频，建立词与视频的对应关系 
def analysis_transcript(video):
    # 转换字幕成text
    from transcript import get_clean_transcript, simple_token
    from models import db, Video
    session = db.session
    video = session.query(Video).filter(Video.video_id == video.video_id).one()
    clean_transcript = get_clean_transcript(video.xml_transcript)
    video.clean_transcript = clean_transcript
    # 分词
    tokens = simple_token(clean_transcript)
    import logging
    logging.basicConfig(filename='unregular_words.log', level=logging.DEBUG)
    # 将词汇与视频建立关系，加入数据库
    from models import Word
    from database import get_or_create
    for word in tokens:
        # 记录非全数字，全字母，长度超过15的词
        if len(word) > 20 or not word.isalpha() or not word.isalnum():
            logging.debug(word)
            break
        if word.istitle() is False:
            word_instance, flag = get_or_create(session, Word, text=word)
        else:
            word_instance, flag = get_or_create(session, Word, text=word.lower())
        session.commit()
        #  添加关系
        video.words.append(word_instance)
        session.commit()
    # 统计词频，总字数，加入数据库，计算语速
    word_number = len(tokens)
    video.word_number = word_number
    if video.duration is not None or video.duration != "":
        video.speed = word_number / duration_to_min(video.duration)
    from transcript import statistic_frequency
    video.word_frequency = statistic_frequency(tokens)
    session.commit()
    return None


def duration_to_min(duration, ):
    """
    duration的例子PT3M32S,返回分钟数
    """
    import isodate
    _ = isodate.parse_duration(duration)
    return _.total_seconds()/60.0


# 获取所有词的原形，检查包含符号的词，并输出到文件中
def load_word_list(filename):
    import json
    with open(filename, "r") as f:
        _list = json.load(f)
    return set(_list)


# 根据CET6单词表，统计每个视频包含的CET6单词，统计总个数，存入数据库
def statistics_for_cet_six(video):
    # 加载单词表到内存 数据结构set
    word_set = load_word_list("cet_clean.json")
    from models import CetSixWordList, Video
    from transcript import get_word_baseform
    import json
    from models import db
    session = db.session
    video = session.query(Video).filter(Video.video_id == video.video_id).one()
    # 获取单个视频的所有词
    word_list = []
    session.add(video)
    for word in video.words:
        baseform = get_word_baseform(word.text)
        if baseform in word_set:
            word_list.append(baseform)
    cet_word = CetSixWordList(total_number=len(word_list),
                              word_list=json.dumps(word_list))
    session.add(cet_word)
    video.cet_six_word_list = cet_word
    session.commit()
    return None
    # 词性还原


def thread_pool(func, iterable, pool_size):
    from multiprocessing.dummy import Pool
    pool = Pool(pool_size)
    pool.map(func, iterable)
    pool.close()
    pool.join()

    return None


def process_pool(func, iterable, pool_size):
    from multiprocessing import Pool
    pool = Pool(pool_size)
    pool.map(func, iterable)
    pool.close()
    pool.join()
    return None


def main():

    from youtube import search_channels
    from models import Channel
    # 获取channel列表
    # channel_id_list = search_channels(50)
    # 下载channel的信息
    # thread_pool(download_channel_details, channel_id_list, 10)
    # 从上传列表id获取视频id列表
    # channel_list = Channel.query.all()
    # thread_pool(download_channel_video_list, channel_list, 10)
    # 下载视频id
    print "video_id done"
    # 基本信息
    from models import Video
    from models import db
    # video_list = db.session.query(Video).order_by(Video.id).all()
    # [download_video_detail(video) for video in video_list]
    # thread_pool(download_video_detail, video_list, 15)

    # 下载字幕 None表示没有下载，""代表没有
    # video_list = db.session.query(Video).filter(Video.xml_transcript == None).all()
    # [download_transcript(video) for video in video_list]
    # thread_pool(download_transcript, video_list, 10)

    # 分析字幕
    video_list = db.session.query(Video).filter(Video.xml_transcript.startswith("<")).all()
    # print "ok"
    # [analysis_transcript(video) for video in video_list]
    process_pool(analysis_transcript, video_list, 4)

    # CET6
    process_pool(statistics_for_cet_six, video_list, 2)


def restart():
    import requests

    try:
        main()
    except requests.exceptions.SSLError as e:
        print e
        import time
        time.sleep(120)
        restart()
    except requests.exceptions.ConnectionError as e:
        print e
        import time
        time.sleep(120)
        restart()
    except Exception as e:
        print e
if __name__ == '__main__':
    restart()
    # main()
    # from models import Video
    # video = Video.query.filter_by(video_id='xGSOVE20xa0').first()
    # download_video_detail(video)
    # download_transcript(video)