## I assume that an empty route can load any single item
## I assume users can only buy in--stock goods

import json
import math
from route import *

WEIGHT   = 99
VOLUME   = 199
QUANTITY = 5
ENTRANCE = "MZ-1-000-000"

def load (demand_json):
    with open (demand_json,'r') as f:
        d = json.load(f)
    for i in d['demand']:
        i["unwatched"] = True
    return d

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

def closest (item, demand_items, stock):
    closest_sku         = demand_items[0]["sku"]
    closest_position    = next(iter(stock[closest_sku].keys()))
    min_distance        = label_distance(closest_position,item["stock_label"])
    i_min               = 0
    for k in range(len(demand_items)):
        if demand_items[k]["unwatched"]:
            for position in stock[demand_items[k]["sku"]]:
                d = label_distance(position, item["stock_label"])
                if d < min_distance:
                    closest_position = position
                    min_distance = d
                    i_min = k
    return i_min, closest_position, min_distance


data          = load("demand.json")
demand, stock = (data["demand"], data["stock"])

still_unwatched = len(demand) - 1
while len(demand) > 0:
    """demand2 = copy demand
    CONTINUE HERE ---> agregar un campo temporarily_watched en demand del json y poner
                 un if con eso en la local search y resetearlo cuando termina el ciclo de esa ruta
                 es mas, puedo poner temporarily_watched en todos los de igual sku porque el rechazo
                 va a ser por peso o volumen
    """
    last_item = { "sku" : "", "weight" : 0, "volume" : 0, "stock_label" : ENTRANCE }
    route     = Route([],WEIGHT,VOLUME,QUANTITY,0,True)
    demand_item_index, stock_label, min_distance = closest(last_item, demand, stock)
    last_item = demand.pop(demand_item_index)
    last_item["stock_label"] = stock_label
    last_item["added_distance"] = min_distance
    #print(last_item)
    # TODO Here an Item Class may become handy
    route.add_item(last_item)
    stock[last_item["sku"]][stock_label] -= 1
    if stock[last_item["sku"]][stock_label] == 0:
        stock[last_item["sku"]].pop(stock_label)
    while route.is_open() and len(demand)>0 and still_unwatched > 0:
        min_item_index, stock_label, min_distance = closest(last_item, demand, stock)
        candidate = demand[min_item_index].copy()
        if route.accepts(candidate):
            last_item = demand.pop(min_item_index)
            last_item["stock_label"]    = stock_label
            last_item["added_distance"] = min_distance
            route.add_item(last_item)
            stock[last_item["sku"]][stock_label] -= 1
            if stock[last_item["sku"]][stock_label] == 0:
                stock[last_item["sku"]].pop(stock_label)
        else:
            still_unwatched -= 1
            demand[min_item_index]["unwatched"] = False
            #TODO put unwatched in all the demand items with same sku
    still_unwatched = len(demand) - 1
    route.opened = False
    print(route)
