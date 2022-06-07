
import tweepy
import csv
import credLib
#============not relevant functions===========

def tweet(text, api):
    api.update_status(text)
def replybyid(id, user, text, tuser):
    api.update_status('@'+str(user)+' ' + str(text),tweetId)
#=============================================

#===========auth functions===================
def ret_auth():
    a,b,c,d= credLib.returnbykey("twitter", "api"), credLib.returnbykey("twitter", "api_secret"), credLib.returnbykey("twitter", "access_token"), credLib.returnbykey("twitter", "access_token_secret")
    auth = tweepy.OAuthHandler(a, b)
    auth.set_access_token(c, d)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return(api)
#=============================================
#===========in progress functions===========
def tweets_since_x_by_user(screen_name, api, since):
    alltweets = []
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
    while len(new_tweets) > 0:
        print(f"getting tweets since {since}")
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        print(oldest)
        print(f"...{len(alltweets)} tweets downloaded so far")
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
    return(outtweets)
#==========================================

#===========polished functions=============

def tweetsbyuser(screen_name, api):
    alltweets = []
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
    print(oldest)
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        print(f"...{len(alltweets)} tweets downloaded so far")
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text,tweet.retweet_count,tweet.favorite_count,tweet.user.screen_name] for tweet in alltweets]
    return(outtweets)

def followingbyuser(user, api):
    screen_name = user
    c = tweepy.Cursor(api.friends, screen_name)
    following_list = []
    for following in c.items():
        following_list.append([following.id_str,following.screen_name,following.description])
    return(following_list)

def followersbyuser(user, api):
    screen_name = user
    c = tweepy.Cursor(api.followers, screen_name)
    follower_list = []
    for follower in c.items():
        follower_list.append([follower.id_str,follower.screen_name,follower.description])
    return(follower_list)

def usertoid(username, api):
    userid = api.get_user(username)
    ID = userid.id_str
    return(ID)

def user_bio(username, api):
    user = api.get_user(username)
    return(user.description)

def repliestotweet(id, api):
    replies=[]
    returnreplies = []
    for tweet in tweepy.Cursor(api.search,q='to:'+name, result_type='recent', timeout=999999).items(1000):
        if hasattr(tweet, 'in_reply_to_status_id_str'):
            if (tweet.in_reply_to_status_id_str==tweet_id):
                replies.append(tweet)
        for tweet in replies:
            returnreplies.append([tweet.created_at,tweet.user.screen_name, tweet.text.replace('\n', ' ')])
    return(returnreplies)

#==========================================
