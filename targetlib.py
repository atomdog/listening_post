#target.py
# ----- import statements ------
import hashlib
#https://www.opensecrets.org/personal-finances
# -----                   ------

class target:
    def __init__(self):
        #target hash
        self.id = None
        #target plaintext name
        self.name = None
        #metadata
        self.meta = {}
        #user id, username, latest twitter collected
        self.twitterflag = False
        self.twitter_user_pointer = None
        self.twitter_username = None
        self.last_collected_twitter = None
        self.earliest_tweet = None
    def fuzz_self_init(self):
        checked = ""
        for key in self.meta:
            checked+=self.meta[key]
        self.id = hashlib.md5(checked.encode()).hexdigest()
    def twitter_init(self, id, username):
        self.twitter_user_pointer = id
        self.twitter_username = username
        self.twitterflag = True
    def check_in(self, handoff):
        if(self.twitterflag == False):
            print("<--- ERROR: Checking in on a target without a configured twitter --->")
            return(False)

        #handoff.
