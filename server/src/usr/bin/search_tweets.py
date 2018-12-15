#!/usr/bin/python
import tweepy as tw
import base64
import requests
import json
import datetime

def get_oauth_handle():
  auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
  auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
  
  return auth

def get_api_instance():
  auth = get_oauth_handle()
  return tw.API(auth)

def get_tweets_by_keyword(key_word):
    api = get_api_instance()
    tweets = api.search(q=key_word, lang="en", return_json=False, following=True)
    return fit_into_structure(tweets)
