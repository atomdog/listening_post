#target.py
# ----- import statements ------
import hashlib

# -----                   ------

class target:
    def __init__(self):
        self.id = None
        self.name = None
        self.last_collected_twitter = None
        self.user_pointer = None
        self.meta = {}
    def fuzz_self_init(self):
        checked = ""
        for key in self.meta:
            checked+=self.meta[key]
        self.id = hashlib.md5(checked.encode()).hexdigest()
    def twitter_init(self, id):
        self.user_pointer = id


    def check_in(self):
        pass
