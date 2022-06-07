# intro
listening_post is a framework to monitor political speech online. Current inputs include Twitter, Youtube, and GMail. These are fed into a common analysis engine. 

you should follow the documentation from inputs to analysis, in order, to get things started. do not configure things out of order, it will not work.

# inputs

## youtube
to start: this project does NOT use the official youtube api. that proved too much of a hassle. as you will see when we get to the gmail api, if you can avoid interacting with any google api's, you should.
## gmail
as of recently, gmail squashed third party access to its smtp servers. if you decide to rewrite this, you will see many resources that seem far simpler. those used to work, but do not any longer. 

#### getting started
[quickstart.py](/google-apis/quickstart.py) handles all of the permissions and token business for you.

from the main listening_directory, (do NOT navigate to the gmail-apis subdirectory to execute this), run 
'''
python3 quickstart.py. 
'''
this will open a browser window and begin an authentification flow. 
login to the email 
>'usatodaytwitter7@gmail.com' 
with the password 
>'HUBXC410B1' 
give listening_post all permissions. it will say that listening_post is not a verified app, ignore this.

now you're all set. you may need to refer back to this to re-authenticate when your token expires.
## twitter
you can likely mostly ignore this part.
