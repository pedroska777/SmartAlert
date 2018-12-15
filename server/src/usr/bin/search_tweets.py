#!/usr/bin/python
import tweepy as tw
import base64
import requests
import json
import datetime

consumer_key = "Rh7NKYaK9LIA4i8blBebqpOKD"
consumer_secret = "ZzZk11ErIyvS6y70hQzpdXJTZfhe47PFlgTQ32NTbxIq0nDmE6"

oauth_token = "1061405509608103936-UW7Hmga3BrqF6TgojuFy7qnygGBCbE"
oauth_token_secret = "oFyekKXqGgQmXcMUIzDTNvjjIxxvMtyD3jtT9xctOUXki"
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(oauth_token, oauth_token_secret)

api = tw.API(auth)

tweets = api.search(q="#fire", lang="en", return_json=False)
