import birdnest
def printfull():
    tweet_row = birdnest.t_dump_by_row('text')
    author = birdnest.t_dump_by_row('authorUSN')
    time = birdnest.t_dump_by_row('time')
    for x in range(0, len(tweet_row)):
        print("---------------")
        print(author[x][0])
        print(tweet_row[x][0])
