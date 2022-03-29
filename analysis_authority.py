#analysis_authority.py
import birdnest
import sentimentSample
#import chunkGen
import matplotlib.pyplot
import matplotlib.dates
from datetime import datetime
import re
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

def sentiment_by_author():

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
sentiment_by_author()
