#!/usr/bin/env python
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from streamy.db import DB


class UnitTests(unittest.TestCase):
    def setUp(self):
        self.db = DB()

    def test_connect(self):
        self.db.connect()
        self.db.disconnect()

    def db_return_collection(self):
        collections = self.db.return_collections()

        self.assertTrue(collections is not None)
        self.assertTrue(collections["tweets"] is not None)
        self.assertTrue(collections["rss"] is not None)


if __name__ == "__main__":
    unittest.main()
