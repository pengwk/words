#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This module does
    Date created: 4/20/2016
    Date last modified: 4/25/2016
    Python Version: 2.7.10
    编写一个函数可以把整个播放列表全部下载下来，
    get_whole_playlist(playListId)
"""

__author__ = "pengwk"
__copyright__ = "Copyright 2016, pengwk"
__credits__ = [""]
__license__ = "Private"
__version__ = "0.1"
__maintainer__ = "pengwk"
__email__ = "pengwk2@gmail.com"
__status__ = "BraveHeart"

from pprint import pprint


import requests
import json


DEVELOPER_KEY = "AIzaSyCWxbyw93TpHw_SSZUq6VPlU8EYzbQ8BAw"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

CHANNEL_NAME = "Seeker Daily"
CHANNEL_ID = "UCgRvm1yLFoaQKhmaTqXk9SA"

PART_VALUES = ["contentDetails", "snippet"]


def get_uploads_list_id(channel_id):
    """获取频道的上传列表ID"""
    result = requests.get("https://www.googleapis.com/youtube/v3/channels",
                          params={
                              "key": DEVELOPER_KEY,
                              "part": PART_VALUES[0],
                              "id": channel_id
                          }
                          )
    uploads_list_id = result.json()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    return uploads_list_id


def search_channels(max_channel_count):
    part = "id"
    channel_list = []
    result = requests.get("https://www.googleapis.com/youtube/v3/search",
                          params={
                              "key": DEVELOPER_KEY,
                              "part": part,
                              "maxResults": 50,
                              "type": "channel",
                              "relevanceLanguage": "en",
                              "safeSearch": "strict",
                          }
                          )
    while 1:
        channel_list.extend(result.json()['items'])
        if len(channel_list) >= max_channel_count:
            break
        try:
            pageToken = result.json()['nextPageToken']
        except KeyError as e:
            break
        result = requests.get("https://www.googleapis.com/youtube/v3/search",
                              params={
                                  "key": DEVELOPER_KEY,
                                  "part": part,
                                  "maxResults": 50,
                                  "type": "channel",
                                  "relevanceLanguage": "en",
                                  "safeSearch": "strict",
                                  "pageToken": pageToken
                              })

    return [channel.get("id").get("channelId") for channel in channel_list]


def get_channel_details(channel_id):
    """
    invideoPromotion
    :param channel_id:
    :return:
    """
    part = "snippet,statistics,brandingSettings,contentDetails,contentOwnerDetails,localizations,status," \
           "topicDetails"
    result = requests.get("https://www.googleapis.com/youtube/v3/channels",
                          params={
                              "key": DEVELOPER_KEY,
                              "part": part,
                              "id": channel_id
                          }
                          )
    return result.json()["items"]


def get_playlist_items(playlist_id):
    """获取整个播放列表的内容
    video_list = [video_id,]
    """
    # todo 性能优化
    video_list = []
    result = requests.get("https://www.googleapis.com/youtube/v3/playlistItems",
                          params={
                              "key": DEVELOPER_KEY,
                              "part": PART_VALUES[0],
                              "playlistId": playlist_id,
                              "maxResults": 50
                          })

    while 1:
        video_list.extend(result.json()['items'])
        try:
            pageToken = result.json()['nextPageToken']
        except KeyError as e:
            break
        result = requests.get("https://www.googleapis.com/youtube/v3/playlistItems",
                              params={
                                  "key": DEVELOPER_KEY,
                                  "part": PART_VALUES[0],
                                  "playlistId": playlist_id,
                                  "maxResults": 50,
                                  "pageToken": pageToken
                                    }
                              )
    
    return [video.get("contentDetails").get("videoId") for video in video_list]


def test_playlist_items():
    list_id = "PLSQl0a2vh4HAbVPn5Gbugtg1o5hfdzEH1"
    pprint(get_playlist_items(list_id))


def get_xml_transcript(video_id, lang="en"):
    """
    字幕不存在时返回""空字符串
    youtube-dl --skip-download --id --sub-lang en https://www.youtube.com/watch?v=jJ_Zejm7LQE
    --write-sub                      Write subtitle file
--write-auto-sub                 Write automatically generated subtitle file
                                 (YouTube only)
--all-subs                       Download all the available subtitles of the
                                 video
--list-subs                      List all available subtitles for the video
--sub-format FORMAT              Subtitle format, accepts formats
                                 preference, for example: "srt" or
                                 "ass/srt/best"
--sub-lang LANGS                 Languages of the subtitles to download
                                 (optional) separated by commas, use --list-
                                 subs for available language tags

    """
    import requests
    from bs4 import BeautifulSoup

    api_url = "http://video.google.com/timedtext"
    _raw_response = requests.get(api_url, params={"lang": lang, "v": video_id})
    return _raw_response.content


def test_xml_transcript():
    no_transcript_video = "qOKwU5BYK08"
    has_transcript_video = "ytkt2YxGou4"
    no_caption_but_asr = "aXufzJ-Vp8g"
    print get_xml_transcript(no_caption_but_asr) == ""


def get_video_detail(video_id):
    """
    上传者本人才能访问
    suggestions: 1
    processingDetails: 1
    recordingDetails: 2
    fileDetails: 1
    无需授权
    contentDetails: 2
    id: 0
    liveStreamingDetails: 2
    localizations: 2
    player: 0
    snippet: 2
    statistics: 2
    status: 2
    topicDetails: 2

    """
    part = "status,snippet,statistics,player,contentDetails"
    result = requests.get("https://www.googleapis.com/youtube/v3/videos",
                          params={
                              "key": DEVELOPER_KEY,
                              "part": part,
                              "id": video_id,
                          })
    item = result.json()["items"][0]
    return item


def test_video_detail():
    video_id = "ytkt2YxGou4"
    print get_video_detail(video_id)

if __name__ == '__main__':
    print len(search_channels(100))
    # test_video_detail()
    # test_playlist_items()

