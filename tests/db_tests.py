#!/usr/bin/env python
import os
import sys
import time
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from sonus.db import DB


class UnitTests(unittest.TestCase):
    def setUp(self):
        self.db = DB()

    def test_connect(self):
        self.db.connect()
        self.db.disconnect()

    def test_users(self):
        self.db.connect()

        # test add and select
        user = {"username": "chris"}
        self.db.add_user(user)
        result = self.db.find_user(user)

        # test remove
        self.db.remove_user(user)
        result_2 = self.db.find_user(user)

        self.assertEquals(user, result)
        self.assertIsNone(result_2)

    def test_songs(self):
        self.db.connect()

        # test add and select
        song = {
            'userId': "chris",
            'songId': "12345",
            'location': {
                'latitude': 10,
                'longitude': 20
            },
            'time': time.time()
        }
        self.db.get_or_create_song(song)
        print "SONGS:", self.db.find_song({})
        # result = self.db.find_song(song)

        # self.assertEquals(song, result)

        # # test remove
        # self.db.remove_song(song)
        # result_2 = self.db.find_song(song)

        # self.assertIsNone(result_2)

    def test_find_songs(self):
        self.db.connect()

        song_1 = {
            'userId': "chris",
            'songId': "12345",
            'location': {
                'latitude': 10,
                'longitude': 20
            },
            'time': time.time()
        }
        song_2 = {
            'userId': "chris",
            'songId': "123456",
            'location': {
                'latitude': 10,
                'longitude': 20
            },
            'time': time.time()
        }
        self.db.get_or_create_song(song_1)
        self.db.get_or_create_song(song_2)

        self.db.find_song(
            {
                'location.latitude': {"$lt": 11, "$gt": 9},
                'location.longitude': {"$lt": 21, "$gt": 19},
            }
        )

        self.db.remove_song(song_1)
        self.db.remove_song(song_2)


if __name__ == "__main__":
    unittest.main()
