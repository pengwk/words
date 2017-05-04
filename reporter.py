#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This module does
    Date created: 4/20/2016
    Date last modified: 4/25/2016
    Python Version: 2.7.10
"""
from __future__ import print_function
from models import Video

__author__ = "pengwk"
__copyright__ = "Copyright 2016, pengwk"
__credits__ = [""]
__license__ = "Private"
__version__ = "0.1"
__maintainer__ = "pengwk"
__email__ = "pengwk2@gmail.com"
__status__ = "BraveHeart"


def main():

    return None


def report_video_():

    video_count = Video.query.count()
    details_count = Video.query.filter(Video.title != None).count()
    xml_count = Video.query.filter(Video.xml_transcript.startswith("<")).count()
    none_transcript = Video.query.filter(Video.xml_transcript == None).count()
    clean_transcript = Video.query.filter(Video.clean_transcript != None).count()

    report_str = u"视频总数：{}\n已下载视频资料数：{}\n有字幕数：{}尚未下载字幕数：{} 词频分析完成数：{}"
    print(report_str.format(video_count, details_count, xml_count, none_transcript, clean_transcript))
    return None


if __name__ == "__main__":
    report_video_()
