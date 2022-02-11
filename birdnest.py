#twitter_lake.py

import numpy as np
import tables
import matplotlib.pyplot as plt

class twitterULog(tables.IsDescription):
    ID      = tables.StringCol(16)   # 16-character String
    time  = tables.StringCol(128)      # Signed 64-bit integer
    text  = tables.StringCol(500)   #500-character string
    follow_pointers = tables.StringCol(5000) #5000-character string
    followed_pointers = tables.StringCol(5000) #5000-character string # 16-character String
    liked_pointers = tables.StringCol(5000)
    tweeted_pointers = tables.StringCol(5000)
#creates empty twitter log
#pass in twitterULog class
def u_create_log(tL):
    h5file = tables.open_file("twitter/twitterUser_log.h5", mode="w", title="twit")
    group = h5file.create_group("/", 'Null', 'Twitter')
    table = h5file.create_table(group, 'Null', tL, "Twitter_Data")
    table.flush()
    h5file.close()

#pass in row title,
def u_dump_by_row(rowName):
    h5file = tables.open_file("twitter/twitterUser_log.h5", mode="a", title="twit")
    table = h5file.root.Null.Null
    arr = []
    for row in table:
        store = []
        q = (row[rowName].decode()).split(",")
        q = list(filter(None, q))
        for x in range(0, len(q)):
            q[x] = float(q[x])
        arr.append(q)
    table.flush()
    h5file.close()
    return(arr)
#max 5,000 following
#
def u_append_log(id, time, text, follows, followed, liked, tweeted):
    h5file = tables.open_file("twitter/twitterUser_log.h5", mode="a", title="twit")
    table = h5file.root.Null.Null
    r = table.row
    r["ID"] = id #encrypt
    r["time"] = time #encrypt
    r["text"] = text #encrypt
    r["follows"] = follows #encrypt
    r["followed"] = followed #encrypt
    r["liked"] = liked #encrypt
    r.append()
    table.flush()
    h5file.close()

class twitterTLog(tables.IsDescription):
    ID      = tables.StringCol(16)   # 16-character String
    time  = tables.StringCol(128)      # Signed 64-bit integer
    text  = tables.StringCol(500)   #500-character string
    author  = tables.StringCol(500)
    liked_pointers = tables.StringCol(5000)

#creates empty twitter log
#pass in twitterTLog class
def t_create_log(tL):
    h5file = tables.open_file("twitter/twitterTweet_log.h5", mode="w", title="twit2")
    group = h5file.create_group("/", 'Null', 'Twitter')
    table = h5file.create_table(group, 'Null', tL, "Twitter_Data")
    table.flush()
    h5file.close()

#pass in row title,
def t_dump_by_row(rowName):
    h5file = tables.open_file("twitter/twitterTweet_log.h5", mode="a", title="twit2")
    table = h5file.root.Null.Null
    arr = []
    for row in table:
        store = []
        q = (row[rowName].decode()).split(",")
        q = list(filter(None, q))
        for x in range(0, len(q)):
            q[x] = float(q[x])
        arr.append(q)
    table.flush()
    h5file.close()
    return(arr)

def t_append_log(id, time, text, author, liked):
    h5file = tables.open_file("twitter/twitterTweet_log.h5", mode="a", title="twit2")
    table = h5file.root.Null.Null
    r = table.row
    r["ID"] = id #encrypt
    r["time"] = time #encrypt
    r["text"] = text #encrypt
    r["author"] = follows #encrypt
    r["liked"] = followed #encrypt
    r.append()
    table.flush()
    h5file.close()

q = twitterTLog
q2 = twitterULog
u_create_log(q)
t_create_log(q2)
