# intro

THE REPOSITORY IS NOT CLEAN OF CREDENTIALS. BEFORE YOU MAKE THIS PUBLIC CHECK DILIGENTLY FOR LEFTOVER PLAINTEXT PASSWORDS.  


listening_post is a framework to monitor political speech online. Current inputs include Twitter, Youtube, and GMail. These are fed into a common analysis engine. 

you should follow the documentation from inputs to analysis, in order, to get things started. do not configure things out of order, it will not work.

# inputs

## youtube
to start: this project does NOT use the official youtube api. that proved too much of a hassle. as you will see when we get to the gmail api, if you can avoid interacting with any google api's, you should.

#### getting started
the api should work sans any key or whatnot. 
#### to add a youtube video to the list of targeted youtube videos:
navigate to [/targeting/youtubevideos.txt](/targeting/youtubevideos.txt)

the file uses the following format:

> videoid,start_time,end_time,speaker

like this:

> DqXJaJbbk1M,233,871,biden

the videoid can be found conveniently in the youtube url;

> https://www.youtube.com/watch?v=SYxZfksAyco

> v=SYxZfksAyco


> videoid = SYxZfksAyco

start and end time are in seconds. this can be found from the sharing url for both points, or you can do the math. 

to target the entire video, you can simply use:

> pzcCNJK2LjI,start,finish,trump

#### collecting youtube videos

run 'python3 transcript.py' from the main directory. 
the script will asynchronously collect the videos' subtitles and deposit them to [memory/youtube/](memory/youtube/)

the files are named in the following format: 

> speaker_videoid.txt

like this:

> benson_eWTs-EwMjdA.txt

the transcript is stored in a quasi-csv format. 

each line follows the format:

> speaker: transcript_text, start_time, duration, date_published

such as:

> hice: that the the u.s army says it's going to, 10.559, 4.881, 2022-02-02


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

#### collecting emails
to collect the emails, you can now run [smtpCheckEmail.py](smtpCheckEmail.py) this will read the entire inbox. to get only new emails, refer to the [gmailfunctions.py](/google-apis/gmailfunctions.py), and swap functions in the smtpCheckEmail to the 'readMail()' function. 

Regardless of which function you use, the inbox will be saved to [memory/inbox.txt](/memory) with a datestring appended to the end, in the format 'm|d|y'
## twitter
you can likely mostly ignore this part.
