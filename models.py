#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This module does
    Date created: 4/20/2017
    Date last modified: 4/25/2017
    Python Version: 2.7.10
    alembic init alembic
    修改init文件
    修改env.py
    alembic revision --autogenerate -m "Added account db.Table"
    alembic upgrade head
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import LONGTEXT

import os
from flask import Flask, render_template_string
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter

__author__ = "pengwk"
__copyright__ = "Copyright 2016, pengwk"
__credits__ = [""]
__license__ = "Private"
__version__ = "0.1"
__maintainer__ = "pengwk"
__email__ = "pengwk2@gmail.com"
__status__ = "BraveHeart"


class ConfigClass(object):
    # Flask settings
    SECRET_KEY =              os.getenv('SECRET_KEY',       'THIS IS AN INSECURE SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',     'mysql+pymysql://root:nopassword@localhost/words_2?charset=utf8mb4')
    CSRF_ENABLED = True

    # Flask-Mail settings
    MAIL_USERNAME =           os.getenv('MAIL_USERNAME',        'handsome_boy@pengwk.com')
    MAIL_PASSWORD =           os.getenv('MAIL_PASSWORD',        'W#ER$RFS#RT*1d')
    MAIL_DEFAULT_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',  '"handsome_boy" <handsome_boy@pengwk.com>')
    MAIL_SERVER =             os.getenv('MAIL_SERVER',          'smtp.exmail.qq.com')
    MAIL_PORT =           int(os.getenv('MAIL_PORT',            '465'))
    MAIL_USE_SSL =        int(os.getenv('MAIL_USE_SSL',         True))

    # Flask-User settings
    USER_APP_NAME        = u"静听"                # Used by email templates

app = Flask(__name__,
            static_url_path='/static',
            template_folder='./templates',
            )
app.config.from_object(__name__+'.ConfigClass')
mail = Mail(app)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

video_word_map_table = db.Table('video_word_maps',
                                db.Column('video_id', db.Integer, db.ForeignKey('video.id')),
                                db.Column('word_id', db.Integer, db.ForeignKey('word.id'))
                                )

video_playlist_map_table = db.Table('video_playlist_maps',
                                    db.Column('video_id', db.Integer, db.ForeignKey('video.id')),
                                    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'))
                                    )

video_tag_map_table = db.Table('video_tag_maps',
                               db.Column('video_id', db.Integer, db.ForeignKey('video.id')),
                               db.Column('video_tag_id', db.Integer, db.ForeignKey('video_tag.id'))
                               )


class Video(db.Model):
    __tablename__ = "video"

    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String(20), unique=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    # 格式     YYYY-MM-DDThh:mm:ss.sZ
    published_at = db.Column(db.String(40))
    # 通过API获取的原始数据
    xml_transcript = db.Column(LONGTEXT)
    # 不包含换行符
    clean_transcript = db.Column(LONGTEXT)
    # 视频的字数，句子数，时长，短语，单词
    # 多对多
    words = db.relationship("Word",
                            secondary=video_word_map_table,
                            # you can also use the db.String name of the db.Table, "maps", as the secondary
                            backref="videos")
    # 多个视频对应一个channel 多对一
    channel_id = db.Column(db.Integer, db.ForeignKey("channel.id"))
    channel = db.relationship('Channel', backref="video")

    _channel_id = db.Column(db.String(60))
    _channel_title = db.Column(db.String(100))

    # 一个列表多个视频，一个视频多个列表 多对多
    playlists = db.relationship("Playlist",
                                secondary=video_playlist_map_table,
                                backref="videos")

    # 总单词数
    word_number = db.Column(db.Integer)
    # 句子数量
    sentence_number = db.Column(db.Integer)
    # 语速
    speed = db.Column(db.String(20))
    # 词频
    word_frequency = db.Column(db.JSON)
    # 标签 多d对多
    tags = db.relationship("VideoTag",
                           secondary=video_tag_map_table,
                           backref="videos")
    _tags = db.Column(db.JSON)
    # 缩略图
    thumbnails = db.Column(db.JSON)
    category_id = db.Column(db.Integer)
    # contentDetails
    duration = db.Column(db.String(20))
    dimension = db.Column(db.String(10))
    definition = db.Column(db.String(10))
    has_caption = db.Column(db.Boolean)
    is_licensed_content = db.Column(db.Boolean)
    projection = db.Column(db.String(20))
    # status
    license = db.Column(db.String(20))
    embedable = db.Column(db.Boolean)
    # 播放器url iframe
    player_url = db.Column(db.Text)
    # 统计
    view_count = db.Column(db.BigInteger)
    like_count = db.Column(db.Integer)
    dislike_count = db.Column(db.Integer)
    favorite_count = db.Column(db.Integer)
    comment_count = db.Column(db.Integer)
    # 包含的六级单词 一对一关系
    cet_six_word_list_id = db.Column(db.Integer, db.ForeignKey("cet_six_word_list.id"))
    cet_six_word_list = db.relationship("CetSixWordList", backref="video", uselist=False)


class CetSixWordList(db.Model):
    __tablename__ = "cet_six_word_list"

    id = db.Column(db.Integer, primary_key=True)

    total_number = db.Column(db.Integer)
    word_list = db.Column(db.JSON)


class Word(db.Model):
    __tablename__ = "word"

    id = db.Column(db.Integer, primary_key=True)
    text= db.Column(db.String(30), unique=True)
    phonetic = db.Column(db.String(30))
    base_form = db.Column(db.String(30))
    # times = db.Column(db.Integer)


class VideoTag(db.Model):
    __tablename__ = "video_tag"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)


class Channel(db.Model):
    __tablename__ = "channel"

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.String(40), unique=True)
    channel_title = db.Column(db.Text)
    description = db.Column(db.Text)
    # 2009-10-01T17:49:50.000Z
    published_at = db.Column(db.String(24))
    # contentDetails
    playlist_likes = db.Column(db.String(30))
    playlist_uploads = db.Column(db.String(30))
    # topicDetails
    topic_details = db.Column(db.JSON)
    # topicCategories
    topic_categories = db.Column(db.JSON)
    # branding_settings
    branding_settings = db.Column(db.JSON)
    status = db.Column(db.JSON)
    # statistics brandingSettings,contentDetails,contentOwnerDetails,invideoPromotion,localizations,status,topicDetails
    view_count = db.Column(db.BigInteger)
    comment_count = db.Column(db.BigInteger)
    subscriber_count = db.Column(db.BigInteger)
    hidden_subscriber_count = db.Column(db.Boolean)
    video_count = db.Column(db.Integer)
    #
    thumbails = db.Column(db.JSON)


class Playlist(db.Model):
    __tablename__ = "playlist"

    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.String(40), unique=True)


class Listener(db.Model):
    __tablename__ = 'listener'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    total_word_frequency = db.Column(db.JSON)


class WatchRecord(db.Model):
    __tablename__ = 'watch_record'

    id = db.Column(db.Integer, primary_key=True)
    listener_id = db.Column(db.Integer, db.ForeignKey("listener.id"))
    listener = db.relationship("Listener", backref="watch_records")
    watch_time = db.Column(db.String(20))
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"))
    video = db.relationship("Video", backref="video", uselist=False)

# Define User DataModel
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # User email information
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    # User information
    is_enabled = db.Column(db.Boolean(), nullable=False, default=False)
    first_name = db.Column(db.String(50), nullable=False, default='')
    last_name = db.Column(db.String(50), nullable=False, default='')

    def is_active(self):
      return self.is_enabled

# Define UserAuth DataModel. Make sure to add flask_user UserMixin!!
class UserAuth(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))

    # User authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')

    # Relationships
    user = db.relationship('User', uselist=False, foreign_keys=user_id)


# Setup Flask-User
db_adapter = SQLAlchemyAdapter(db, User, UserAuthClass=UserAuth)
user_manager = UserManager(db_adapter, app)


def test_db():
    from database import get_or_create
    video, flag = get_or_create(db.session, Video, id=1)
    print video.video_id

if __name__ == "__main__":
    db.create_all()
    # test_db()
    pass
    # test()
