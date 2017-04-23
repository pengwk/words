#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This module does
    Date created: 4/20/2017
    Date last modified: 4/25/2017
    Python Version: 2.7.10
"""

__author__ = "pengwk"
__copyright__ = "Copyright 2016, pengwk"
__credits__ = [""]
__license__ = "Private"
__version__ = "0.1"
__maintainer__ = "pengwk"
__email__ = "pengwk2@gmail.com"
__status__ = "BraveHeart"

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, JSON, Table, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship

MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "nopassword"
DB_NAME = "youtube_videos"

# 连接到MySQL数据库 格式dialect+driver://username:password@host:port/database
# UTF8支持 ?charset=utf8', encoding='utf-8'
eng = create_engine('mysql://root:nopassword@localhost/youtube_videos?charset=utf8', encoding='utf-8')

Base = declarative_base()

video_word_map_table = Table('video_word_maps', Base.metadata,
                             Column('video_id', Integer, ForeignKey('video.id')),
                             Column('word_id', Integer, ForeignKey('word.id'))
                             )

video_playlist_map_table = Table('video_playlist_maps', Base.metadata,
                                 Column('video_id', Integer, ForeignKey('video.id')),
                                 Column('playlist_id', Integer, ForeignKey('playlist.id'))
                                 )

video_tag_map_table = Table('video_tag_maps', Base.metadata,
                            Column('video_id', Integer, ForeignKey('video.id')),
                            Column('videotag_id', Integer, ForeignKey('videotag.id'))
                            )


class Video(Base):
    __tablename__ = "video"

    id = Column(Integer, primary_key=True)
    video_id = Column(String(20))
    title = Column(String(100))
    description = Column(Text)
    # 格式     YYYY-MM-DDThh:mm:ss.sZ
    published_at = Column(String(40))
    # 通过API获取的原始数据
    xml_transcript = Column(Text)
    # 不包含换行符
    clean_transcript = Column(Text)
    # todo 视频的字数，句子数，时长，短语，单词
    # 多对多
    words = relationship("Word",
                         secondary=video_word_map_table,
                         # you can also use the string name of the table, "maps", as the secondary
                         backref="videos")
    # 多个视频对应一个channel 多对一
    channel_id = Column(Integer, ForeignKey("channel.id"))
    channel = relationship('channel', bacdkref="video")

    # 一个列表多个视频，一个视频多个列表 多对多
    playlists = relationship("Playlist",
                             secondary=video_playlist_map_table,
                             backref="videos")

    # 总单词数
    word_number = Column(Integer)
    # 句子数量
    sentence_number = Column(Integer)
    # 语速
    speed = Column(String(20))
    # 词频
    word_frequency = Column(JSON)
    # 标签 多d对多
    tags = relationship("VideoTag",
                        secondary=video_tag_map_table,
                        backref="videos")
    # 缩略图
    thumbnails = Column(JSON)
    category_id = Column(Integer)
    # contentDetails
    duration = Column(String(20))
    dimension = Column(String(10))
    definition = Column(String(10))
    has_caption = Column(Boolean)
    is_licensed_content = Column(Boolean)
    projection = Column(String(20))
    # status
    license = Column(String(20))
    embedable = Column(Boolean)
    # 播放器url iframe
    player_url = Column(Text)
    # 统计
    view_count = Column(Integer)
    like_count = Column(Integer)
    dislike_count = Column(Integer)
    favorite_count = Column(Integer)
    comment_count = Column(Integer)
    # 包含的六级单词 一对一关系
    cet_six_word_list_id = Column(Integer, ForeignKey("CetSixWordList.id"))
    cet_six_word_list = relationship("CetSixWordList", backref="video", uselist=False)


class CetSixWordList(Base):
    __tablename__ = "cet_six_word_list"

    id = Column(Integer, primary_key=True)

    total_number = Column(Integer)
    word_list = Column(JSON)


class Word(Base):
    __tablename__ = "word"

    id = Column(Integer, primary_key=True)
    text = Column(String(30))
    phonetic = Column(String(30))
    base_form = Column(String(30))
    # times = Column(Integer)


class VideoTag(Base):
    __tablename__ = "video_tag"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))


class Channel(Base):
    __tablename__ = "channel"

    id = Column(Integer, primary_key=True)
    channel_id = Column(String(20))
    channel_title = Column(String(40))


class Playlist(Base):
    __tablename__ = "playlist"

    id = Column(Integer, primary_key=True)
    playlistId = Column(String(40))


class Listener(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    total_word_frequency = Column(JSON)


class WatchRecord(Base):
    __tablename__ = 'watch_record'

    id = Column(Integer, primary_key=True)
    listener = relationship("listener", backref="watch_records")
    listener_id = Column(Integer, ForeignKey("listener.id"))
    watch_time = Column(String(20))
    video_id = Column(Integer, ForeignKey("video.id"))
    video = relationship("video", backref="video", uselist=False)


Base.metadata.bind = eng
Base.metadata.create_all()


def test():
    session = sessionmaker(bind=eng)
    ses = session()
    c1 = Video(title='funny_video', description="What a beautiful!")
    ses.add(c1)
    ses.commit()

    videos = ses.query(Video).all()

    for video in videos:
        print video.title, video.description


class DataDealer:
    def __init__(self, username=MYSQL_USERNAME, password=MYSQL_PASSWORD, db_name=DB_NAME):
        self.username = username
        self.password = password
        self.db_name = db_name
        self.engine = create_engine('mysql://{}:{}@localhost/{}?charset=utf8'.format(self.username,
                                                                                     self.password,
                                                                                     self.db_name),
                                    encoding='utf-8')
        self.session = sessionmaker(bind=self.engine)()

    def add(self, video_item):
        self.session.add(video_item)
        self.session.commit()
        return None


def get_or_create(session, model, defaults=None, **kwargs):
    '''
    example usage:myCountry = get_or_create(session, Country, name=countryName) name:model's filed
    :param session:
    :param model:
    :param defaults:
    :param kwargs:
    :return:
    '''
    from sqlalchemy.sql import ClauseElement
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.iteritems() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True


def main():
    return None


if __name__ == "__main__":
    pass
    # test()
