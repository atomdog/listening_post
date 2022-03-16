#post_control.py
import smtpCheckEmail
import twitterInterface
import tweepy
import credLib
class ctroller:
    def __init__(self):
        a,b,c,d= credLib.returnbykey("twitter", "api"), credLib.returnbykey("twitter", "api_secret"), credLib.returnbykey("twitter", "access_token"), credLib.returnbykey("twitter", "access_token_secret")
        self.auth = tweepy.OAuthHandler(a, b)
        self.auth.set_access_token(c, d)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    def log_emails(self):
        print(smtpCheckEmail.checkemail())
    def log_user_followers(self, usn):
        print(twitterInterface.followersbyuser(usn, self.api))
    def log_user_tweets(self, usn):
        print(twitterInterface.tweetsbyuser(usn, self.api))
q = ctroller()
#q.log_emails()
#get tweets in a swoop, store in h5, get additional info on each tweet from h5 as well


q.log_user_tweets("@reginaldbolding")
