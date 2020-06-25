import json
import math

class Item (object):

    def __init__ (self, sku, weight, volume, stock, position_labels, picked):
        self.sku                = sku
        self.weight             = weight
        self.volume             = volume
        self.stock              = stock
        self.position_labels    = position_labels
        self.picked             = False

    def distance (self, other):
        for label in self.position_labels:
            for label2 in other.position_labels:
                
        label_distance(l1,l2) for l1 in item1.labels() for l2 in item2.labels()
        return 0

    def closest (self, items = {}):

  
def load (demand):
    f = open (demand)
    d = json.load(f)
    items = { } # dictionary with Item class objects
    return items

def label_distance (label_one, label_two):
    """ 
    labels are MZ-1-003-008: 
                   area-floor-aisle-position 
    this distance takes everything as unitary

                                { -1 if even--odd
    horizontal_correction     = {  0 if same parity
                                { +1 if odd--even
    """
    pos             = [int(label_one[9:12]), int(label_two[9:12])]
    layers          = [math.ceil(pos[0]/2),math.ceil(pos[1]/2)]
    diff_position   = max(layers)-min(layers)
    print("diff_position {}".format(diff_position))
    aisles          = math.fabs(int(label_one[5:8]) - int(label_two[5:8]))
    print("aisles {}".format(aisles))
    horizontal_correction = (pos[0] % 2 - pos[1] % 2)
    print("horizontal_correction {}".format(horizontal_correction))
    crosses         = sum([int(i % 7 == 0) for i in range(min(layers),max(layers))])
    print("crosses {}".format(crosses))
    return 3*crosses + diff_position + 4*aisles + horizontal_correction
