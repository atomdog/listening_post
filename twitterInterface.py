
import tweepy
import csv

def tweet(text, api):
    api.update_status(text)
    pass

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
    with open(f'raw_twit/tweets|{screen_name}|.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)
    pass

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

def followingbyuser(user, api):
    screen_name = user
    c = tweepy.Cursor(api.friends, screen_name)
    with open('raw_twit/following|' + str(user) + '|.csv', 'w') as f:
        csv_writer = csv.DictWriter(f, fieldnames=('user',))
        csv_writer.writeheader()
        for following in c.items():
            row = {'user': following.screen_name}
            csv_writer.writerow(row)
def replybyid(id, user, text, tuser):
    api.update_status('@'+str(user)+' ' + str(text),tweetId)
