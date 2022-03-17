#twitter_lake.py

import numpy as np
import tables
import matplotlib.pyplot as plt
#supreme court
#by term lookup

class twitterULog(tables.IsDescription):
    ID            = tables.StringCol(32)    #32-character string
    username      = tables.StringCol(128)
    time_observed = tables.StringCol(128)   #128-character string
    username      = tables.StringCol(128)   #128-character string
    bio           = tables.StringCol(500)   #500-character string

    #need to track : following, followed, liked

    #follow_pointers = tables.StringCol(5000) #5000-character string
    #followed_pointers = tables.StringCol(5000) #5000-character string # 16-character String
    #liked_pointers = tables.StringCol(5000)
    #tweeted_pointers = tables.StringCol(5000)

#creates empty twitter log
#pass in twitterULog class
def u_create_log(tL):
    h5file = tables.open_file("twitter/userStore.h5", mode="w", title="twit")
    group = h5file.create_group("/", 'Null', 'Twitter')
    table = h5file.create_table(group, 'Null', tL, "Twitter_Data")
    table.flush()
    h5file.close()

#pass in row title,
def u_dump_by_row(rowName):
    h5file = tables.open_file("twitter/userStore.h5", mode="a", title="twit")
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
def u_append_log(id, time, text, follows, followed, liked, tweeted):
    h5file = tables.open_file("twitter/userStore.h5", mode="a", title="twit")
    table = h5file.root.Null.Null
    r = table.row
    r["ID"] = id #encrypt
    r["username"] = time #encrypt
    r["time_observed"] = text #encrypt
    r["bio"] = follows #encrypt
    r["followed"] = followed #encrypt
    r["liked"] = liked #encrypt
    r.append()
    table.flush()
    h5file.close()




#===================================== tweets side =======================
class twitterTLog(tables.IsDescription):
    tweet_ID      = tables.StringCol(32)
    time  = tables.StringCol(128)
    text  = tables.StringCol(500)
    authorUSN  = tables.StringCol(128)
    authorID  = tables.StringCol(128)
    likesNum = tables.StringCol(128)

    #liked_pointers = tables.StringCol(5000)
    #liked_pointers = tables.StringCol(5000)
    #liked_pointers = tables.StringCol(5000)

#creates empty twitter log
#pass in twitterTLog class
def t_create_log(tL):
    h5file = tables.open_file("twitter/tweetStore.h5", mode="w", title="twit2")
    group = h5file.create_group("/", 'Null', 'Twitter')
    table = h5file.create_table(group, 'Null', tL, "Twitter_Data")
    table.flush()
    h5file.close()

#pass in row title,
def t_dump_by_row(rowName):
    h5file = tables.open_file("twitter/tweetStore.h5", mode="a", title="twit2")
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
    h5file = tables.open_file("twitter/tweetStore.h5", mode="a", title="twit2")
    table = h5file.root.Null.Null
    r = table.row
    r["ID"] = id
    r["time"] = time
    r["text"] = text
    r["author"] = follows
    r["liked"] = followed
    r.append()
    table.flush()
    h5file.close()
    
#===================================== edges side =======================
class twitterELog(tables.IsDescription):
    ID_A  = tables.StringCol(32)
    ID_B  = tables.StringCol(32)
    #reply to, tweeted, follows, followed, liked
    type  = tables.StringCol(32)
def e_create_log(eL):
    h5file = tables.open_file("twitter/edgeStore.h5", mode="w", title="twit3")
    group = h5file.create_group("/", 'Null', 'Twitter')
    table = h5file.create_table(group, 'Null', eL, "Twitter_Data")
    table.flush()
    h5file.close()
def e_dump_by_row(rowName):
    h5file = tables.open_file("twitter/edgeStore.h5", mode="a", title="twit3")
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
def e_append_log(ID_A, ID_B, type):
    h5file = tables.open_file("twitter/edgeStore.h5", mode="a", title="twit3")
    table = h5file.root.Null.Null
    r = table.row
    r["ID_A"] = ID_A
    r["ID_B"] = ID_B
    r["type"] = type
    r.append()
    table.flush()
    h5file.close()

q = twitterTLog
q2 = twitterULog
u_create_log(q)
t_create_log(q2)
