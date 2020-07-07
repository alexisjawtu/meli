import sys
import json
import math
from   route  import *
from   output import *

# unitary distances
BOX                   = 1 # 1 BLOCK == 7 BOXES
AISLE                 = 4
CROSS                 = 3
MAX_PICKERS_PER_SIDE  = 3
MAX_PICKERS_PER_CROSS = 3
ENTRANCE              = "MZ-1-000-000"

def load (demand_json):

    with open (demand_json,'r') as f:
        d = json.load(f)
    return d

def check_collision_table(item,route,collision_table):

    check        = True
    picking_turn = route.quantity + 1
    position     = int(item["location"][9:12])
    aisle        = item["location"][5:8]
    last_aisle   = route.items[-1]["location"][5:8]
    block        = math.ceil(position/14)
    last_block   = math.ceil(int(route.items[-1]["location"][9:12])/14)
    side         = position % 2

    ## Restrictions
    # collisions along same picking-aisle
    key1  = "{}-{}-{}-{}".format(block,aisle,side,picking_turn)
    check = check and (len(collision_table.get(key1, [])) < MAX_PICKERS_PER_SIDE)

    # crossing diagonally passing through same cross-aisle, from a picking aisle
    # to another, in any direction
    aisle_seq     = sorted([int(aisle), int(last_aisle)])
    in_cross_keys = []
    if (math.fabs(block - last_block) == 1):
        cross = block -1
        for ai in range(aisle_seq[0],aisle_seq[1]):
            key2           = "{}-{}-{}-{}".format(picking_turn,cross,ai,ai+1)
            in_cross_keys += [key2]
            b              = len(collision_table.get(key2, [])) < MAX_PICKERS_PER_CROSS
            check          = check and b
    if (check): # update collision table occupying places
        collision_table[key1] = collision_table.get(key1, []) + [route.number]
        for key in in_cross_keys:
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
    if (left[5:8] == right[5:8] and int(left[9:12]) % 2 == 0):
        left, right = right, left
    aisles        = int(right[5:8]) - int(left[5:8])
    vert_pos_left, vert_pos_right = int(left[9:12]), int(right[9:12])
    layers        = [math.ceil(vert_pos_left/2),math.ceil(vert_pos_right/2)]
    diff_position = BOX*(max(layers)-min(layers))
    horizontal_correction = vert_pos_left % 2 - vert_pos_right % 2
    crosses       = sum([int(i % 7 == 0) for i in range(min(layers),max(layers))])
    if (crosses == 0 and aisles > 0):
        vertic_gap = min(layers[0] % 7 + layers[1] % 7, 16 - layers[0] % 7 - layers[1] % 7)
    else:
        vertic_gap = CROSS*crosses + diff_position
    horiz_gap = AISLE*aisles + horizontal_correction
    return vertic_gap + horiz_gap

def closest (item, demand_items, stock):

    i_min               = 0
    closest_sku         = demand_items[i_min]["sku"]
    closest_position    = next(iter(stock[closest_sku].keys()))
    min_distance        = label_distance(closest_position,item["location"])
    for k in range(len(demand_items)):
        if (demand_items[k]["unwatched"]):
            for position in stock[demand_items[k]["sku"]]:
                d = label_distance(position, item["location"])
                if (d < min_distance):
                    closest_position = position
                    min_distance     = d
                    i_min            = k
    return i_min, closest_position, min_distance

def unwatch_all(demand):

    for i in demand:
        i["unwatched"] = True

def main(json_file):

    data              = load(json_file)
    demand, stock     = (data["demand"], data["stock"])
    unwatch_all(demand)
    still_unwatched   = len(demand)
    forced            = len(demand)
    route_number      = 1
    turn              = 1 # we split the routes into picking turns
    collision_table   = {}
    output            = Output()
    output[turn]      = { "routes" : [] }

    k                 = 0
    while (len(demand) > 0 and k < forced):
        last_item = {
                        "sku"      :"",
                        "weight"   :0,
                        "quantity" :0,
                        "volume"   :0,
                        "location":ENTRANCE
                    }
        route     = Route(route_number,[last_item],0,0,0,0,True)
        while (route.is_open() and len(demand) > 0 and still_unwatched > 0):
            (min_item_index,location,min_distance) = closest(last_item,demand,
                                                                stock)
            candidate = {
                "sku"       : demand[min_item_index]["sku"],
                "weight"    : demand[min_item_index]["weight"],
                "volume"    : demand[min_item_index]["volume"],
                "location"  : location
            }
            if (route.accepts(candidate)
                    and check_collision_table(candidate,route,collision_table)):
                last_item = demand.pop(min_item_index)
                last_item["location"]    = location
                last_item["quantity"]    = stock[last_item["sku"]][location]
                last_item["added_distance"] = min_distance
                route.add_item(last_item)
                stock[last_item["sku"]][location]    -= 1
                if stock[last_item["sku"]][location] == 0:
                    stock[last_item["sku"]].pop(location)
            else:
                still_unwatched                    -= 1
                demand[min_item_index]["unwatched"] = False
        unwatch_all(demand)
        still_unwatched   = len(demand)
        route.opened      = False
        if (len(route.items[1:]) > 0):
            output[turn]["routes"] += [route.to_json()]
            route_number           += 1
        else:
            # now we are left with hanging items. Set collision_table 
            # equal to {} and start over for the next turn of routes.
            collision_table = {}
            turn           += 1
            output[turn]    = { "routes" : [] }
        del(route)
        k += 1
    
    if (k == forced):
        print("hangs")
        output.pop(turn)

    output.sort()
    output.to_json(json_file)
    output.to_tex(json_file)

if (__name__ == "__main__"):
    main(sys.argv[1])
