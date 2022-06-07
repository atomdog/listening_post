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
to collect the emails, you can now run [smtpCheckEmail.py](smtpCheckEmail.py) 

this will read the entire inbox. to get only new emails, refer to the [gmailfunctions.py](/google-apis/gmailfunctions.py), and swap functions in the smtpCheckEmail to the 'readMail()' function. 

Regardless of which function you use, the inbox will be saved to [memory/inbox.txt](/memory) with a datestring appended to the end, in the format 'm|d|y'

The email inbox uses custom delimiters. Many emails use non-standard formatting and they do not all use the same non-standard formatting. Detecting and properly parsing each one proved too much in the time frame given to write this library, so the output had to reflect and handle that. 

The delimiter; 

`==INTERRUPT==`

separates JSON formatted text:

> {'Subject': "e", 'From': "plurbus@wincampaign.com" 'Message': "unum"}

ie:


`
==INTERRUPT==
{
  'Subject': 'Happy Mothers Day from Eddie Joe Williams', 
  'From': 'Vote GoEddieJoe <info@goeddiejoe.com>', 
  'Message': [<p>My wife DeLona of 49 years and ALL mothers deserve to be honored and loved.
    View this email in your browser (https://mailchi.mp/66399deba7dc/happy-mothers-day-from-eddie-joe-williams?e=fefe785530)
    ** Happy Mothers Day!
    ------------------------------------------------------------
    My wife DeLona of 49 years, and my four daughters, are great Christian women and great moms. We take this day to honor and thank those women who put    their heart and souls into their family, children, and grandchildren. We cannot thank the mothers out there enough who stand with us through struggles    and triumphs to make our families the best they can be. We will forever be grateful, such as I am, to all the moms out there who make it all possible.    God has blessed us in many ways. He has definitely blessed me with a better half that everyday I am proud to call my wife and my daughters mom.
    P.S. The eleven grandkids love her to!
    -Eddie Joe Williams
    ============================================================
    ** GoEddieJoe4SOS (http://www.twitter.com/GoEddieJoe4SOS)
    ** GoEddieJoe (http://www.facebook.com/GoEddieJoe)
    ** GoEddieJoe4SOS (http://instagram.com/GoEddieJoe4SOS)
    Copyright Â© 2022 Paid for by Elect Eddie Joe Williams Arkansas Secretary of State, All rights reserved.
    You are receiving this email because you had an interest in Arkansas, politics, voting, or specific hobbies.
    Our mailing address is:
    Paid for by Elect Eddie Joe Williams Arkansas Secretary of State
    401 Cobblestone Dr
    Cabot, AR 72023-9458
    USA
    Want to change how you receive these emails?
    You can ** update your preferences 
    or ** unsubscribe from this list 
}
==INTERRUPT==
`


## twitter
you can likely mostly ignore this part, although it is by far the most built out and well-formatted. 

[birdnest.py](birdnest.py) contains a library for a custom h5 database containing users and tweets. 

the code is very straightforward and readable, however,

tweets are formatted in columns like so:

> tweetID|time|text|authorUsername|authorID|likes|retweets

users are formatted in columns like so: 

> ID|Username|time_observed|username|bio

I don't remember why I added a second column for usernames. I don't believed it is used, but it may have been a check as some users change their username

There is also an edge database.

> IDa|IDb|type

This can store interactions between users and tweets or users and users. The type is a string which can be 'follows', 'liked', 'retweeted'.

The snapshot() function creates a snapshot of the database at the current time, cloning it and allowing reference to the state of things at that time. 

The create_empty_logs() function overwrites the main logs with new ones, and is called when initializing or deleting the non-snapshotted database.

Each database has a read and append function, both straightforward. Encoding is important. Do not throw non-utf8 characters into the database, check your string encoding when parsing anything. 

the [tw_ctrl.py](tw_ctrl.py) is a wrapper for the API via [twitterInterface.py](twitterInterface.py). It handles OAuth and related tasks, and is straightforward to use. You can use twitterInterface.py alone by calling ret_auth(), and passing the returned authenticated api object to the other twitterInterface functions. 

Twitter was primarily handled by the mostly depreciated acquisition authority, discussed below. 

## [acquisition_authority.py](acquisition_authority.py)

Back when Twitter was a main focus, the acquisition_authority formatted the names of the candidates and metadata about them and tied these to users. The target parameters in [conf.json](conf.json) created a dictionary to store information on them to access in the context of tweets and other things. 

This file is large and relatively aged so it is not extremely relevant to the documentation.

# analysis, etc

## [analysis_authority.py](analysis_authority.py)

The analysis authority contains the beginning of the analysis, including the language loop which is a natural language engine from [oslo](https://github.com/atomdog/oslo). It also contains a multiprocessing sentiment analysis function, ideally run with as many cores as you can offer it, otherwise it will take a very long time. 

This code:

`q = language_loop()`

`q.read_complete_youtube()`

`q.spin()`

`q.compare()`

creates a language loop, reads in the youtube videos, makes the connections between them, and compares speakers. 

The language loop itself, and associated files such as the semantic web, modwern, and the Language folder in general are large and complex files involving co-routines, suspended execution, and various NLP concepts which do not have a place being documented here. You are best off creating your own version of these files or reading through them yourself.

It is advised you carry out whatever analysis you plan on doing using the dataflows provided, and your own implementation of a semantic network, or another readily available. 

If you are absolutely set on using them, the associated documentation can be found on the [oslo](https://github.com/atomdog/oslo) project page. 

# useful part

[debug.py](debug.py) will export your data to spreadsheets for later use by others. 

