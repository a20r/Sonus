
import config
from flask import Response, jsonify, render_template, request
import os

MIME_DICT = {
    "js": "text/javascript",
    "css": "text/css",
    "imgs": "image/png",
    "libraries": "text/javascript",
    "data": "text/csv",
    "sounds":  "audio/vnd.wav"
}

STATIC_DIR = "static/"

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

@config.app.route("/userLoggedIn", methods=["POST"])
def userLoggedIn():
    print 'user logged in ',request.form['id']
    return jsonify({'status':'ok'})




