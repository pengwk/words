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
from __future__ import print_function
from pprint import pprint


import requests

requests.packages.urllib3.disable_warnings()

__author__ = "pengwk"
__copyright__ = "Copyright 2016, pengwk"
__credits__ = [""]
__license__ = "Private"
__version__ = "0.1"
__maintainer__ = "pengwk"
__email__ = "pengwk2@gmail.com"
__status__ = "BraveHeart"

# for EOF ERROR

import ssl
from functools import wraps


def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)

    return bar


ssl.wrap_socket = sslwrap(ssl.wrap_socket)

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
                          },
                          verify=False,
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
                          },
                          verify=False,

                          )
    while 1:
        channel_list.extend(result.json()['items'])
        if len(channel_list) >= max_channel_count:
            break
        try:
            page_token = result.json()['nextPageToken']
        except KeyError:
            break
        result = requests.get("https://www.googleapis.com/youtube/v3/search",
                              params={
                                  "key": DEVELOPER_KEY,
                                  "part": part,
                                  "maxResults": 50,
                                  "type": "channel",
                                  "relevanceLanguage": "en",
                                  "safeSearch": "strict",
                                  "pageToken": page_token
                              },
                              verify=False, )

    return [channel.get("id").get("channelId") for channel in channel_list]


def search_videos(max_video_count):
    """
    200M内存可以装44500个id
    :return: a list such as ["ididi", "idididid"]

    result.json() 的结构
    {u'etag': u'"m2yskBQFythfE4irbTIeOgYYfBU/ZNdWTsc0Ju8PukbfXV3eGecnklA"',
    u'items': [
            {u'etag': u'"m2yskBQFythfE4irbTIeOgYYfBU/BDEfjpY3JDutURWxdJdJ8calYuA"',
             u'id': {u'kind': u'youtube#video', u'videoId': u'nSDgHBxUbVQ'},
             u'kind': u'youtube#searchResult'},
            {u'etag': u'"m2yskBQFythfE4irbTIeOgYYfBU/zuVoF_UgDzKd4rLZUAnv2ICc594"',
             u'id': {u'kind': u'youtube#video', u'videoId': u'c4BLVznuWnU'},
             u'kind': u'youtube#searchResult'},
            {u'etag': u'"m2yskBQFythfE4irbTIeOgYYfBU/c9HMnuzitTzhAJSX2G9KBFLgRUQ"',
             u'id': {u'kind': u'youtube#video', u'videoId': u'GjkFr48jk68'},
             u'kind': u'youtube#searchResult'},
            {u'etag': u'"m2yskBQFythfE4irbTIeOgYYfBU/s08U9XV9EZ4Zb1cowMMCr1FduxM"',
             u'id': {u'kind': u'youtube#video', u'videoId': u'_GgfLZFj6kM'},
             u'kind': u'youtube#searchResult'}
             ],
    u'kind': u'youtube#searchListResponse',
    u'nextPageToken': u'CDIQAA',
    u'pageInfo': {u'resultsPerPage': 50, u'totalResults': 1000000},
    u'regionCode': u'JP'}
    """
    part = "id"
    search_url = "https://www.googleapis.com/youtube/v3/search"
    commond_params = {"key": DEVELOPER_KEY,
                      "part": part,
                      "videoCaption": "closedCaption",
                      "maxResults": 50,
                      "type": "video",
                      "relevanceLanguage": "en",
                      "safeSearch": "strict",
                      "regionCode": "US"
                      }
    video_list = []
    result = requests.get(search_url,
                          params=commond_params,
                          verify=False,
                          )
    while 1:
        try:
            video_list.extend(result.json()['items'])
        except KeyError:
            pprint(result.json())
        if len(video_list) >= max_video_count:
            break
        try:
            page_token = result.json()['nextPageToken']
            commond_params.update({"pageToken": page_token})
        except KeyError:
            break

        result = requests.get(search_url,
                              params=commond_params,
                              verify=False, )
    return [item.get("id").get("videoId") for item in video_list]


def test_search_videos():
    pprint(search_videos(200))


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
                          },
                          verify=False,
                          )
    return result.json()["items"][0]


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
                          },
                          verify=False,
                          )

    while 1:
        try:
            video_list.extend(result.json()['items'])
        except KeyError:
            pprint(playlist_id)
            pprint(result.json())
        try:
            page_token = result.json()['nextPageToken']
        except KeyError:
            break
        result = requests.get("https://www.googleapis.com/youtube/v3/playlistItems",
                              params={
                                  "key": DEVELOPER_KEY,
                                  "part": PART_VALUES[0],
                                  "playlistId": playlist_id,
                                  "maxResults": 50,
                                  "pageToken": page_token
                              },
                              verify=False,
                              )

    return [video.get("contentDetails").get("videoId") for video in video_list]


def test_playlist_items():
    list_id = "PLSQl0a2vh4HAbVPn5Gbugtg1o5hfdzEH1"
    pprint(get_playlist_items(list_id))


def get_xml_transcript(video_id, lang="en"):
    """
    字幕不存在时返回""空字符串
    """
    import requests

    api_url = "http://video.google.com/timedtext"
    _raw_response = requests.get(api_url, params={"lang": lang, "v": video_id})
    return _raw_response.content


def test_xml_transcript():
    # no_transcript_video = "qOKwU5BYK08"
    # has_transcript_video = "ytkt2YxGou4"
    no_caption_but_asr = "aXufzJ-Vp8g"
    print(get_xml_transcript(no_caption_but_asr) == "")


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
                          },
                          verify=False, )
    items = result.json().get("items")
    from pprint import pprint
    # pprint(items)
    # google api 会出现错误，要包含这个不然发出错误的会配额已满消息
    if items is None:
        raise Exception("Quotas have reached")
    return items[0]


def test_video_detail():
    video_id = "ytkt2YxGou4"
    print(get_video_detail(video_id))


if __name__ == '__main__':
    test_search_videos()
    # print(len(search_channels(100)))
    # test_video_detail()
    # test_playlist_items()
