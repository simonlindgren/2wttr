#!/usr/bin/env python3

import requests
import os
import json
import time

from config_fas import *

endpoint = "https://api.twitter.com/2/tweets/search/all"

params = {
    'query': query,
    'expansions': 'author_id,referenced_tweets.id,geo.place_id,in_reply_to_user_id,referenced_tweets.id.author_id',
    'tweet.fields': 'created_at,author_id,lang,entities,geo,referenced_tweets,in_reply_to_user_id,public_metrics', 
    'user.fields': 'username',
    
    
    'start_time': start_time,
    'end_time': end_time,
    'max_results': max_results,
    
}


headers = {"Authorization": "Bearer {}".format(bearer_token)}

with open("dataset.jsonl", "w") as datafile:

    # MAKE FIRST REQUEST
    print("Getting tweets")
    response = requests.request("GET", endpoint, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    json_response = response.json()

    # PARSE PAGE
    try:
        
        for tweet_dict in json_response['data']:
            user_dict = json_response['includes']['users'] # read the dict with user data which comes separately from the tweet_dict
            
            # Add some user data to the tweet data dicty
            user_to_get = tweet_dict['author_id']
            
            for u in user_dict:
                if u['id'] == user_to_get:
                    tweet_dict['username'] = u['username']
                    tweet_dict['name'] = u['name']

            datafile.write(str(tweet_dict) + "\n")
    except:
        print("No tweets returned")

    # PAGINATE
    try:
        next_token = json_response['meta']['next_token'] # get next_token
        query_params['pagination_token'] = pagination_token # add pagination key to query dict
    except:
        print("No more pages")
    
    # KEEP GETTING PAGES
    while True:
            time.sleep(1)
            response = requests.request("GET", endpoint, headers=headers, params=params)
            if response.status_code != 200:
                raise Exception(response.status_code, response.text)
            json_response = response.json()
            try:          
                for tweet_dict in json_response['data']:
                    user_dict = json_response['includes']['users']
                    user_to_get = tweet_dict['author_id']
                    for u in user_dict:
                        if u['id'] == user_to_get:
                            tweet_dict['username'] = u['username']
                            tweet_dict['name'] = u['name']
                              
                datafile.write(str(tweet_dict) + "\n")
            
                next_token = json_response['meta']['next_token']
                query_params['pagination_token'] = pagination_token

            except:
                break
    
    print("Done")

print(json_response)
