import tweepy
import numpy as np

auth_strs="""
GOKdKri37f12tLkBeBKNmaPms
GF6QTHGIOCeRAh6MDL5IndUB9hc44bfspvuJYVgxu4xPPK1nyd
1551096070129819649-3yGvFt9dZAzYfggDPUetyKiAfRiph1
oJNtrV30R9xpSaudcim0hFpAjQTRMSuVlSuNPkdWwmV9a
""".split()

bearer_token = "AAAAAAAAAAAAAAAAAAAAAMy9fAEAAAAAHLX1fhBHxjsv2tTSABpon2qOUp4%3DdcsbBizZyGgXXsIYj6ipqxOUfXa6myD3XIjX1jgmxM88z26c2p"
my_name = "AzukiResponder"
my_id = "AzukiResponder"

class Log:

    content = []

    def info(self, a):
        self.content.append(a)
    
    def output(self):
        print(self.content)

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
    query = f"from:{test_user} -is:retweet "
    query = f"azuki -is:retweet "

    # a user's tweet must be at least a number to be liked be bot
    log.info(f"processing query: {query}")

    for tweet in tweepy.Paginator(
        finder.search_recent_tweets, 
        query=query,
        tweet_fields=["text", 'public_metrics', "id"], 
        max_results=10).flatten(limit=50):
        log.info(tweet.text)
        bot.like(tweet.id)
        log.info("Liked!!\n")
        liked_count += 1

    log.info(f"total liked tweets: {liked_count}")
    return log

if __name__ == "__main__":

    log = respond_azuki()
    log.output()