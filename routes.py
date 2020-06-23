import json

def load (demand):
    f = open (demand,)
    return json.load(f)
