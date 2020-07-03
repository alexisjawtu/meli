## I assume that an empty route can load any single item
## I assume users can only buy in--stock goods

import json
import math
from   route import *

# unitary distances
BOX   = 1 # 1 BLOCK == 7 BOXES
AISLE = 4
CROSS = 3
ENTRANCE = "MZ-1-000-000"

def load (demand_json):
    with open (demand_json,'r') as f:
        d = json.load(f)
    return d

def check_collision_table(stock_label,route,collision_table):
    picking_turn = route.quantity + 1
    position     = int(stock_label[9:12])
    aisle        = stock_label[5:8]
    side         = position % 2
    block        = math.ceil(position/14)
    key          = "{}-{}-{}-{}".format(block,aisle,side,picking_turn)
    check = False
    if (len(collision_table.get(key, [])) < 3):
        check = True
        # update table
        collision_table[key] = collision_table.get(key, []) + [route.number]
    return check


def label_distance (label_one, label_two):
    """ 
                                    { -1 if even - odd
        horizontal_correction    =  {  0 if same parity
                                    { +1 if odd - even
    """ 
    l = [label_one,label_two]
    l.sort()
    left, right   = tuple(l)
    if left[5:8] == right[5:8] and int(left[9:12]) % 2 == 0:
        left, right = right, left
    aisles        = int(right[5:8]) - int(left[5:8])
    vert_pos_left, vert_pos_right = int(left[9:12]), int(right[9:12])
    layers        = [math.ceil(vert_pos_left/2),math.ceil(vert_pos_right/2)]
    diff_position = BOX*(max(layers)-min(layers))
    horizontal_correction = vert_pos_left % 2 - vert_pos_right % 2
    crosses       = sum([int(i % 7 == 0) for i in range(min(layers),max(layers))])
    if crosses == 0 and aisles > 0:
        vertic_gap = min(layers[0] % 7 + layers[1] % 7, 16 - layers[0] % 7 - layers[1] % 7)
    else:
        vertic_gap = CROSS*crosses + diff_position
    horiz_gap = AISLE*aisles + horizontal_correction
    return vertic_gap + horiz_gap

def closest (item, demand_items, stock):
    i_min               = 0
    closest_sku         = demand_items[i_min]["sku"]
    closest_position    = next(iter(stock[closest_sku].keys()))
    min_distance        = label_distance(closest_position,item["stock_label"])
    for k in range(len(demand_items)):
        if demand_items[k]["unwatched"]:
            for position in stock[demand_items[k]["sku"]]:
                d = label_distance(position, item["stock_label"])
                if d < min_distance:
                    closest_position = position
                    min_distance     = d
                    i_min            = k
    return i_min, closest_position, min_distance

def unwatch_all(demand):
    for i in demand:
        i["unwatched"] = True


## main cycle   
data              = load("demand.json")
demand, stock     = (data["demand"], data["stock"])
unwatch_all(demand)
still_unwatched   = len(demand)
route_number      = 1
turn              = 1 # we split the routes into picking turns
collision_table   = {}
print(len(demand))
output = { "routes" : [] }

# this is a temporary forced stopping criterion.
#k=0
#w = len(demand)
while (len(demand) > 0):
    last_item = {"sku":"","weight":0,"volume":0,"stock_label":ENTRANCE}
    route     = Route(route_number,[],0,0,0,0,True)
    while (route.is_open() and len(demand) > 0 and still_unwatched > 0):
        min_item_index,stock_label,min_distance = closest(last_item,demand,
                                                          stock)
        candidate = demand[min_item_index]
        if (route.accepts(candidate)
                and check_collision_table(stock_label,route,collision_table)):
            last_item = demand.pop(min_item_index)
            last_item["stock_label"]    = stock_label
            last_item["added_distance"] = min_distance
            route.add_item(last_item)
            stock[last_item["sku"]][stock_label]    -= 1
            if stock[last_item["sku"]][stock_label] == 0:
                stock[last_item["sku"]].pop(stock_label)
        else:
            still_unwatched -= 1
            demand[min_item_index]["unwatched"] = False

    unwatch_all(demand)
    still_unwatched   = len(demand)
    route.opened      = False
    if (len(route.items) > 0):
        output["routes"] += [route.to_json()]
        route.to_txt()
        route_number     += 1
    else:
        # now we are left with hanging items. Set collision_table = {}
        # and start over for the next turn of routes
        collision_table = {}
        turn += 1
        with open ("output{}.json".format(turn),"w") as outfile:
            json.dump (output, outfile, indent = 4)
        output = { "routes" : [] }
    del(route)
    #k+=1
with open ("output{}.json".format(turn),"w") as outfile:
    json.dump (output, outfile, indent = 4)