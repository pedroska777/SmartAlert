#!/usr/bin/python
import tweepy as tw
import base64
import requests
import json
import datetime

consumer_key = CONSUMER_KEY
consumer_secret = CONSUMER_SECRET

oauth_token = ACCESS_TOKEN
oauth_token_secret = ACCESS_TOKEN_SECRET
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(oauth_token, oauth_token_secret)

api = tw.API(auth)

tweets = api.search(q="#fire", lang="en", return_json=False)
