#!/usr/bin/env python
import json
import random

import soundcloud

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream, API


if __name__ == "__main__":
    # client_id = "0020643627fb540d480f7c4434796d2c"
    # client = soundcloud.Client(client_id=client_id)

    # # users = client.get("/users", q="London", limit=200, offset=100)
    # users = client.get("/users", q="London", limit=50, offset=100)
    # print "LENGTH:", len(users)
    # print users[0].keys()

    # for user in users:
    #     print user.username

    # Go to http://dev.twitter.com and create an app.
    # The consumer key and secret will be generated for you after
    # consumer_key = "bqyKjzTjaQpKEDZ7blcuIg"
    # consumer_secret = "f3NFp8ZucXMibQvq9j24VTmXVtQlyhIoqt3z6Uw4ms"

    # # After the step above, you will be redirected to your app's page.
    # # Create an access token under the the "Your access token" section
    # access_token = "14113807-VrdngSdnYVhVx9ja1GvROt2Dd3FEWqnWRR6Y3XxBf"
    # access_token_secret = "jHR0rd8tCvSjpx4hdlj69cdYiY1HWHVpoktqZcsKf2WZw"

    # auth = OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    # api = API(auth)

    # user = api.get_user(screen_name="FourTet")
    # print user.name
    # print user.location
