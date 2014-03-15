
import config
from flask import Response, jsonify, render_template, request, g
import os
from db import DB

import time

from threading import Timer

MIME_DICT = {
    "js": "text/javascript",
    "css": "text/css",
    "imgs": "image/png",
    "libraries": "text/javascript",
    "data": "text/csv",
    "sounds":  "audio/vnd.wav",
    "fonts": "font/opentype"
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
    userId = request.form.get('userId')
    songId = request.form.get('songId')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    song = db.find_song({'songId': songId}) or db.add_song({'songId': songId})
    songObj = {
        'userId': userId,
        'location': {
            'latitude': latitude,
            'longitude': longitude
        },
        'time': time.time()
    }

    song.setdefault('now', []).append(songObj)
    song.setdefault('total', []).append(songObj)
    db.update_song(song)
    t = Timer(200.0, remove, [userId, songId])
    t.start()
    return jsonify({'status': 'ok'})


@config.app.route("/desong", methods=["POST"])
def desong():
    userId = request.form.get('userId')
    songId = request.form.get('songId')
    remove(userId, songId)


def remove(userId, songId):
    db = get_db()
    user = db.songs.find({'songId': songId, 'now.userId': userId})
    song = db.find_song({'songId': songId})
    song['all'].remove(user)
    db.update_song(song)

@config.app.route("/purge", methods=["GET"])
def purge():
    db = get_db()
    db.songs.remove()
    db.users.remove()
    return jsonify({'status': 'ok'})

# @config.app.route("/songsNearMe", methods=["GET"])
# def songsNearMe():
#     db = get_db()
#
#     latitude = request.form.get('latitude')
#     longitude = request.form.get('longitude')
