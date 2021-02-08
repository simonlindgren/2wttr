#!/usr/bin/env python3

import requests
import os
import json
import time

from config_fas import *

endpoint = "https://api.twitter.com/2/tweets/search/all"

params = {
    'query': query,
    'tweet.fields': tweet_fields,
    'user.fields': user_fields,
    'start_time': start_time,
    'end_time': end_time,
    'max_results': max_results
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
        for tweet in json_response['data']:
            datafile.write(str(tweet) + "\n")
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
              
                for tweet in json_response['data']:
                    datafile.write(str(tweet) + "\n")
                next_token = json_response['meta']['next_token']
                query_params['pagination_token'] = pagination_token

            except:
                break
    
    print("Done")