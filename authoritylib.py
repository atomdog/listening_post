#authority.py

# ----- import statements ------
import pickle
import targetlib
import os
import csv
import json
import tw_ctrl

# -----                   ------

def freeze_authority(author):
    fh = open("memory/authorityonice.obj", 'wb')
    pickle.dump(author, fh)

def torch_authority():
    author = authority()
    fh = open("memory/authorityonice.obj", 'wb')
    pickle.dump(author, fh)

def thaw_authority():
    fh = open("memory/authorityonice.obj", 'rb')
    author = pickle.load(fh)
    return(author)

class authority:
    def __init__(self):
        self.targets = []
        #set up configuration
        with open('conf.json') as json_file:
            data = json.load(json_file)
        self.target_parameters = data['target_parameters']
        self.controller = tw_ctrl.ctrl()

    #fuzzy loading csv so we can be lazy later on
    def load_controller(self):
        self.controller = tw_ctrl.ctrl()

    def load_targets(self):
        path = "targeting/"
        q = os.listdir(path)
        q = sorted(q)
        for file in q:
            if file.endswith(".csv"):
                with open(path+file, mode='r') as csv_file:
                    print("===== Processing " + str(file) + " ===========")
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    col_names = []
                    self.load_controller()
                    for row in csv_reader:
                        if line_count == 0:
                            col_names = row
                            col_names = list((map(lambda x: x.lower(), col_names)))
                            line_count += 1
                        else:
                            new_target = targetlib.target()
                            new_target.meta = dict(zip(self.target_parameters, " "))
                            line_count += 1
                            for x in range(0, len(row)):
                                new_target.meta[col_names[x]] = row[x]
                            new_target.fuzz_self_init()
                            if('@' in new_target.meta['twitter']):
                                tw_id = self.controller.convert_username(new_target.meta['twitter'])
                                new_target.twitter_init(tw_id, new_target.meta['twitter'])
                            self.targets.append(new_target)
                    print("====== Processed " + str(file) + " ===========")
        freeze_authority(self)


q = torch_authority()
q = thaw_authority()
print(q.targets)
q.load_targets()
