#!/usr/bin/env python
import pymongo


class DB(object):

    def __init__(self, **kwargs):
        self.host = kwargs.get("host", "localhost")
        self.port = kwargs.get("port", "27017")
        self.state = "IDLE"
        self.client = None

    def connect(self):
        db_url = 'mongodb://{0}:{1}/'.format(self.host, self.port)
        self.client = pymongo.MongoClient(db_url)
        self.state = "CONNECTED"
        db = self.client["sonus"]

        # collections
        self.users = db["users"]
        self.songs = db["songs"]

    def disconnect(self):
        if self.state == "CONNECTED":
            self.client.disconnect()
            self.state = "DISCONNECTED"

    def purge(self):
        self.users.remove()
        self.songs.remove()

    # SONG FUNCTIONS
    def add_song(self, song):
        if self.find_song(song) is None:
            self.songs.insert(song)

    def remove_song(self, song):
        self.songs.remove(song)

    def update_song(self, old, new):
        self.songs.update(old, new, upsert=True)

    def find_song(self, song):
        result = self.songs.find_one(song)
        return result

    def find_songs(self, song):
        result = self.songs.find(song)
        return result

    # USER FUNCTIONS
    def add_user(self, user):
        if self.find_user(user) is None:
            self.users.insert(user)

    def remove_user(self, user):
        self.users.remove(user)

    def find_user(self, user):
        result = self.users.find_one(user)
        return result
