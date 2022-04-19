#get_yt_transcript.py
from youtube_transcript_api import YouTubeTranscriptApi
def a_return_transcript(id, start, finish):
    startpost == 0
    endpost == 100000000000
    clippedtranscript = []
    if(start=="start" and finish =="finish"):
        transcript = YouTubeTranscriptApi.get_transcript(id)
        return(transcript)
    else:
        if(finish != "finish"):
            endpost = finish
        if(start!="start"):
            startpost = start
        transcript = YouTubeTranscriptApi.get_transcript(id)
        for x in range(0, len(transcript)):
            if(transcript[x]["start"]>=startpost and transcript[x]["start"]<=finishpost):
                clippedtranscript.append(startpost)
    return(clippedtranscript)

def pull_by_file():
    file1 = open('/targeting/youtubevideos.txt', 'r')
    Lines = file1.readlines()
    transcripts = []
    count = 0
    for line in Lines:
        count += 1
        line = line.strip()
        line = line.split(",")
        transcripts.append(a_return_transcript(line[0], line[1], line[2]))
    return(transcripts)
