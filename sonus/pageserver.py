
import config
from flask import Response, jsonify, render_template, request, g
import os
import json
from db import DB

import time

from threading import Timer

MIME_DICT = {
    "js": "text/javascript",
    "css": "text/css",
    "imgs": "image/png",
    "libraries": "text/javascript",
    "data": "text/csv",
    "sounds":  "audio/vnd.wav"
}

STATIC_DIR = "static/"


def get_db():
    if not hasattr(g, "db"):
        g.db = DB()
        g.db.connect()

    return g.db


@config.app.route("/<file_type>/<filename>", methods=["GET"])
def get_static(file_type, filename):
    with open(STATIC_DIR + file_type + "/" + filename) as f:
        res = Response(f.read(), mimetype=MIME_DICT[file_type])
        return res


@config.app.route("/", methods=["GET"])
def get_index():
    return render_template(
        "index.html"
    )


@config.app.route("/song", methods=["POST"])
def song():
    db = get_db()

    # form
    data = json.loads(request.data)
    userId = data.get('userId')
    songId = data.get('songId')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # add song if it does not exists
    db.add_song()

    # create user dict
    user = {
        'userId': userId,
        'location': {
            'latitude': latitude,
            'longitude': longitude
        },
        'time': time.time()
    }

    # create song dict
    song = {"songId": songId}
    song.setdefault('now', []).append(user)
    song.setdefault('total', []).append(user)

    # update song details (i.e. "now" and "total" fields)
    db.update_song({"songId": songId}, song)

    # remove user from now after certain time
    t = Timer(1000.0, remove_user_from_now, [userId, songId])
    t.start()

    return jsonify({'status': 'ok'})


@config.app.route("/desong", methods=["POST"])
def desong():
    # form
    userId = request.form.get('userId')
    songId = request.form.get('songId')

    # remove user from "now" field in song
    remove_user_from_now(userId, songId)


def remove_user_from_now(userId, songId):
    db = get_db()
    user = db.songs.find({'songId': songId, 'now.userId': userId})
    song = db.find_song({'songId': songId})
    song['all'].remove(user)
    db.update_song(song)


# @config.app.route("/songsNearMe", methods=["GET"])
# def songsNearMe():
#     db = get_db()
#
#     latitude = request.form.get('latitude')
#     longitude = request.form.get('longitude')
