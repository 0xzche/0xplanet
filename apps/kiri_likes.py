import tweepy
import numpy as np

auth_strs="""
VStGb3HMjzZhzf4ni8aslS5OM 
KPAB4tbnuhKTEWgnKQHYVnESu3IpXwbCB499ujgE8RsU54zfei 
1513021814502535168-DXy7cjeq7YR1nwZzLYiNzXjYGOZhQL 
MNZNxo1zuF8lRkOLopiTpmtrF1AcbqXF1Lv9v8gwowQRg
""".split()

bearer_token = "AAAAAAAAAAAAAAAAAAAAAKdFcQEAAAAAgZTy1s6rPckJ8zWc6%2BETr%2Fzq%2F88%3DvdZFOlmVn3g1LEpclFOqe4ik7ARArut6E5pA6CpMw1bCwOP5IS"
kiri_username = "kiriko_0101"
kiri_id = "1513021814502535168"

class Log:

    content = []

    def info(self, a):
        self.content.append(a)
    
    def output(self):
        print(self.content)

log = Log()


def kiri_likes():
    
    # kiri the shitposter
    kiri = tweepy.Client(
        consumer_key=auth_strs[0],
        consumer_secret=auth_strs[1],
        access_token=auth_strs[2],
        access_token_secret=auth_strs[3],
    )
    #kiri.create_tweet(text="gm. say it back")

    # tweet finder
    finder = tweepy.Client(bearer_token=bearer_token)

    tgt_users = [
        "AzukiSales",
        "0xMiikka",
        "ZAGABOND", 
        "AzukiOfficial", 
        "DemnaAzuki", 
        "KLiebsMfer",
        "latteshelby",
    ]
    np.random.shuffle(tgt_users)

    # query for each user
    queries = {}
    for u in tgt_users:
        queries[u] = f"from:{u} -is:retweet "

    # a user's tweet must be at least a number to be liked be kiri
    like_count_thres = {}
    like_count_thres["AzukiSales"] = 0
    default_min_like_count = 5

    count = 0
    liked_count = 0
    max_like_count = 5

    tweets_liked_by_kiri = finder.get_liked_tweets(kiri_id)
    tweets_liked_by_kiri = [_.id for _ in tweets_liked_by_kiri.data]
    
    for u, query in queries.items():

        log.info(f"processing query: {query}")
        min_like_count = like_count_thres.get(u, default_min_like_count)

        for tweet in tweepy.Paginator(
            finder.search_recent_tweets, 
            query=query,
            tweet_fields=["text", 'public_metrics', "id"], 
            max_results=10).flatten(limit=50):

            if tweet.id in tweets_liked_by_kiri:
                log.info(f"({count}) Kiri already liked this :( ")
                continue

            count += 1
            like_count = tweet.public_metrics["like_count"]
            if like_count < min_like_count:
                log.info(f" too few likes : {like_count}; NGMI ")
            else:
                # detect liked by kiri or not
                log.info("-------------------------------\n")
                log.info(f" a lot of likes and not liked by kiri : {like_count} ")
                log.info(tweet.text)
                log.info("-------------------------------\n")
                try:
                    kiri.like(tweet.id)
                    log.info("Liked!!\n")
                    liked_count += 1
                    if liked_count > max_like_count:
                        log.info(f"total liked tweets: {liked_count} > {max_like_count}; taking a break")
                        return log
                except tweepy.errors.TooManyRequests:
                    log.info("Too many requests! Can't like this tweet.\n")
                    log.info(f"total liked tweets: {liked_count}")
                    return log

    log.info(f"total liked tweets: {liked_count}")
    return log

if __name__ == "__main__":

    log = kiri_likes()
    log.output()
