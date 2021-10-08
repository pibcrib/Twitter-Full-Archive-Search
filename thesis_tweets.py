import tweepy
import os
import csv
import ssl
import time
from requests.exceptions import Timeout, ConnectionError
from requests.packages.urllib3.exceptions import ReadTimeoutError

''' More info on Full-Archive API:
https://developer.twitter.com/en/docs/twitter-api/premium/search-api/quick-start/premium-full-archive'''

# Add your Twitter API credentials
#       Source code currently pulls values from environment variables
#       Following 4 vairables should be defined in environment before running script
#       Function for checking if twitter credentials are set in environment
consumer_key = os.environ.get("CONSUMER_KEY", None)
consumer_secret = os.environ.get("CONSUMER_SECRET", None)
access_key = os.environ.get("ACCESS_KEY", None)
access_secret = os.environ.get("ACCESS_SECRET", None)
#       Function for checking if twitter credentials are set in environment
def check_credentials():
    credential_lst = [consumer_key, consumer_secret, access_key, access_secret]
    has_creds = sum(bool(cred) for cred in credential_lst) == 4

    if has_creds:
        return True

    else:
        print("Error: Twitter Credential(s) Not Included:")
        for cred in credential_lst:
            if not cred:
                print(f"\n{cred.upper()}")

        print("Please set environment variables for the abvoe credentials.")
        return False

# Handling authentication with Twitter
if not check_credentials():
    exit()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

# Create a wrapper for the API provided by Twitter
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Define the search term to make the search
search_words = "#boycotthandm"

# Exclude retweets in our search
new_search = search_words + " -filter:retweets" + " result_type:popular"

'''Search for tweets created within a given time frame.'''
date_since = "201801050000"   #2018-1-5 00:00

# Define until what date we are looking for tweets
date_until = "201801302359" #2018-01-30 23:59

# Total tweets to gather in our search
totalTweets = 5000 #consider doing 100000

# Numbers of tweets to return per page, max is 100. Default is 15.
count = 100

# Filter by language
lang = "en"

'''Filter by latitude,longitude,radius.
# 37.781157 -122.398720 1mi'''
geocode = ""

# Filter by recent, popular or mixed.
result_type = "recent"

'''Include info on entities found in Tweets, including hashtags,
links, and mentions. Set to True or False'''
include_entities = True

# Set the name for CSV file  where the tweets will be saved
filename = "tweets_HM"

# Function for handling pagination in our search
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print('Reached rate limite. Sleeping for >15 minutes')
            time.sleep(15 * 60)

# Function for making the search using Twitter API
def search_tweets(new_search, date_since):

    # performs the search using the defined variables
    # consider uncommenting commented parametrs for more restrictions
    for tweet in limit_handled(tweepy.Cursor(api.search_full_archive,
                               environment_name = "searcher", # CHANGE THIS TO ENV NAME FROM API
                               query = new_search,
                               maxResults=count,
                               tweet_mode='extended',
                               #lang=lang,
                               #geocode=geocode,
                               #result_type=result_type,
                               #include_entities=include_entities,
                               #bucket = "day",
                               fromDate =date_since,
                               toDate=date_until).items(totalTweets)):

        try:
            content = tweet.text

            '''Convert all named and numeric character references
            (e.g. &gt;, &#62;, &#x3e;) in the string s to the
            corresponding Unicode characters'''
            content = (content.replace('&amp;', '&').replace('&lt;', '<')
                       .replace('&gt;', '>').replace('&quot;', '"')
                       .replace('&#39;', "'").replace(';', " ")
                       .replace(r'\u', " ").replace('\u2026', ""))

            # Save other information from the tweet
            user = tweet.author.screen_name
            timeTweet = tweet.created_at
            source = tweet.source
            tweetId = tweet.id
            tweetUrl = "https://twitter.com/statuses/" + str(tweetId)
            favcount = tweet.favorite_count
            recount = tweet.retweet_count
            repc =  tweet.reply_count
            isVerf = tweet.author.verified
            followersc = tweet.author.followers_count
            friendsc = tweet.author.friends_count
            listedc = tweet.author.listed_count
            statusesc = tweet.author.statuses_count
            crat = tweet.author.created_at
            ggeo = tweet.geo
            prot = tweet.author.protected

            # Uncomment to Exclude retweets, too many mentions and too many hashtags
            #if not any((('RT @' in content,
            #           content.count('@') >= 2, content.count('#') >= 3))):


            # Saves the tweet information in a new row of the CSV file
            writer.writerow([content, timeTweet,
                                user, source, tweetId, tweetUrl, favcount, recount, repc, isVerf, followersc, friendsc, listedc, statusesc, crat, ggeo, prot])

        except Exception as e:
            print('Encountered Exception:', e)


def work():

    # Opening a CSV file to save the gathered tweets
    with open(filename+".csv", 'w', encoding="utf-8") as file:
        global writer
        writer = csv.writer(file, lineterminator = '\n')

        # Add a header row to the CSV
        writer.writerow(["Tweet Content", "Date", "User",
                         "Source", "Tweet ID", "Tweet URL", "#Favs", "#RTs", "#reply", "isVerf", "followersc", "friendsc", "listedc", "statusesc", "crat", "ggeo", "prot"])

        # Initializing the Twitter search
        try:
            search_tweets(search_words, date_since)

        # Stop temporarily when hitting Twitter rate Limit
        except tweepy.RateLimitError:
            print("RateLimitError...waiting ~15 minutes to continue")
            time.sleep(1001)
            search_tweets(search_words, date_since)

        # Stop temporarily when getting a timeout or connection error
        except (Timeout, ssl.SSLError, ReadTimeoutError,
                ConnectionError) as exc:
            print("Timeout/connection error...waiting ~15 minutes to continue")
            time.sleep(1001)
            search_tweets(search_words, date_since)

        # Stop temporarily when getting other errors
        except tweepy.TweepError as e:
            if 'Failed to send request:' in e.reason:
                print("Time out error caught.")
                time.sleep(1001)
                search_tweets(search_words, date_since)
            elif'Too Many Requests' in e.reason:
                print("Too many requests, sleeping for 15 min")
                time.sleep(1001)
                search_tweets(search_words, date_since)
            else:
                print(e)
                print("Other error with this user...passing")

    input("Press any key to exit program")


if __name__ == '__main__':
    work()
