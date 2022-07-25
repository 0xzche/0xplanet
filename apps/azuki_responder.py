import tweepy
import numpy as np
from datetime import datetime, timedelta

auth_strs="""
GOKdKri37f12tLkBeBKNmaPms
GF6QTHGIOCeRAh6MDL5IndUB9hc44bfspvuJYVgxu4xPPK1nyd
1551096070129819649-may2dItjJDnMRlR12agUOWRKb3IWYd
UC56FnVTcxfbrjel0tJO8gTFzv1WGtH6KHaNfzgBmgctg
""".split()

"""
client secret
vlQ7YYsTlhHxzOaax7Y5R40SG8krw_O6orB_z2AlP-8gxzCfYE
"""

bearer_token = "AAAAAAAAAAAAAAAAAAAAAMy9fAEAAAAAHLX1fhBHxjsv2tTSABpon2qOUp4%3DdcsbBizZyGgXXsIYj6ipqxOUfXa6myD3XIjX1jgmxM88z26c2p"
my_name = "AzukiResponder"
my_id = "AzukiResponder"

class Log:

    content = []

    def info(self, a):
        self.content.append(a)
    
    def output(self):
        [print(_) for _ in self.content]

log = Log()


def respond_azuki():
    
    # me the shitposter
    bot = tweepy.Client(
        consumer_key=auth_strs[0],
        consumer_secret=auth_strs[1],
        access_token=auth_strs[2],
        access_token_secret=auth_strs[3],
    )
    #bot.create_tweet(text="gm. say it back")

    # tweet finder
    finder = tweepy.Client(bearer_token=bearer_token)

    test_user = "0xMiikka"
    #query = f"azuki from:{test_user} -is:retweet"
    query = f"azuki -from:{my_id} -is:retweet "

    # a user's tweet must be at least a number to be liked be bot

    lag_minutes = 3
    start_time = datetime.utcnow() - timedelta(minutes=lag_minutes)
    log.info(f"processing query: {query}; start time: {start_time}")
    query_results = list(tweepy.Paginator(
        finder.search_recent_tweets, 
        query=query,
        tweet_fields=["text", 'public_metrics', "id", "author_id"], 
        max_results=10,
        start_time=start_time,
    ).flatten(limit=10))

    log.info(f"total n results: {len(query_results)}")
    replied_count = 0
    for tweet in query_results:

        log.info(f"\n processing new tweet \n content of tweet: \n {tweet.text} \n ")
        text = ''.join(filter(str.isalnum, tweet.text)).lower()
        if text.endswith("azuki"):
            try:
                bot.create_tweet(text='Azuki', in_reply_to_tweet_id=tweet.id)
                log.info("Replied!!\n")
                bot.like(tweet.id)
                log.info("Liked!!\n")
                replied_count += 1
            except Exception as e:
                log.info(f"Falied to reply! Reason: {e}")

        if tweet.text.lower().strip().endswith("!ikz"):
            try:
                bot.create_tweet(text='!IKZ', in_reply_to_tweet_id=tweet.id)
                log.info("Replied!!\n")
                bot.like(tweet.id)
                log.info("Liked!!\n")
                replied_count += 1
            except Exception as e:
                log.info(f"Falied to reply! Reason: {e}")

    log.info(f"total replied tweets tweets: {replied_count}")
    return log

if __name__ == "__main__":

    log = respond_azuki()
    log.output()