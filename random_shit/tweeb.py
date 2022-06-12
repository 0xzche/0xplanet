import tweepy

"""
client = tweepy.client(bearer_token='aaaaaaaaaaaaaaaaaaaaakdfcqeaaaaanerqihfcfuvsx8iaqeae84fkdeq%3dftqsv4ajgqj6gsopybbgmc3pfacuarpbpzdeibyw1ltyvwueau')

# Replace with your own search query
query = 'from:azukiofficial -is:retweet'

tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'], max_results=100)

for tweet in tweets.data:
    print("--------------")
    print(tweet.text)
    if len(tweet.context_annotations) > 0:
        print(tweet.context_annotations)
"""

auth_strs="""
VStGb3HMjzZhzf4ni8aslS5OM 
KPAB4tbnuhKTEWgnKQHYVnESu3IpXwbCB499ujgE8RsU54zfei 
1513021814502535168-DXy7cjeq7YR1nwZzLYiNzXjYGOZhQL 
MNZNxo1zuF8lRkOLopiTpmtrF1AcbqXF1Lv9v8gwowQRg
""".split()

client0 = tweepy.Client(
    consumer_key=auth_strs[0],
    consumer_secret=auth_strs[1],
    access_token=auth_strs[2],
    access_token_secret=auth_strs[3],
)

#client0.create_tweet(text="gm. say it back")

client1 = tweepy.Client(
    bearer_token="AAAAAAAAAAAAAAAAAAAAAKdFcQEAAAAAgZTy1s6rPckJ8zWc6%2BETr%2Fzq%2F88%3DvdZFOlmVn3g1LEpclFOqe4ik7ARArut6E5pA6CpMw1bCwOP5IS"
)
query = "azuki -is:retweet"
for tweet in tweepy.Paginator(
    client1.search_recent_tweets, 
    query=query,
    tweet_fields=['context_annotations', 'created_at'], 
    max_results=10).flatten(limit=20):
    print("---------------------------")
    print(tweet.text)