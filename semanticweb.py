#semantic node, ie word plus semantic meaning representation
import hashlib
import _pickle as pickle
import inspect#needed?

import json
import nltk
from nltk.corpus import stopwords
import random
import itertools
from datetime import datetime

import networkx as nx
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
#-------------- aidan's notes --------------------
#layer of action TRACKS in web *****!!!
#sem_edges have hash of two connecting words creating unique key for pairs of words
#perhaps a higher level edge for a->root->b
#-------------------------------------------------

def freeze_web(web_cl):
    fh = open("memory/serialized-instances/chillyWeb.obj", 'wb')
    pickle.dump(web_cl, fh)

def torch_web():
    web_cl = sw()
    fh = open("memory/serialized-instances/chillyWeb.obj", 'wb')
    pickle.dump(web_cl, fh)

def thaw_web():
    fh = open("memory/serialized-instances/chillyWeb.obj", 'rb')
    wewb = pickle.load(fh)
    return(wewb)


class sem_node:
    #'semantic hash' function
    #uniquely represents BOTH text and semantic form/meaning
    #superior to text as words which take different forms have different meanings
    def semHasher(self):
        self.semHash = hashlib.md5((self.text+self.form).encode()).hexdigest()

    def __init__(self, stringinit, POS, opos):
        self.inbound_edges  = []
        self.outbound_edges = []
        self.node_x = None
        self.node_y = None
        #textual representation
        self.text = stringinit
        #semantic POS
        self.form = POS
        self.score = 0
        self.alt_form = opos
        self.entity_tag = 'none'
        self.qual = "node"
        self.bind = None

        #semantic hash initialization
        self.semHash = None
        self.semHasher()
        #profile link
        #allows for direct resolution of subjects to other pieces of information
        self.profileLink = None
        self.individual_traces = []

class live_node:
    def semHasher(self):
        self.semHash = hashlib.md5((self.type).encode()).hexdigest()
    def __init__(self, stringinit, type):
        self.inbound_edges  = []
        self.outbound_edges = []
        self.node_x = None
        self.node_y = None
        #textual representation
        self.text = stringinit
        self.qual = "live_node"
        self.type = type
        self.entity_tag = self.type
        #semantic hash initialization
        self.semHash = None
        self.semHasher()
        #semantic POS (not relevant here)
        self.form = "live"
        self.alt_form = "none"
        self.profileLink = None
        #individual_traces
        self.individual_traces = []

class entity_node:
    def semHasher(self):
        self.semHash = hashlib.md5((self.type).encode()).hexdigest()
    def __init__(self, stringinit, type):
        self.inbound_edges  = []
        self.outbound_edges = []
        self.node_x = None
        self.node_y = None
        #textual representation
        self.text = stringinit
        self.qual = "entity_node"
        self.type = type
        self.entity_tag = self.type
        self.score = 1
        self.source = ""
        self.url = ""
        #semantic hash initialization
        self.semHash = None
        self.semHasher()
        #semantic POS (not relevant here)
        self.form = "entity"
        self.alt_form = "none"
        self.profileLink = None
        #individual_traces
        self.individual_traces = []

#carries meta-data for vector,
class sem_vector:
    def __init__(self):
        self.speaker = None
        self.frame = None
        #time metadata
        self.t = ""
        self.source = ""
        self.url = ""
        #sentence type
        self.type = None
        #actual vector
        self.track = []
        self.text = None
        self.chunk_indices = None
        self.entity_indices = None
        self.subj = None
        self.obj = None
        self.relation = None
        self.sentiment = None
        self.topic_clustering = None

    def resolve_chunk_indices(self):
        #print(self.frame['chunks'])
        ci =  []
        chunks = self.frame['chunks']
        for x in range(0, len(chunks)):
            cheld = chunks[x].split(' ')
            for y in range(0, len(cheld)):
                chunks.append(cheld[y])
        if(self.frame['chunks']==None):
            self.chunk_indices = ci
        elif(self.chunk_indices != None):
            if(len(self.chunk_indices)==0 or len(self.resolve_chunk_indices) >= 1):
                return(self.chunk_indices)
        else:
            for x in range(0, len(self.track)):
                if(self.track[x].qual == 'node'):
                    if(self.track[x].text in chunks):
                        ci.append(x)
            self.chunk_indices = ci
        #print(chunks)
        return(self.chunk_indices)

    def entify(self):
        #type_lookup = {"CARDINAL":0,"DATE":2,"EVENT":4,"FAC":6, "GPE":8, "LANGUAGE":10, "LAW":12, "LOC":14, "MONEY":16, "NORP":18, "ORDINAL":20, "ORG":22, "PERCENT":24, "PERSON":26, "PRODUCT":28, "QUANTITY":30, "TIME":32, "WORK_OF_ART":34}
        sep =  []
        cp = -1
        self.entity_indices = []
        ets = self.frame['entities']
        for x in range(0, len(ets)):
            eheld = ets[x][0].split(' ')
            sep.append([ets[x][1]])
            cp+=1
            for y in range(0, len(eheld)):
                sep[cp].append(eheld[y])
        for y in range(0, len(sep)):
            for x in range(0, len(self.track)):
                if(self.track[x].qual == 'node'):
                    totie = []
                    for z in range(1, len(sep[y])):
                        if(self.track[x].text == sep[y][z]):
                            self.track[x].entity_tag = sep[y][0]
                            totie.append(x)
                            self.entity_indices.append(x)
            if(len(totie)>0):
                q = entity_bind()
                q.points = totie
                for x in range(0, len(totie)):
                    self.track[x].bind = q
        return(self.entity_indices)


#semantic edge, ie connection between two semantic nodes
#carries sentiment charge, negation charge, semantic meaning type, and a weight
#weight is updated by encounter frequency

class sem_edge:
    def __init__(self):
        self.sentiment_charge = 0.0
        self.negation = 0.0
        self.type = None
        self.weight = 0.0
        self.qual = "edge"

class entity_bind:
    def __init__(self):
        self.points = []
        self.qual = "entity_bind"

#vertical traces across time/meaning
class noided:
    def __init__(self):
        self.end = True
        self.qual = "noid"

class sem_trace:
    def __init__(self, ax, ay, bx, by):
        #starting point
        #x is column, y is row
        self.ax = ax
        self.ay = ay
        #ending point
        self.bx = bx
        self.by = by

#semantic web
class sw:
    def __init__(self):
        #composed of semantic row adjacency vectors
        self.semWeb = []
        #composed of semantic column adjacency vectors
        self.semTrack = []
        #total nodes, for arbitrary querying
        self.nodeList  = []
        self.traces = []
        self.relationLabel = []
        self.init_special_nodes()
        self.e_types = [    "CARDINAL", "DATE",  "EVENT",  "FAC",        "GPE",       "LANGUAGE", "LAW",   "LOC",       "MONEY",    "NORP",   "ORDINAL",  "ORG",           "PERCENT",   "PERSON", "PRODUCT", "QUANTITY",     "TIME",  "WORK_OF_ART"]
        self.type_lookup = {"CARDINAL":0,"DATE":2,"EVENT":4,"FAC":6, "GPE":8, "LANGUAGE":10, "LAW":12, "LOC":14, "MONEY":16, "NORP":18, "ORDINAL":20, "ORG":22, "PERCENT":24, "PERSON":26, "PRODUCT":28, "QUANTITY":30, "TIME":32, "WORK_OF_ART":34}
    def init_special_nodes(self):
        types = [    "CARDINAL", "DATE",  "EVENT",  "FAC",        "GPE",       "LANGUAGE", "LAW",   "LOC",       "MONEY",    "NORP",   "ORDINAL",  "ORG",           "PERCENT",   "PERSON", "PRODUCT", "QUANTITY",     "TIME",  "WORK_OF_ART"]
        types_name = ["numbers", "dates", "events", "facilities", "countries", "language", "laws",  "locations", "monetary", "groups", "order",    "organization", "percentage", "people", "objects", "measurements", "times", "titles"]
        ctrack = []
        #make node for each type

        for ind in range(0, len(types)):
            q = entity_node(types_name[ind], types[ind])
            q.node_x = 0
            q.node_y = len(self.semWeb)
            #insert into nodelist
            self.nodeList.append(q)
            #insert into track for semvector
            ctrack.append(self.nodeList[ind])
            #add an edge
            co = sem_edge()
            ctrack.append(co)
            #noid
        end = noided()
        ctrack.append(end)
        #wrap in semvector
        forweb = sem_vector()
        forweb.text = types_name
        forweb.track = ctrack
        #insert into semweb
        self.semWeb.append(forweb)

    def state_insert(self, snf):
        #for creation of a 'live' state node

        pass

    def update_root_rep(self):
        bookmark = self.semWeb[self.recent_entry()].track
        current_root_rep = []
        for x in range(0, len(bookmark)):
            if(bookmark[x].qual == "node"):
                current_root_rep.append(bookmark[x].text)
        self.root_rep.append(current_root_rep)
        #print(self.root_rep)


    def recent_entry(self):
        if(len(self.semWeb)==0):
            return 0
        elif(len(self.semWeb)>=1):
            return(len(self.semWeb)-1)

    #nodes:
        #{
            #{key, label, tag, url, cluster, x, y, score}
            #{key, label, tag, url, cluster, x, y, score}
        #}

    #edges:
        #{
            #{key, key}
        #}
    #clusters
        #{
            #{key, color, label}
        #}

    def export_to_json(self):
        print("<--- EXPORTING TO JSON --->")
        json_node_form = []
        json_edge_form = []
        final_json = {}
        diff_ents = []
        diff_spk = ["symbolic"]
        diff_spk_y = [0]
        diff_source = [""]
        diff_date =[""]
        bumpbool = False
        #ry = r = lambda: random.randint()
        for row in range(0, len(self.semWeb)):
            for nodec in range(0, len(self.semWeb[row].track)):
                if((self.semWeb[row].track[nodec].qual == "node" or self.semWeb[row].track[nodec].qual == "entity_node") and self.semWeb[row].track[nodec].text != " "):
                    #self.semWeb[row].track[nodec].text
                    if(self.semWeb[row].track[nodec].entity_tag not in diff_ents):
                        diff_ents.append(self.semWeb[row].track[nodec].entity_tag)
                    if(self.semWeb[row].track[nodec].qual != "entity_node"):
                        if(self.semWeb[row].speaker not in diff_spk):
                            diff_spk.append(self.semWeb[row].speaker)
                            diff_spk_y.append(10)
                        if(self.semWeb[row].source not in diff_source):
                            diff_source.append(self.semWeb[row].source)
                        if(self.semWeb[row].t not in diff_source):
                            diff_date.append(self.semWeb[row].t)
                        x_start = (diff_spk.index(self.semWeb[row].speaker)*20)+20
                        y_start = diff_spk_y[diff_spk.index(self.semWeb[row].speaker)]
                        toadd = {'key':str(row)+'-'+str(nodec),'label':self.semWeb[row].track[nodec].text,'tag':self.semWeb[row].track[nodec].entity_tag,'date_spoken':self.semWeb[row].t,'score':self.semWeb[row].track[nodec].score, 'source':self.semWeb[row].source,'url':self.semWeb[row].url, 'cluster':self.semWeb[row].speaker,'x':x_start+nodec,'y':y_start}
                    else:
                        toadd={'key':str(row)+'-'+str(nodec),'label':self.semWeb[row].track[nodec].text,'tag':self.semWeb[row].track[nodec].entity_tag,'date_spoken':self.semWeb[row].t, 'source':self.semWeb[row].source,'score':self.semWeb[row].track[nodec].score, 'url':self.semWeb[row].url, 'cluster':'symbolic','x':nodec,'y':row}
                    json_node_form.append(toadd)
            if(self.semWeb[row].speaker!=None):
                diff_spk_y[diff_spk.index(self.semWeb[row].speaker)]+=2
        for x in range(0, len(self.traces)):
            target_node_x = self.semWeb[self.traces[x].ay].track[self.traces[x].ax]
            if(target_node_x.qual == "entity_node" or target_node_x.qual == "node"):
                s = str(self.traces[x].ay) +'-'+str(self.traces[x].ax)
                e = str(self.traces[x].by) +'-'+str(self.traces[x].bx)
            if([s,e] not in json_edge_form):
                json_edge_form.append([s,e])
        final_json['nodes'] = json_node_form
        final_json['edges'] = json_edge_form

        tagbuilder = []
        clusterbuilder = []
        sourcebuilder = []
        date_builder = []
        r = lambda: random.randint(0,255)

        for x in range(0, len(diff_spk)):
            clusterbuilder.append({'key': diff_spk[x], "color": '#%02X%02X%02X' % (r(),r(),r()), "clusterLabel":str(diff_spk[x])})
        for x in range(0, len(diff_ents)):
            tagbuilder.append({'key': diff_ents[x], "image":str(diff_ents[x])+".svg"})
        for x in range(0, len(diff_source)):
            sourcebuilder.append({'key': diff_source[x], "image":str(diff_source[x])+".svg"})
        #diff_date = diff_date.sort(key=lambda date: datetime.strptime(date, "%y-%m-%d"))
        for y in range(0, len(diff_date)):
            date_builder.append({'key': y, 'date':diff_date[y]})
        final_json['tags']=tagbuilder
        final_json['clusters']=clusterbuilder
        final_json['sources']=sourcebuilder
        final_json['date']=date_builder
        #print(final_json)
        with open('./viz/sigma.js-main/demo/public/dataset.json', 'w') as outfile:
            json.dump(final_json, outfile)

    def hash_word_combo(self, wordText, pos_tag):
        return(hashlib.md5((wordText+pos_tag).encode()))

    #find by hash
    def find_web_index_by_hash(self, to_locate_hash):
        #O(n) time
        indices = []
        rev_nodeList = self.nodeList
        rev_nodeList.reverse()
        for x in range(0, len(rev_nodeList)):
            if(rev_nodeList[x].semHash == to_locate_hash):
                #print(rev_nodeList[x].text)
                indices.append([rev_nodeList[x].node_x, rev_nodeList[x].node_y])
        return(indices)

    #find by text
    def find_web_index_by_text(self, to_locate_text):
        #O(n) time
        indices = []
        rev_nodeList = self.nodeList
        rev_nodeList.reverse()
        for x in range(0, len(rev_nodeList)):
            if(rev_nodeList[x].text == to_locate_text):
                indices.append([rev_nodeList[x].node_x, rev_nodeList[x].node_y])
        return(indices)
    #nodeEncounter, add semnode
    def nodeEncounter(self, frame, current):
        #get relevant information out of the sentence frame
        wordText = frame['plaintext'][current]
        pos_tag = frame['tokens'][current][1]
        opos_tag = frame['tokens'][current][4]
        ents = frame['entities']
        if(wordText=="nt"):
            wordText = "not"
        #check if text is within an entity
        #initialize node index as None
        currentNodeIndex = None
        #create node hash
        tenativeN = hashlib.md5((wordText+pos_tag).encode())
        self.nodeList.append(sem_node(wordText, pos_tag, opos_tag))
        #attach x,y coordinates to the node
        #we haven't appended to the semtrack or semweb so length is correct
        currentNodeIndex = len(self.nodeList)
        #if length of the nodeList is greater than 1 we can correct for off by 1 error
        if(len(self.nodeList)>=1):
            currentNodeIndex = currentNodeIndex-1
        self.nodeList[currentNodeIndex].node_x = len(self.semTrack)
        self.nodeList[currentNodeIndex].node_y = len(self.semWeb)
        """
        for eiter in range(0, len(ents)):
            if(wordText in ents[eiter][0]):
                self.nodeList[currentNodeIndex].entity_tag = ents[eiter][1]
        """
        #print(self.nodeList[currentNodeIndex].node_x, self.nodeList[currentNodeIndex].node_y)
        #return node index
        return(currentNodeIndex, frame['emotional_charge_vector'][current])



    def track_construction(self, sentFrame, current, sentcharge):
        #toss node into semtrack
        self.semTrack.append(self.nodeList[current])
        outbound_edge = sem_edge()
        if(self.nodeList[current].alt_form=="neg"):
            outbound_edge.negation = 1.0
        else:
            outbound_edge.negation = 0
        outbound_edge.sentiment_charge = sentcharge
        outbound_edge.type = None
        outbound_edge.weight = None
        self.semTrack.append(outbound_edge)


    def track_stop(self):
        q = noided()
        self.semTrack.append(q)

    #encounter sentence, words into nodes, create
    def sentenceEncounter(self, sentFrame, sourceFrame, sentiment, source, time, url):
        if(sentFrame == None):
            return False
        #print(sentFrame['plaintext'])
        for x in range(0, len(sentFrame['plaintext'])):
            if(sentFrame['plaintext'][x] == "nt"):
                sentFrame['plaintext'][x] == "not"
            current_nodeXval, sentcharge = self.nodeEncounter(sentFrame, x)
            #print(sentFrame['tokens'][x])
            if(current_nodeXval!=None):
                self.track_construction(sentFrame, current_nodeXval, sentcharge)
        #noid track
        self.track_stop()
        #init vector carrier
        vectorized = sem_vector()
        #pass track to vector
        vectorized.track = self.semTrack
        vectorized.frame = sentFrame
        vectorized.text = sentFrame['plaintext']
        vectorized.source = source
        vectorized.url = url
        vectorized.t = time
        #if we have a sentence type prediction, fill it in
        if(sentFrame['sent_type_pred']!=None):
            vectorized.type = sentFrame['sent_type_pred']
        vectorized.entify()
        vectorized.speaker = sentFrame['speaker']
        vectorized.sentiment = sentiment
        #slide in vector to web
        self.semWeb.append(vectorized)
        self.semTrack = []
    def spinentitytrace(self):
        self.traces = []
        totrace = {}
        scoredict = {}
        for x in range(0, len(self.nodeList)):
            scoredict[self.nodeList[x].text] = 0
        for iterator in range(0, len(self.nodeList)):
            #print(str(iterator)+ " of " + str(len(self.nodeList))+" (nodes)")
            cx = self.nodeList[iterator].node_x
            cy = self.nodeList[iterator].node_y
            self.nodeList[iterator].individual_traces = []
            self.semWeb[cy].track[cx].individual_traces = []
            if((self.nodeList[iterator].text in nltk.corpus.stopwords.words('english') or self.nodeList[iterator].text == " " or self.nodeList[iterator].text == "")):
                pass
            else:
                cnode = self.nodeList[iterator]
                cx = self.nodeList[iterator].node_x
                cy = self.nodeList[iterator].node_y
                '''
                if(self.nodeList[iterator].qual == 'node'):
                    scoredict[self.nodeList[iterator].text]+=1
                    self.semWeb[cy].track[cx].score = scoredict[self.nodeList[iterator].text]
                    cnode = self.nodeList[iterator]
                    cx = self.nodeList[iterator].node_x
                    cy = self.nodeList[iterator].node_y
                    found = self.find_web_index_by_text(self.semWeb[cy].track[cx].text)
                    for x in range(0, len(found)):
                        self.semWeb[cy].track[cx].individual_traces.append(sem_trace(cx, cy, found[x][0], found[x][1]))
                        self.nodeList[iterator].individual_traces.append(sem_trace(cx, cy, found[x][0], found[x][1]))
                        self.traces.append(sem_trace(cx, cy, found[x][0], found[x][1]))
                '''
                if(self.nodeList[iterator].entity_tag!='none' and self.nodeList[iterator].qual != 'entity_node'):
                    targetx = self.type_lookup[self.nodeList[iterator].entity_tag]
                    #print(targetx)
                    cnode = self.nodeList[iterator]
                    #print(self.semWeb[0].track[targetx].entity_tag + ": " + cnode.text)
                    print("Tying " + str(cnode.node_x) + ", " + str(cnode.node_y) + "--->" + str(targetx) + ', 0')
                    self.semWeb[cnode.node_y].track[cnode.node_x].individual_traces.append(sem_trace(cnode.node_x, cnode.node_y, targetx, 0))
                    self.semWeb[0].track[targetx].individual_traces.append(sem_trace(targetx, 0, cnode.node_x, cnode.node_y))
                    self.nodeList[iterator].individual_traces.append(sem_trace(cnode.node_x, cnode.node_y, targetx, 0))
                    self.traces.append(sem_trace(cnode.node_x,cnode.node_y, targetx, 0))
                    if(not(self.nodeList[iterator].text in totrace)):
                        totrace[self.nodeList[iterator].text] = []
                        totrace[self.nodeList[iterator].text].append(iterator)
                    else:
                        totrace[self.nodeList[iterator].text].append(iterator)
        for key in totrace:
            if(len(totrace[key])>1):
                for x in range(1, len(totrace[key])):
                    cnode = self.nodeList[totrace[key][x]]
                    targetx = self.nodeList[totrace[key][x-1]].node_x
                    targety = self.nodeList[totrace[key][x-1]].node_y
                    self.semWeb[cnode.node_y].track[cnode.node_x].individual_traces.append(sem_trace(cnode.node_x, cnode.node_y, targetx, targety))
                    self.semWeb[targety].track[targetx].individual_traces.append(sem_trace(targetx, targety, cnode.node_x, cnode.node_y))
                    self.nodeList[totrace[key][x]].individual_traces.append(sem_trace(cnode.node_x, cnode.node_y, targetx, targety))
                    self.traces.append(sem_trace(cnode.node_x,cnode.node_y, targetx, targety))
        print(totrace)
        #self.export_to_json()
    def similarity_by_speaker_entities(self,spk1,spk2):
        collected_1 = []
        collected_2 = []
        for x in range(0, len(self.semWeb)):
            if(self.semWeb[x].speaker == spk1):
                for y in range(0, len(self.semWeb[x].track)):
                    if(self.semWeb[x].track[y].qual=="node"):
                        if(self.semWeb[x].track[y].entity_tag!="none"):
                            collected_1.append(self.semWeb[x].track[y].text)
            if(self.semWeb[x].speaker == spk2):
                for y in range(0, len(self.semWeb[x].track)):
                    if(self.semWeb[x].track[y].qual=="node"):
                        if(self.semWeb[x].track[y].entity_tag!="none"):
                            collected_2.append(self.semWeb[x].track[y].text)
        collected_1 = set(collected_1)
        collected_2 = set(collected_2)
        intersection = collected_1.intersection(collected_2)
        union = collected_1.union(collected_2)
        return float(len(intersection)) / len(union)
    def similarity_by_speaker_text(self,spk1,spk2):
        collected_1 = []
        collected_2 = []
        for x in range(0, len(self.semWeb)):
            if(self.semWeb[x].speaker == spk1):
                for y in range(0, len(self.semWeb[x].text)):
                    collected_1.append(self.semWeb[x].text[y])
            if(self.semWeb[x].speaker == spk2):
                for y in range(0, len(self.semWeb[x].text)):
                    collected_2.append(self.semWeb[x].text[y])
        collected_1 = set(collected_1)
        collected_2 = set(collected_2)
        intersection = collected_1.intersection(collected_2)
        union = collected_1.union(collected_2)
        return float(len(intersection)) / len(union)
    def set_by_speaker_entities(self,spk1):
        collected_1 = []
        for x in range(0, len(self.semWeb)):
            if(self.semWeb[x].speaker == spk1):
                for y in range(0, len(self.semWeb[x].track)):
                    if(self.semWeb[x].track[y].qual=="node"):
                        if(self.semWeb[x].track[y].entity_tag!="none"):
                            collected_1.append(self.semWeb[x].track[y].text)
        collected_1 = set(collected_1)
        return(collected_1)

    def set_by_speaker_text(self,spk1):
        collected_1 = []
        collected_2 = []
        for x in range(0, len(self.semWeb)):
            if(self.semWeb[x].speaker == spk1):
                for y in range(0, len(self.semWeb[x].text)):
                    collected_1.append(self.semWeb[x].text[y])
        collected_1 = set(collected_1)
        return(collected_1)

    def venn_all_speakers(self):
        known_speakers = []
        known_speakers_dict = {}
        similarities = {}
        for x in range(0, len(self.semWeb)):
            if(not(self.semWeb[x].speaker in known_speakers) and self.semWeb[x].speaker != None):
                known_speakers.append(self.semWeb[x].speaker)
                known_speakers_dict[self.semWeb[x].speaker] = {}
                known_speakers_dict[self.semWeb[x].speaker] = {}
                known_speakers_dict[self.semWeb[x].speaker]['text'] = self.set_by_speaker_text(self.semWeb[x].speaker)
                known_speakers_dict[self.semWeb[x].speaker]['entities'] = self.set_by_speaker_entities(self.semWeb[x].speaker)
        textvenlist = []
        entityvenlist = []
        titlevenlist = []
        for key in known_speakers_dict:
            textvenlist.append(known_speakers_dict[key]['text'])
            entityvenlist.append(known_speakers_dict[key]['entities'])
            wordcloud = WordCloud(background_color="white").generate(" ".join(known_speakers_dict[key]['entities']))
            wordcloud.to_file(key+"_e_word_cloud.png")
            titlevenlist.append(key)
        titlevenlist = tuple(titlevenlist)
        return(known_speakers_dict)
    def compare_all_speakers(self):
        known_speakers = []
        known_speakers_dict = {}
        e_known_speakers_dict = {}
        similarities = {}
        for x in range(0, len(self.semWeb)):
            if(not(self.semWeb[x].speaker in known_speakers) and self.semWeb[x].speaker != None):
                known_speakers.append(self.semWeb[x].speaker)
                known_speakers_dict[self.semWeb[x].speaker] = {}
                e_known_speakers_dict[self.semWeb[x].speaker] = {}
        total_permutations = list(itertools.permutations(known_speakers, 2))
        e_total_permutations = list(itertools.permutations(known_speakers, 2))
        for y in range(0, len(total_permutations)):
            if(total_permutations[y][0]!=total_permutations[y][1]):
                known_speakers_dict[total_permutations[y][0]][total_permutations[y][1]] = (self.similarity_by_speaker_text(total_permutations[y][0],total_permutations[y][1]))
        for y in range(0, len(e_total_permutations)):
            if(e_total_permutations[y][0]!=e_total_permutations[y][1]):
                e_known_speakers_dict[total_permutations[y][0]][total_permutations[y][1]] = (self.similarity_by_speaker_entities(e_total_permutations[y][0],e_total_permutations[y][1]))


        #print(e_known_speakers_dict)
        G = nx.Graph()

        added = []
        count = 0
        summedweight = 0
        for key in e_known_speakers_dict:
            G.add_node(key)
            added.append(key)
            #print(key)
            #print(known_speakers_dict[key])
            for key2 in e_known_speakers_dict[key]:
                if(key in added):
                    summedweight+=e_known_speakers_dict[key][key2]
                    count+=1

        for key in e_known_speakers_dict:
            for key2 in e_known_speakers_dict[key]:
                G.add_edge(key,key2,weight=((e_known_speakers_dict[key][key2]*count)/summedweight))

        edge_weight = list(nx.get_edge_attributes(G,'weight').values())

        pos = nx.spring_layout(G, iterations=1000, k=0.1)
        nx.draw(G,pos, width=edge_weight, with_labels=True)
        plt.show()
        plt.clf()
        self.venn_all_speakers()
        return(known_speakers_dict)



#while loop for mutex, parse if semicolon

    def aggregate_by_noun_chunks(self, row_index):
        print("<--- Retrieving relevant sentences via noun chunks for:   -->")
        print(" ".join(self.semWeb[row_index].text))
        print("<------------------------------------------------------------> ")
        chunkindices = self.semWeb[row_index].resolve_chunk_indices()
        targeted_nodes = []
        aggregatedplaintext = []
        for x in range(0, len(chunkindices)):
            q = self.semWeb[row_index].track[chunkindices[x]]
            for x2 in range(0, len(q.individual_traces)):
                if(' ' in self.semWeb[q.individual_traces[x2].by].text):
                    self.semWeb[q.individual_traces[x2].by].text.remove(' ')
                aggregatedplaintext.append(" ".join(self.semWeb[q.individual_traces[x2].by].text))
        aggregatedplaintext = ". ".join(aggregatedplaintext)

        if(len(aggregatedplaintext)<10):
            aggregatedplaintext += " ".join(self.semWeb[row_index].text)
        print(aggregatedplaintext)
        return(aggregatedplaintext)


    def get_by_entity(self, type):
        key = self.type_lookup[type]
        elist = self.semWeb[0].track[key].individual_traces
        #print(key)
        #print(elist)
        aggregated =[]
        for x in range(0, len(elist)):
            #print(elist[x].by)
            aggregated.append([self.semWeb[elist[x].by].speaker,self.semWeb[elist[x].by].sentiment, self.semWeb[elist[x].by].track[elist[x].bx].text])
        return(aggregated)

    def aggregate_recent_conversation(self):
        aggregated = []
        return(aggregated)

    def aggregate_by_occurence(self, hash):
        aggregated =[]
        return(aggregated)

    def aggregate_by_speaker(self,spkid):
        aggregated =[]
        return(aggregated)







#need a handler to pass different types of statements in, ie add speaker if it was a spoken request
#automatically load and pass in commands

def handler(take_in):
    pass









#init vector with nodes,
#graph; time is y, word is X, thus we have a vector of length n, where n is number
#of known words (exposed semantic vocabulary)?

#connecting things between y axis? perhaps subjects, etc

#edges carry several charges across them
