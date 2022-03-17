
import tweepy
import csv

#============not relevant functions===========
def tweet(text, api):
    api.update_status(text)
def replybyid(id, user, text, tuser):
    api.update_status('@'+str(user)+' ' + str(text),tweetId)
#=============================================

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



def tweetsbyuser(screen_name, api):
    alltweets = []
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        print(f"...{len(alltweets)} tweets downloaded so far")
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
    return(outtweets)


def repliesbyid(id, api):
    replies=[]
    for tweet in tweepy.Cursor(api.search,q='to:'+name, result_type='recent', timeout=999999).items(1000):
        if hasattr(tweet, 'in_reply_to_status_id_str'):
            if (tweet.in_reply_to_status_id_str==tweet_id):
                replies.append(tweet)
    with open('raw_twit/replies|' + str(tweet_id) + '|.csv', 'a') as f:
        csv_writer = csv.DictWriter(f, fieldnames=('user', 'text'))
        csv_writer.writeheader()
        for tweet in replies:
            row = {'user': tweet.user.screen_name, 'text': tweet.text.replace('\n', ' ')}
            csv_writer.writerow(row)

def followersbyuser(user, api):
    screen_name = user
    c = tweepy.Cursor(api.followers, screen_name)
    with open('raw_twit/followers|' + str(user) + '|.csv', 'w') as f:
        csv_writer = csv.DictWriter(f, fieldnames=('user',))
        csv_writer.writeheader()
        for follower in c.items():
            row = {'user': follower.screen_name}
            csv_writer.writerow(row)

#===========polished functions=============

def tweetsbyuser(screen_name, api):
    alltweets = []
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        print(f"...{len(alltweets)} tweets downloaded so far")
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
    return(outtweets)

def followingbyuser(user, api):
    screen_name = user
    c = tweepy.Cursor(api.friends, screen_name)
    following_list = []
    for following in c.items():
        following_list.append(following.screen_name)
    return(following_list)

def followersbyuser(user, api):
    screen_name = user
    c = tweepy.Cursor(api.followers, screen_name)
    follower_list = []
    for follower in c.items():
        follower_list.append(follower.screen_name)
    return(follower_list)

def usertoid(username, api):
    userid = api.get_user(username)
    ID = userid.id_str
    return(ID)
#==========================================
