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

# 数据库连接
def create_session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    eng = create_engine('mysql://root:nopassword@localhost/words?charset=utf8',
                        encoding='utf-8')

    session = sessionmaker(bind=eng)
    return session()

# 首先，定义一个频道列表
# 获取单个频道里的上传列表

# 获取列表中所有的视频id，将上传列表与视频存入数据库，加入外键关系

# 将频道列表中的所有频道完成这一步
def download_channel_video_list(channel_id):
    # 获取上传列表Id
    from youtube import get_uploads_list_id,get_playlist_items

    upload_list_id = get_uploads_list_id(channel_id)
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
    video.xml_transcript = dt(video.id)
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
    from models import Word, get_or_create
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
        session.commit()
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
    from models import Video
    session = create_session()
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