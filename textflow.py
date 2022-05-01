#textflow.py
import semanticweb
import mod_wern
import re
import time

class stream():
    def __init__(self):
        self.recent_entities = []
        self.recent_chunks = []

        pass

    def split_sentences(self,blocktext):
        pass
    def resolve_source(self,voi):
        pass
    def unknown_resolve(self,voi):
        pass
    def subject_swap(self):
        pass
    def spin_trace(self):
        semanticweb.freeze_web(self.webo)
        print("< ------- Spinning Traces ------ >")
        self.webo.spinentitytrace()
        print("< ------- Traces Spun ------ >")
        semanticweb.freeze_web(self.webo)
        self.webo.export_to_json()
    def compare_speakers(self):
        print('<-- comparing speakers -->')
        self.webo.compare_all_speakers()
    def routine(self):
        print("<--- Thawing Semantic Web --->")
        #self.webo = semanticweb.torch_web()
        self.webo = semanticweb.thaw_web()
        print("<--- Semantic Web Thawed --->")
        #instantiate coroutines
        print("<--- Preparing Flows --->")
        self.wern = mod_wern.runnable()
        while(next(self.wern)!=True):
            time.sleep(0.1)
        print("<--- Flow to w Initialized --->")
        #init coroutines
        self.currentSF = next(self.wern)
        #enter loop
        yield(True)
        while(True):
            fpack = yield
            print("<-- Text Flow Processing Input -->")

            if(fpack is not None):
                fpack[1] = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|", "", fpack[1])
                #f = fpack[1]
                #send to w
                next(self.wern)
                self.currentSF = self.wern.send(fpack)
                #print(self.currentSF)
                nom = self.currentSF
                if(nom == None):
                    print("<---- ERR: w OFFLINE ---->")
                #check if w returned a viable processed sentence frame
                if(nom!= True and nom != None and nom['plaintext']!= None and len(nom['plaintext'])!=0):
                    #encounter in semantic web
                    self.webo.sentenceEncounter(self.currentSF, fpack[0], fpack[2], fpack[3], fpack[4], fpack[5])
                    #semanticweb.freeze_web(self.webo)
                    #spin traces in semantic web
                    #self.webo.spintrace()
                    #self.webo.export_to_json()
                    #print(self.webo.get_by_entity("PERSON"))
                    #webbedcontext = self.webo.aggregate_by_noun_chunks(self.webo.recent_entry())
                    print("<-- Text flow cycle complete -->")
                    yield("a")
                else:
                    pass
