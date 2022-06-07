#get_yt_transcript.py
from youtube_transcript_api import YouTubeTranscriptApi
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
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
def get_metadata(id):
    video_url = "https://www.youtube.com/watch?v=" + id
    session = HTMLSession()
    try:
        response = session.get(video_url)
        response.html.render(sleep=1)
        soup = bs(response.html.html, "html.parser")
        date = soup.find("meta", itemprop="datePublished")["content"]
        print(date)
        return(date)
    except Exception as e:
        print(e)
        return("")


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

        dt = get_metadata(line[0])
        transcripts_item = []
        with open("memory/youtube/"+ line[3]+"_"+line[0] + ".txt", 'w') as out:
            for b in range(0, len(q)):
                towrite = str(line[3])+ ': '
                for key in q[b]:
                    if(type(q[b][key]) == str):
                        q[b][key] = q[b][key].replace(",", "")
                        q[b][key] = q[b][key].replace(">", "")
                        q[b][key] = q[b][key].replace(u'\xa0', u' ')
                        q[b][key] = q[b][key].replace('\n', " ")
                        q[b][key] = q[b][key].lower()
                    towrite += str(q[b][key]) + ", "
                towrite += str(dt)
                if(dt==""):
                    dt = "0000-00-00"
                transcripts_item.append(str(towrite))
                out.write(str(towrite))
                out.write("\n")
        transcripts.append(transcripts_item)
    return(transcripts)
pull_by_file()
