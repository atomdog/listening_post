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
        return(twitterInterface.followersbyuser(usn, self.api))
    def log_user_tweets(self, usn):
        return(twitterInterface.tweetsbyuser(usn, self.api))
    def convert_username(self, usn):
        try:
            q = twitterInterface.usertoid(usn, self.api)
            return(q)
        except Exception as e:
            print("EXCEPTION IN USERNAME CONVERSION FOR "+ str(usn))
            print("    ")
            print("    ")
            print(e)
            print("    ")
            print("Returning...")


    def twitter_routine(self, usn):
        pass



#q.log_emails()
#get tweets in a swoop, store in h5, get additional info on each tweet from h5 as well
