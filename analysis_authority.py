#analysis_authority.py
import birdnest
import sentimentSample
import chunkGen

def sentiment_by_tweet():
    tweet_row = birdnest.t_dump_by_row('text')
    author = birdnest.t_dump_by_row('authorUSN')

    for x in range(0, len(tweet_row)):
        print("---------")
        print(sentimentSample.retsent(tweet_row[x][0]))
        print(author[x][0])
        print("---------")
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
chunk_by_tweet()
#sentiment_by_tweet()
