#authority.py

# ----- import statements ------
import pickle
import targetlib
import os
import csv
import json
import tw_ctrl
import grandtimeline
import birdnest
from datetime import datetime
import smtpCheckEmail
# -----                   ------

def freeze_authority(author):
    fh = open("memory/authorityonice.obj", 'wb')
    pickle.dump(author, fh)

def torch_authority():
    author = authority()
    fh = open("memory/authorityonice.obj", 'wb')
    pickle.dump(author, fh)

def thaw_authority():
    fh = open("memory/authorityonice.obj", 'rb')
    author = pickle.load(fh)
    return(author)


def freeze_emails(inbo):
    fh = open("memory/inbox.obj", 'wb')
    pickle.dump(inbo, fh)

def torch_email():
    inbo = []
    fh = open("memory/inbox.obj", 'wb')
    pickle.dump(inbo, fh)

def thaw_email():
    fh = open("memory/inbox.obj", 'rb')
    inbo = pickle.load(fh)
    return(inbo)


def pull_emails():
    appInbox = thaw_email()
    print("<--- Checking emails --->")
    inbox = smtpCheckEmail.checkemail()
    print(inbox)
    inbox = appInbox + inbox
    freeze_emails(inbox)




class authority:
    def __init__(self):
        self.targets = []
        #set up configuration
        with open('conf.json') as json_file:
            data = json.load(json_file)
        self.target_parameters = data['target_parameters']
        self.controller = tw_ctrl.ctrl()

    def reload_controller(self):
        self.controller = tw_ctrl.ctrl()
    #fuzzy loading csv so we can be lazy later on
    def load_targets(self):
        path = "targeting/"
        q = os.listdir(path)
        q = sorted(q)
        for file in q:
            if file.endswith(".csv") and file == "pitch_sample.csv":
                with open(path+file, mode='r') as csv_file:
                    print("===== Processing " + str(file) + " ===========")
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    col_names = []
                    self.reload_controller()
                    for row in csv_reader:
                        if line_count == 0:
                            col_names = row
                            col_names = list((map(lambda x: x.lower(), col_names)))
                            line_count += 1
                        else:
                            new_target = targetlib.target()
                            new_target.meta = dict(zip(self.target_parameters, " "))
                            line_count += 1
                            for x in range(0, len(row)):
                                new_target.meta[col_names[x]] = row[x]
                            new_target.fuzz_self_init()
                            print("Creating Target For: " + str(new_target.meta['name']))
                            if('@' in new_target.meta['twitter']):
                                tw_id = self.controller.convert_username(new_target.meta['twitter'])
                                new_target.twitter_init(tw_id, new_target.meta['twitter'])
                                if(self.controller.get_bio(new_target.meta['twitter']) != None):
                                    new_target.own_twitter_bio = self.controller.get_bio(new_target.meta['twitter'])
                            self.targets.append(new_target)
                    print("====== Processed " + str(file) + " ===========")
        #Save self
        freeze_authority(self)

    def create_target_users(self):
        for x in range(0, len(self.targets)):
            c = self.targets[x]
            if(c.check_in()):
                now = datetime.now()
                dt_string = now.strftime("%d:%m:%Y:s%H:%M:%S")
                birdnest.u_append_log(c.twitter_user_pointer, c.twitter_username, str(dt_string), c.own_twitter_bio.encode('utf-8'))
                #print(c.id, c.twitter_username, dt_string, c.own_twitter_bio.encode('utf-8'))
    def first_pass_followers(self):
        self.reload_controller()
        for x in range(0, len(self.targets)):
            c = self.targets[x]
            print("<---------- Followers for: ------------>")
            print(c.twitter_username)
            if(c.check_in()):
                followers = self.controller.log_user_followers(c.twitter_username)
                for y in range(0, len(followers)):
                    now = datetime.now()
                    dt_string = now.strftime("%d:%m:%Y:s%H:%M:%S")
                    birdnest.u_append_log(followers[y][0],followers[y][1], str(dt_string), followers[y][2].encode('utf-8'))
                    birdnest.e_append_log(followers[y][0], c.twitter_user_pointer, 'follows')
            print("<------------- COMPLETE --------------->")

    def first_pass_following(self):
        self.reload_controller()
        for x in range(0, len(self.targets)):
            c = self.targets[x]
            print("<---------- Followers for: ------------>")
            print(c.twitter_username)
            print("-----------")
            if(c.check_in()):
                followers = self.controller.log_user_following(c.twitter_username)
                for y in range(0, len(followers)):
                    now = datetime.now()
                    dt_string = now.strftime("%d:%m:%Y:s%H:%M:%S")
                    birdnest.u_append_log(followers[y][0],followers[y][1], str(dt_string), followers[y][2].encode('utf-8'))
                    birdnest.e_append_log(followers[y][0], c.twitter_user_pointer, 'follows')

    def first_pass_likes(self):
        pass

    #t_append_log(id, time, text, author, liked, retweets)
    #[tweet.id_str, tweet.created_at, tweet.text,tweet.retweet_count,tweet.favorite_count,tweet.user.screen_name]
    def first_pass_tweets(self):
        self.reload_controller()
        for x in range(0, len(self.targets)):
            c = self.targets[x]
            print("<---------- Tweets for: ------------>")
            print(c.twitter_username)
            if(c.check_in()):
                tweets = self.controller.log_user_tweets(c.twitter_username)
                for y in range(0, len(tweets)):
                    #now = datetime.now()
                    #dt_string = now.strftime("%d:%m:%Y:s%H:%M:%S")

                    birdnest.t_append_log(tweets[y][0],tweets[y][1],tweets[y][2],c.twitter_username, tweets[y][4], tweets[y][3])
                    birdnest.e_append_log(c.twitter_user_pointer, tweets[y][0], 'tweeted')

    def author_max_tweets(self, username):
        max_retweets = 0
        topr = []
        mrindex = 0
        topl = []
        max_likes = 0
        mlindex = 0
        tweets = self.controller.log_user_tweets(username)
        for x in range(0, len(tweets)):
            if(int(tweets[x][3])>max_retweets):
                max_retweets = int(tweets[x][3])
                mrindex = x
                topr.append(mrindex)
            if(int(tweets[x][4])>max_likes):
                max_likes = int(tweets[x][4])
                mlindex = x
                topl.append(mlindex)

        print("-------")
        print("Likes")
        for x in range(len(topl)-5, len(topl)):
            print(tweets[x])
        print("-------")
        print("Retweets")
        for x in range(len(topr)-5, len(topr)):
            print(tweets[x])

#pull_emails()

#q = torch_authority()
#q = thaw_authority()
#q.load_targets()
#q.create_target_users()
#q.first_pass_tweets()
#q.author_max_tweets("@CongressmanHice")
#q.first_pass_following()
#q.first_pass_followers()
