import json
import math

def load (demand):
    f = open (demand,)
    return json.load(f)

def distance (label_one, label_two):
    """ labels are MZ-1-003-008: 
                   area-floor-aisle-position 

        this distance takes everything as unitary """
    aisles          = math.abs(int(label_one[5:8]) - int(label_two[5:8]))
    diff_position   = math.abs(int(label_one[9:12]) - int(label_two[9:12]))
    
    crosses         = how many mults of 7 between ?
    
    correction      =  0 if same pari
                      -1 if even--odd
                      +1 if odd--even  

    return 3*crosses + diff_position + 4*aisles + correction