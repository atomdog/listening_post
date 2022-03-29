#birdnest.py
import numpy as np
import tables
import matplotlib.pyplot as plt
import os
from datetime import datetime
import shutil

#check if unique!!

#================== user database ========================
class twitterULog(tables.IsDescription):
    ID            = tables.StringCol(32)    #32-character string
    username      = tables.StringCol(128)
    time_observed = tables.StringCol(128)   #128-character string
    username      = tables.StringCol(128)   #128-character string
    bio           = tables.StringCol(1024)   #500-character string

#creates empty user log
#pass in instance of twitterULog class
def u_create_log(uL):
    h5file = tables.open_file("memory/twitter/userStore.h5", mode="w", title="twit")
    group = h5file.create_group("/", 'Null', 'Twitter')
    table = h5file.create_table(group, 'Null', uL, "Twitter_Data")
    table.flush()
    h5file.close()

#pass in row title,
def u_dump_by_row(rowName):
    h5file = tables.open_file("memory/twitter/userStore.h5", mode="a", title="twit")
    table = h5file.root.Null.Null
    arr = []
    for row in table:
        store = []
        q = (row[rowName].decode()).split(",")
        q = list(filter(None, q))
        for x in range(0, len(q)):
            q[x] = q[x]
        arr.append(q)
    table.flush()
    h5file.close()
    return(arr)

def u_length():
    h5file = tables.open_file("memory/twitter/userStore.h5", mode="a", title="twit")
    table = h5file.root.Null.Null
    count=0
    for row in table:
        count+=1
    table.flush()
    h5file.close()
    return(count)

def u_append_log(id, username, time_observed, bio):
    h5file = tables.open_file("memory/twitter/userStore.h5", mode="a", title="twit")
    table = h5file.root.Null.Null
    r = table.row
    print("Storing User Data For: " + str(username) + ", ID: " + str(id))
    r["ID"] = id
    r["username"] = username
    r["time_observed"] = time_observed
    r["bio"] = bio
    r.append()
    table.flush()
    h5file.close()

#=========================================================
#================== tweet database =======================
class twitterTLog(tables.IsDescription):
    tweet_ID      = tables.StringCol(32)
    time          = tables.StringCol(128)
    text          = tables.StringCol(500)
    authorUSN     = tables.StringCol(128)
    authorID      = tables.StringCol(128)
    likesNum      = tables.StringCol(128)
    retweetsNum   = tables.StringCol(128)

#creates empty tweet log
#pass in instance of twitterTLog class
def t_create_log(tL):
    h5file = tables.open_file("memory/twitter/tweetStore.h5", mode="w", title="twit2")
    group = h5file.create_group("/", 'Null', 'Twitter')
    table = h5file.create_table(group, 'Null', tL, "Twitter_Data")
    table.flush()
    h5file.close()

#pass in row title,
def t_dump_by_row(rowName):
    h5file = tables.open_file("memory/twitter/tweetStore.h5", mode="a", title="twit2")
    table = h5file.root.Null.Null
    arr = []
    for row in table:
        store = []
        q = (row[rowName].decode()).split(",")
        q = list(filter(None, q))
        for x in range(0, len(q)):
            q[x] = q[x]
        arr.append(q)
    table.flush()
    h5file.close()
    return(arr)

def t_append_log(id, time, text, author, liked, retweets):
    h5file = tables.open_file("memory/twitter/tweetStore.h5", mode="a", title="twit2")
    table = h5file.root.Null.Null
    r = table.row
    print("Storing Tweet: @" + str(author) + ": " + str(text) +"("+str(id)+")")
    r["authorID"] = id.encode('utf-8')
    r["time"] = str(time).encode('utf-8')
    r["text"] = text.encode('utf-8')
    r["authorUSN"] = author.encode('utf-8')
    r["likesNum"] = str(liked).encode('utf-8')
    r['retweetsNum'] = str(retweets).encode('utf-8')
    r.append()
    table.flush()
    h5file.close()

#=========================================================
#=================== edge database =======================
class twitterELog(tables.IsDescription):
    ID_A  = tables.StringCol(32)
    ID_B  = tables.StringCol(32)
    #reply to, tweeted, follows, followed, liked
    type  = tables.StringCol(32)

#creates empty edge log
#pass in instance of twitterELog class
def e_create_log(eL):
    h5file = tables.open_file("memory/twitter/edgeStore.h5", mode="w", title="twit3")
    group = h5file.create_group("/", 'Null', 'Twitter')
    table = h5file.create_table(group, 'Null', eL, "Twitter_Data")
    table.flush()
    h5file.close()

#pass in name of row
def e_dump_by_row(rowName):
    h5file = tables.open_file("memory/twitter/edgeStore.h5", mode="a", title="twit3")
    table = h5file.root.Null.Null
    arr = []
    for row in table:
        store = []
        q = (row[rowName].decode()).split(",")
        q = list(filter(None, q))
        for x in range(0, len(q)):
            q[x] = q[x]
        arr.append(q)
    table.flush()
    h5file.close()
    return(arr)
def e_append_log(ID_A, ID_B, type):
    h5file = tables.open_file("memory/twitter/edgeStore.h5", mode="a", title="twit3")
    table = h5file.root.Null.Null
    r = table.row
    print("Storing Edge Data For: " + str(ID_A) + " --" + str(type) + "--> " + str(ID_B))
    r["ID_A"] = ID_A
    r["ID_B"] = ID_B
    r["type"] = type
    r.append()
    table.flush()
    h5file.close()
#=========================================================

def create_empty_logs():
    qU = twitterULog
    qT = twitterTLog
    qE = twitterELog
    #create logs from scratch
    u_create_log(qU)
    t_create_log(qT)
    e_create_log(qE)

def snapshot():
    now = datetime.now()
    dt_string = now.strftime("%d:%m:%Y:%H:%M:%S")
    shutil.copy("memory/twitter/edgeStore.h5", "memory/twitter/edgeStore_" + dt_string + ".h5")
    shutil.copy("memory/twitter/userStore.h5", "memory/twitter/userStore_" + dt_string + ".h5")
    shutil.copy("memory/twitter/tweetStore.h5", "memory/twitter/tweetStore_" + dt_string + ".h5")
#snapshot()
#create_empty_logs()
