import json
import math

class Item:

    def __init__ (self, sku, weight, volume, stock, position_labels, in_stock):
        self.sku                = sku
        self.weight             = weight
        self.volume             = volume
        self.stock              = stock
        self.position_labels    = position_labels
        self.in_stock           = self.stock != {}

        ## tal vez no haga falta: cuando arme la ruta
        #al meterlo en una ruta, hago item.pick() y mando {sku, position_label} a la ruta
        #y al item le decremento el stock de esa etiqueta
        ## aca poner algo que diga cual etiqueta de position fue ruteada
        ## self.picked_for_route   = 
        # ----> hace falta?? self.routed_label       = ''

    def get_sku (self):
        return self.sku

    def set_sku (self, a):
        self.sku = a

    def get_weight (self):
        return self.weight

    def set_weight (self, a):
        self.weight = a

    def get_volume (self):
        return self.volume

    def set_volume (self, a):
        self.volume = a

    def get_stock (self):
        return self.stock

    def set_stock (self, stock):
        self.stock = stock

    def get_position_labels (self):
        return self.position_labels

    def set_position_labels (self, a):
        self.position_labels = a
    
    def get_in_stock (self):
        return self.in_stock

    def set_in_stock (self, a):
        self.in_stock = a

    # def get_routed_label (self):
    #     return self.routed_label

    # 

    # def set_routed_label (self, label):
    #     self.routed_label = label

    def closest (self, items=[]):
        i = 0
        #while items[i].picked == True:
        #    i += 1
        the_closest         = items[i]
        min_label, min_dist = self.distance(the_closest)
        i_min = i
        for k in range(i+1,len(items)):
            if items[k].get_in_stock:
                l, d = self.distance(item)
                if d < min_dist:
                    min_label, min_dist = (l, d)
                    i_min = k
        #the_closest = items[i_min]
        #the_closest.set_routed_label(l)
        return i_min, min_label, min_dist

    def distance (self, other):
        return point_set_distance (self.picked_label, other.position_labels)

    def pick_for_route (self, position_label, route):
        self.picked_for_route       = route
        self.picked_label           = position_label
        self.stock[position_label] -= 1
        if self.stock[position_label] == 0:
            self.stock.pop(position_label)
  
def load (demand):
    with open (demand, 'r') as f:
        d = json.load(f)
    # q = d['stock']
    # identify by sku
    demand = { i["sku"] : i for i in d['demand'] }
    #weight = d[]
    #volume = d[]
    items = [] # list with Item class objects
    for sku, data in iter(demand.items()):
        item = Item(sku,data["weight"],data["volume"],d["stock"][sku],\
                    d['stock'][sku].keys(),True)
        items.append(item)
    return items

def label_distance (label_one, label_two):
    """ 
    labels are MZ-1-003-008: 
               area-floor-aisle-position 
    
    this distance takes everything as unitary
    and everything in same area -- same floor

                               { -1 if even - odd
    horizontal_correction    = {  0 if same parity
                               { +1 if odd - even
    """
    l = [label_one,label_two]
    l.sort()
    left, right = tuple(l)
    if left[5:8] == right[5:8] and int(left[9:12]) % 2 == 0:
        left, right = right, left
    aisles          = int(right[5:8]) - int(left[5:8])
    vert_pos_left, vert_pos_right = int(left[9:12]), int(right[9:12])
    layers        = [math.ceil(vert_pos_left/2),math.ceil(vert_pos_right/2)]
    diff_position = max(layers)-min(layers)
    horizontal_correction = vert_pos_left % 2 - vert_pos_right % 2
    crosses       = sum([int(i % 7 == 0) for i in range(min(layers),max(layers))])
    #print("aisles {}".format(aisles))
    #print("crosses {}".format(crosses))
    #print("horizontal_correction {}".format(horizontal_correction))
    #print("diff_position {}".format(diff_position))
    if crosses == 0 and aisles > 0:
        vertic_gap = min(layers[0] % 7 + layers[1] % 7, 16 - layers[0] % 7 - layers[1] % 7)
    else:
        vertic_gap = 3*crosses + diff_position
    horiz_gap = 4*aisles + horizontal_correction
    return vertic_gap + horiz_gap

def point_set_distance (current_label, other_labels):

    dist_realiz = other_labels[0]
    current_min = label_distance(dist_realiz,current_label)

    for label in other_labels:
        l_d = label_distance(label,current_label)
        if l_d < current_min:
            current_min = l_d
            dist_realiz = label

    return (dist_realiz,current_min)
