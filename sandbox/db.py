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

    def disconnect(self):
        if self.state == "CONNECTED":
            self.client.disconnect()
            self.state = "DISCONNECTED"

    def return_collections(self):
        if self.state == "IDLE" or self.state == "DISCONNECTED":
            raise RuntimeError("Not connected to database!")

        else:
            collections = {}

            db = self.client.streamy
            collections = {
                "tweets": db.tweets,
                "rss": db.rss,
                "result": db.result
            }

            return collections
