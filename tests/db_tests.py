#!/usr/bin/env python
import os
import sys
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
        song = {"title": "Hello World"}
        self.db.add_song(song)
        result = self.db.find_song(song)

        # test remove
        self.db.remove_song(song)
        result_2 = self.db.find_song(song)

        self.assertEquals(song, result)
        self.assertIsNone(result_2)


if __name__ == "__main__":
    unittest.main()
