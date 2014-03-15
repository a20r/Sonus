
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
    print request.form
    userId = request.form.get('userId')
    songId = request.form.get('songId')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    
    song = db.get_or_create_song(songId)

    songObj = {'userId': userId,
               'location': {'latitude': latitude,
                            'longitude': longitude},
               'time': time.time()}
    song.setdefault('now',{})[userId] = songObj
    song.setdefault('total',{})[userId] = songObj
    db.update_song(song)
    t = Timer(200.0, remove, [songObj, songId])
    t.start()


    return jsonify({'status': 'ok'})


@config.app.route("/desong", methods=["POST"])
def desong():
    db = get_db()
    userId = request.form.get('userId')
    songId = request.form.get('songId')

    song = db.get_or_create_song(songId)
    if userId in song['now'].keys():
        del song['now'][userId]
    db.update_song(song)
    


def remove(songObj):
    db = get_db()
    song = db.get_or_create_song(songId)
    if songObj['userId'] in song['now'].keys():
        del song['now'][songObj['userId']]
