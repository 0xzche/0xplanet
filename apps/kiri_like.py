import tweepy

auth_strs="""
VStGb3HMjzZhzf4ni8aslS5OM 
KPAB4tbnuhKTEWgnKQHYVnESu3IpXwbCB499ujgE8RsU54zfei 
1513021814502535168-DXy7cjeq7YR1nwZzLYiNzXjYGOZhQL 
MNZNxo1zuF8lRkOLopiTpmtrF1AcbqXF1Lv9v8gwowQRg
""".split()

bearer_token = "AAAAAAAAAAAAAAAAAAAAAKdFcQEAAAAAgZTy1s6rPckJ8zWc6%2BETr%2Fzq%2F88%3DvdZFOlmVn3g1LEpclFOqe4ik7ARArut6E5pA6CpMw1bCwOP5IS"


if __name__ == "__main__":

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

    queries = []
    tgt_users = [
        "ZAGABOND", 
        "AzukiOfficial", 
        "DemnaAzuki", 
        "cygaar_dev",
        "0xMiikka",
        "Skywalker2620",
    ]

    for u in tgt_users:
        queries.append(f"from:{u} -is:retweet ")

    count = 0
    for query in queries:
        print(f"processing query: {query}")
        for tweet in tweepy.Paginator(
            finder.search_recent_tweets, 
            query=query,
            tweet_fields=["text", 'public_metrics'], 
            max_results=10).flatten(limit=100):

            like_count = tweet.public_metrics["like_count"]
            if like_count < 10:
                print(f" too few likes : {like_count}; NGMI ")
            else:
                print("-------------------------------\n")
                print(f" a lot of likes : {like_count} ")
                print(tweet.text)
                print("-------------------------------\n")
                kiri.like(tweet.id)
                count += 1
    print(f"total liked tweets: {count}")