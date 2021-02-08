#!/usr/bin/env python3

import json

with open("parsed_dataset.jsonl", "w") as outfile:

    with open("dataset.jsonl", "r") as rawdata:

        for tweet in rawdata:

            clean_tweet = {}

            tweet = tweet.replace("'", '"') # fix json format 
            tweet = json.loads(tweet)

            text = tweet['text']
            text = text.replace('"', "'") # user only single quotes within tweet text
            text = text.replace("\n", " ")

            mentioned = []
            for i in tweet['entities']['mentions']:
                mentioned.append("@" + i['username'])

            replied_to = ""
            retweeted = ""
            quoted = ""
            for i in tweet['referenced_tweets']:
                if i['type'] == "replied_to":
                    replied_to = i['id']
                if i['type'] == "retweeted":
                    retweeted = i['id']
                if i['type'] == "quoted":
                    quoted = i['id']


            # Basic
            clean_tweet['tweet_id'] = tweet['id']
            clean_tweet['created_at'] = tweet['created_at']
            clean_tweet['lang'] = tweet['lang']

            # User
            clean_tweet['author_id'] = tweet['author_id']
            clean_tweet['username'] = "@" + tweet['username']
            clean_tweet['name'] = tweet['name']

            # Tweet
            clean_tweet['text'] = text

            # Connections
            clean_tweet['in_reply_to_user_id'] = tweet['in_reply_to_user_id']

            clean_tweet['mentioned_tweet_id'] = mentioned
            clean_tweet['replied_to_tweet_id'] = replied_to
            clean_tweet['retweeted_tweet_id'] = retweeted
            clean_tweet['quoted_tweet_id'] = quoted



            # Metrics
            clean_tweet['retweet_count'] = tweet['public_metrics']['retweet_count']
            clean_tweet['reply_count'] = tweet['public_metrics']['reply_count']
            clean_tweet['like_count'] = tweet['public_metrics']['like_count']
            clean_tweet['quote_count'] = tweet['public_metrics']['quote_count']
            
            outfile.write(str(clean_tweet) + "\n")