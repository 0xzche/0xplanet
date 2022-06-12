import tweepy

auth_strs="""
VStGb3HMjzZhzf4ni8aslS5OM 
KPAB4tbnuhKTEWgnKQHYVnESu3IpXwbCB499ujgE8RsU54zfei 
1513021814502535168-DXy7cjeq7YR1nwZzLYiNzXjYGOZhQL 
MNZNxo1zuF8lRkOLopiTpmtrF1AcbqXF1Lv9v8gwowQRg
""".split()

bearer_token = "AAAAAAAAAAAAAAAAAAAAAKdFcQEAAAAAgZTy1s6rPckJ8zWc6%2BETr%2Fzq%2F88%3DvdZFOlmVn3g1LEpclFOqe4ik7ARArut6E5pA6CpMw1bCwOP5IS"
kiri_username = "kiriko_0101"


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
    ]

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
    for u, query in queries.items():

        print(f"processing query: {query}")
        min_like_count = like_count_thres.get(u, default_min_like_count)

        for tweet in tweepy.Paginator(
            finder.search_recent_tweets, 
            query=query,
            tweet_fields=["text", 'public_metrics', "id"], 
            max_results=10).flatten(limit=50):

            count += 1

            try:
                liking_users = finder.get_liking_users(tweet.id)
            except tweepy.errors.TooManyRequests:
                print("Too many requests! Can't get liking users.\n")
                print(f"total liked tweets: {liked_count}")
                return

            if liking_users.data is None:
                liking_usernames = []
            else:
                liking_usernames = [u.username for u in liking_users.data]

            if kiri_username in liking_usernames:
                print(f"({count}) Kiri already liked this :( ")
                continue

            like_count = tweet.public_metrics["like_count"]
            if like_count < min_like_count:
                print(f" too few likes : {like_count}; NGMI ")
            else:
                print("-------------------------------\n")
                print(f" a lot of likes : {like_count} ")
                print(tweet.text)
                print("-------------------------------\n")
                try:
                    kiri.like(tweet.id)
                    print("Liked!!\n")
                    count += 1
                except tweepy.errors.TooManyRequests:
                    print("Too many requests! Can't like this tweet.\n")
                    print(f"total liked tweets: {liked_count}")
                    return

    print(f"total liked tweets: {liked_count}")

if __name__ == "__main__":

    kiri_likes()