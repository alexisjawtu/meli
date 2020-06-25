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
        self.picked_label       = ''

    def closest (self, items = {}):
        for item in items:
            if item.picked == False:
                d = self.distance(self.picked_label,item)
***************                continue here

    def distance (self, other):
        return point_set_distance (self.picked_label, other.position_labels)

  
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

def point_set_distance (current_label, other_labels):

    dist_realiz = other_labels[0]
    current_min = label_distance(dist_realiz,current_label)

    for label in other_labels:
        l_d = label_distance(label,current_label)
        if l_d < current_min:
            current_min = l_d
            dist_realiz = label

    return (dist_realiz,current_min)
