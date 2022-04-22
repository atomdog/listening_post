#get_yt_transcript.py
from youtube_transcript_api import YouTubeTranscriptApi
def a_return_transcript(id, start, finish):
    startpost = -1
    endpost = 100000000000000
    clippedtranscript = []
    isfloat = False

    if(start=="start" and finish =="finish"):
        print(id)
        print("Full video...")
        transcript = YouTubeTranscriptApi.get_transcript(id)
        return(transcript)
    else:
        if(finish != "finish"):
            endpost = float(finish)
        if(start!="start"):
            startpost = float(start)
        transcript = YouTubeTranscriptApi.get_transcript(id)
        #print(transcript)
        print(id)
        print(str(start), "->", str(finish))
        for x in range(0, len(transcript)):
            if(transcript[x]["start"] >=startpost and transcript[x]["start"]<=endpost):
                clippedtranscript.append(transcript[x])
    return(clippedtranscript)

def pull_by_file():
    file1 = open('targeting/youtubevideos.txt', 'r')
    Lines = file1.readlines()
    transcripts = []
    count = 0
    for line in Lines:
        count += 1
        line = line.strip()
        line = line.split(",")
        try:
            q = a_return_transcript(line[0], line[1], line[2])#,# line[3])
        except Exception as e:
            q = []
            print("Exception...")
            print(e)
            print("Ignoring video.......")
        #print(q)
        transcripts_item = []
        with open("memory/youtube/"+ line[3]+"_"+line[0] + ".txt", 'w') as out:
            for b in range(0, len(q)):
                towrite = str(line[3])+ ': '
                for key in q[b]:
                    towrite += str(q[b][key]) + ", "
                transcripts_item.append(str(towrite))
                out.write(str(towrite))
                out.write("\n")
        transcripts.append(transcripts_item)
    return(transcripts)
pull_by_file()
