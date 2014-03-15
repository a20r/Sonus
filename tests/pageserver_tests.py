#!/usr/bin/env python
import os
import sys
import requests
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from sonus.db import DB


class UnitTests(unittest.TestCase):

    def setUp(self):
        self.url = "http://127.0.0.1:8000"
        self.db = DB()
        self.db.connect()

        test_songs = [
            {
                "songId": "1",
                "total": [
                    {
                        "userId": "1",
                        "location": {
                            "latitude": 37.782551,
                            "longitude": -122.445368
                        }
                    },
                    {
                        "userId": "2",
                        "location": {
                            "latitude": 37.782745,
                            "longitude": -122.444586
                        }
                    }
                ]
            },
            {
                "songId": "2",
                "total": [
                    {
                        "userId": "3",
                        "location": {
                            "latitude": 37.782842,
                            "longitude": -122.443688
                        },
                    },
                    {
                        "userId": "4",
                        "location": {
                            "latitude": 37.782919,
                            "longitude": -122.442815
                        }
                    }
                ]
            },
            {
                "songId": "3",
                "total": [
                    {
                        "userId": "5",
                        "location": {
                            "latitude": 37.782992,
                            "longitude": -122.442112
                        },
                    },
                    {
                        "userId": "6",
                        "location": {
                            "latitude": 37.783206,
                            "longitude": -122.440829
                        }
                    }
                ]
            },
            {
                "songId": "4",
                "total": [
                    {
                        "userId": "7",
                        "location": {
                            "latitude": 37.753837,
                            "longitude": -122.403172
                        }
                    },
                    {
                        "userId": "8",
                        "location": {
                            "latitude": 37.752986,
                            "longitude": -122.403112
                        }
                    },
                    {
                        "userId": "9",
                        "location": {
                            "latitude": 37.751266,
                            "longitude": -122.403355
                        }
                    }
                ]
            }
        ]
        for s in test_songs:
            self.db.add_song(s)

    def tearDown(self):
        self.db.disconnect()
        self.db.purge()

    def rest_post(self, url, data):
        return requests.post(url, data)

    def rest_get(self, url):
        return requests.get(url)

    def test_song(self):
        url = os.path.join(self.url, "song")
        form = {
            "userId": "chris",
            "songId": "12345",
            "latitude": "10",
            "longitude": "20"
        }
        self.rest_post(url, form)

        # assert
        userId = form["userId"]
        songId = form["songId"]
        song = self.db.find_song({"songId": songId})
        self.assertTrue(song['now'][0]["userId"] == userId)
        self.assertTrue(song['total'][0]["userId"] == userId)

    def test_desong(self):
        # add test song
        url = os.path.join(self.url, "song")
        form = {
            "userId": "chris",
            "songId": "12345",
            "latitude": "10",
            "longitude": "20"
        }
        self.rest_post(url, form)

        # desong
        url = os.path.join(self.url, "desong")
        form = {
            "userId": "chris",
            "songId": "12345",
        }
        self.rest_post(url, form)
        song = self.db.find_song({"songId": "12345"})

        # assert
        self.assertTrue(len(song["now"]) == 0)

    def test_near(self):
        songs = self.db.find_songs({})
        songs = [i for i in songs]
        # print "LENGTH", len(songs)

        near_url = os.path.join(
            self.url,
            "near",
            "37.782551",
            "-122.445368",
            "1"
        )
        result = self.rest_get(near_url)
        print result.text


if __name__ == "__main__":
    unittest.main()
