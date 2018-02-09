#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This module does
    Date created: 4/20/2016
    Date last modified: 4/25/2016
    Python Version: 2.7.10
"""
from flask import Flask, request, send_from_directory
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter, current_user

__author__ = "pengwk"
__copyright__ = "Copyright 2016, pengwk"
__credits__ = [""]
__license__ = "Private"
__version__ = "0.1"
__maintainer__ = "pengwk"
__email__ = "pengwk2@gmail.com"
__status__ = "BraveHeart"

# set the project root directory as the static folder, you can set others.
from models import app, User
from models import Video, db, History
from flask import render_template


import bug2butterfly

raise IOError('Hi')

@app.route("/")
def hello():
    print current_user
    print current_user.is_anonymous
    return render_template('index.html')


@app.route("/home")
@login_required
def home():
    watched_videos = current_user.watched_videos

    videos = db.session.query(Video).filter(Video.xml_transcript != "",
                                            ~Video.id.in_([video.id for video in watched_videos])
                                            )
    return render_template("home.html",
                           recommend_videos=videos[0:3],
                           slides_videos=videos[4:16],
                           bottom_videos=videos[17:25],
                           )


# werghWD0_
@app.route("/watch")
@login_required
def watch_video():
    video_id = request.args.get("v")
    video = db.session.query(Video).filter(Video.video_id == video_id).one()
    import json
    frequency = json.loads(video.word_frequency)
    keys = json.dumps(frequency.keys())
    # 增加历史记录
    history = History(video=video, user=current_user)
    db.session.add(history)
    db.session.commit()
    # 增加watched_video
    current_user.watched_videos.append(video)
    db.session.commit()
    return render_template("watch.html", video=video, frequency=frequency, keys=keys)


@app.route("/i")
@login_required
def i():
    return render_template("i.html")


@app.route("/history")
@login_required
def history():
    return render_template("history.html", videos=current_user.watched_videos)


@app.route("/statistics")
@login_required
def statistics():
    data = {}
    watched_videos = current_user.watched_videos
    data["total_videos"] = len(watched_videos)
    data["total_words"] = sum(video.word_number for video in watched_videos)
    from main import duration_to_min
    data["total_time"] = sum(duration_to_min(video.duration) for video in watched_videos)
    return render_template("statistics.html", data=data)


@app.route("/try/home")
def try_home():
    videos = db.session.query(Video).filter(Video.xml_transcript != "")
    return render_template("home.html",
                           recommend_videos=videos[0:3],
                           slides_videos=videos[4:16],
                           bottom_videos=videos[17:25],
                           )


# werghWD0_
@app.route("/try/watch")
def try_watch_video():
    video_id = request.args.get("v")
    video = db.session.query(Video).filter(Video.video_id == video_id).one()
    import json
    frequency = json.loads(video.word_frequency)
    keys = json.dumps(frequency.keys())
    # 增加历史记录
    history = History(video=video, user=current_user)
    db.session.add(history)
    db.session.commit()
    # 增加watched_video
    current_user.watched_videos.append(video)
    db.session.commit()
    return render_template("watch.html", video=video, frequency=frequency, keys=keys)


@app.route("/try/i")
def try_i():
    return render_template("i.html")


@app.route("/try/history")
def try_history():
    return render_template("history.html", videos=current_user.watched_videos)


@app.route("/try/statistics")
def try_statistics():
    data = {}
    watched_videos = current_user.watched_videos
    data["total_videos"] = len(watched_videos)
    data["total_words"] = sum(video.word_number for video in watched_videos)
    from main import duration_to_min
    data["total_time"] = sum(duration_to_min(video.duration) for video in watched_videos)
    return render_template("statistics.html", data=data)


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
