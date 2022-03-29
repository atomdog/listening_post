#analysis_authority.py
import birdnest
import sentimentSample
#import chunkGen
import matplotlib.pyplot as plt
import matplotlib.dates
import seaborn as sns
from datetime import datetime
import re
import json
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import chunkGen
import more_itertools as itools
import textflow
from multiprocessing import Pool
#THIS IS A TERRIBLE FUNCTION IT NEEDS TO BE CHANGED
def generate_tweet_timeline_x(timestring):
    timestring = timestring.replace("[", '')
    timestring = timestring.replace("]", '')
    timestring = timestring.replace(':', " ")
    timestring = timestring.replace('-', " ")
    timestring = timestring.split(" ")
    for x in range(0, len(timestring)):
        timestring[x] = int(timestring[x])
    time = timestring
    time = datetime(time[0], time[1], time[2], time[3], time[4])
    return(time)

def coresent(clist):
    returnlist = []
    for iterat in range(0, len(clist)):
        q = sentimentSample.retsent(clist[iterat])
        returnlist.append(q)
        print(q)
        print(str((iterat/len(clist)*100))+"%")
    return(returnlist)

def core_rip_sentiment(cores):
    tweet_row = birdnest.t_dump_by_row('text')
    author = birdnest.t_dump_by_row('authorUSN')
    time = birdnest.t_dump_by_row('time')
    #inefficiency right here
    for x in range(0, len(tweet_row)):
        tweet_row[x] = tweet_row[x][0]
    tweetsforcores = [list(c) for c in itools.divide(cores, tweet_row)]
    with Pool(cores) as p:
        returnedlist = p.map(coresent, tweetsforcores)
    retval = []
    for x in range(0, len(returnedlist)):
        retval.extend(returnedlist[x])
    return(retval)

def stash_sentiment(di):
    for keyq in di:
        for x in range(0, len(di[keyq]['x'])):
            di[keyq]['x'][x] = str(di[keyq]['x'][x])
    with open('memory/analysis/sentimentstash.json', 'w') as outfile:
        json.dump(di, outfile)

def open_sentiment():
    with open('memory/analysis/sentimentstash.json') as json_file:
        data = json.load(json_file)
    for keyq in data:
        for x in range(0, len(data[keyq]['x'])):
            data[keyq]['x'][x] = generate_tweet_timeline_x(data[keyq]['x'][x])
    return(data)

def vis_sentiment(di):
    fig, ax = plt.subplots()
    colors  = sns.color_palette(None, len(di))
    it = 0
    for key in di:
        color = colors[it]


    plt.legend()
    plt.show()

def sentiment_by_author_ripped():
    graph_dict = {}
    #['2022-03-14 23:21:51']
    tweet_row = birdnest.t_dump_by_row('text')
    author = birdnest.t_dump_by_row('authorUSN')
    time = birdnest.t_dump_by_row('time')
    rippedlist = core_rip_sentiment(15)
    for x in range(0, len(tweet_row)):
        if(not (author[x][0] in graph_dict)):
            print("Creating dict for author: " + author[x][0])
            graph_dict[author[x][0]] = {"x": [], "y": []}
        timex = generate_tweet_timeline_x(time[x][0])
        graph_dict[author[x][0]]["x"].append(timex)

        sent = rippedlist[x]
        if(sent == 'Positive'):
            graph_dict[author[x][0]]["y"].append(1)
        elif(sent == 'Negative'):
            graph_dict[author[x][0]]["y"].append(-1)
        else:
            graph_dict[author[x][0]]["y"].append(0)
    stash_sentiment(graph_dict)

def sentiment_by_author_single_core():
    graph_dict = {}
    #['2022-03-14 23:21:51']
    tweet_row = birdnest.t_dump_by_row('text')
    author = birdnest.t_dump_by_row('authorUSN')
    time = birdnest.t_dump_by_row('time')
    for x in range(0, len(tweet_row)):
        if( not (author[x][0] in graph_dict)):
            print("Creating dict for author: " + author[x][0])
            graph_dict[author[x][0]] = {"x": [], "y": []}
        sent = sentimentSample.retsent(tweet_row[x][0])
        #append x
        timex = generate_tweet_timeline_x(time[x][0])
        graph_dict[author[x][0]]["x"].append(timex)
        #append sentiment
        if(sent == 'Positive'):
            graph_dict[author[x][0]]["y"].append(1)
        elif(sent == 'Negative'):
            graph_dict[author[x][0]]["y"].append(1)
        else:
            graph_dict[author[x][0]]["y"].append(0)
    for key in graph_dict:
        plt.plot(graph_dict[key]["x"], graph_dict[key]["y"], label=key)
    plt.legend()
    plt.show()

def chunk_by_tweet():
    spGen = chunkGen.chunkGenerator()
    #wait until generator is alive
    while(next(spGen)!=True):
        time.sleep(0.1)
    tweet_row = birdnest.t_dump_by_row('text')
    author = birdnest.t_dump_by_row('authorUSN')
    for x in range(0, len(tweet_row)):
        next(spGen)
        print(spGen.send(tweet_row[x][0])[2])
#chunk_by_tweet()
#sentiment_by_author_ripped()
graph_dict = open_sentiment()

class language_loop:
    def __init__(self):
        print("< ------- Text Flow Initializing ------ >")
        self.flow = textflow.stream().routine()
        self.seg_s = chunkGen.docprocgen()
        while(next(self.flow)!=True):
            time.sleep(0.1)
        while(next(self.seg_s)!=True):
            time.sleep(0.1)
        print("< ------- Text Flow Online ------ >")
    def read_complete_tweets(self):
        tweet_row = birdnest.t_dump_by_row('text')
        author = birdnest.t_dump_by_row('authorUSN')
        time = birdnest.t_dump_by_row('time')
        for x in range(0, len(tweet_row)):
            self.flow.send([author[x][0], tweet_row[x][0]])

q = language_loop()
q.read_complete_tweets()
