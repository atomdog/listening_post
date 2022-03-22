#tw_ctrl.py
import smtpCheckEmail
import twitterInterface
import tweepy
import birdnest
import credLib
class ctrl:
    def __init__(self):
        a,b,c,d= credLib.returnbykey("twitter", "api"), credLib.returnbykey("twitter", "api_secret"), credLib.returnbykey("twitter", "access_token"), credLib.returnbykey("twitter", "access_token_secret")
        self.auth = tweepy.OAuthHandler(a, b)
        self.auth.set_access_token(c, d)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    def log_emails(self):
        return(smtpCheckEmail.checkemail())
    def log_user_followers(self, usn):
        followers = twitterInterface.followersbyuser(usn, self.api)
        return(followers)
    def log_user_following(self, usn):
        followers = twitterInterface.followingbyuser(usn, self.api)
        return(followers)
    def log_user_tweets(self, usn):
        tweets = twitterInterface.tweetsbyuser(usn, self.api)
        return(tweets)
    def convert_username(self, usn):
        try:
            q = twitterInterface.usertoid(usn, self.api)
            return(q)
        except Exception as e:
            print("    ")
            print("    ")
            print("<--- ERROR: Exception in Username to ID conversion --->")
            print(usn)
            print("    ")
            print("    ")
            print(e)
            print("    ")
            print("    ")
            print("<----------------------------------------------------->")
    def twitter_routine(self, usn):
        pass
    def get_bio(self, usn):
        try:
            q = twitterInterface.user_bio(usn, self.api)
            return(q)
        except Exception as e:
            print("    ")
            print("    ")
            print("<--- ERROR: Exception Retrieving User Bio --->")
            print(usn)
            print("    ")
            print("    ")
            print(e)
            print("    ")
            print("    ")
            print("<-------------------------------------------->")



#q.log_emails()
#get tweets in a swoop, store in h5, get additional info on each tweet from h5 as well
