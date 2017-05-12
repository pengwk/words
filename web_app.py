#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This module does
    Date created: 4/20/2016
    Date last modified: 4/25/2016
    Python Version: 2.7.10
"""
from flask import Flask, request, send_from_directory
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter

__author__ = "pengwk"
__copyright__ = "Copyright 2016, pengwk"
__credits__ = [""]
__license__ = "Private"
__version__ = "0.1"
__maintainer__ = "pengwk"
__email__ = "pengwk2@gmail.com"
__status__ = "BraveHeart"

# set the project root directory as the static folder, you can set others.
from models import app

@app.route("/")
def hello():
    return app.send_static_file('cover/index.html')


from flask import render_template


@app.route("/home")
def videos():
    from models import Video, db
    videos = db.session.query(Video).filter(Video.xml_transcript!="").all()
    return render_template("home.html",
                           recommend_videos=videos[0:3],
                           slides_videos=videos[4:16],
                           bottom_videos=videos[17:25],
                           )


@app.route("/watch")
# @login_required
def watch_video():
    from models import Video, db
    video_id = request.args.get("v")
    video = db.session.query(Video).filter(Video.video_id==video_id).one()
    import json
    frequency = json.loads(video.word_frequency)
    keys = json.dumps(frequency.keys())
    return render_template("watch.html", video=video, frequency=frequency, keys=keys)


@app.route("/i")
def i():
    return "I"


@app.route("/history")
def history():
    return "history"


@app.route("/statistics")
def statistics():
    return "statistics"


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

    
